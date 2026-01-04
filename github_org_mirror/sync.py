"""GitHub to local sync operations."""

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import Config
from .transfer import Repository, clone_repo, list_org_repos
from .utils import (
    get_repo_remote_url,
    is_git_repo,
    parse_github_remote,
    print_error,
    print_info,
    print_success,
    print_warning,
    set_repo_remote_url,
    build_github_url,
)


@dataclass
class SyncResult:
    """Result of a sync operation."""

    cloned: List[str]
    moved: List[Tuple[str, str, str]]  # (repo, from_org, to_org)
    orphaned: List[str]
    errors: List[str]


def get_local_repos(config: Config) -> Dict[str, Dict[str, Path]]:
    """
    Get all local repositories organized by org.

    Returns: {org: {repo_name: path}}
    """
    result: Dict[str, Dict[str, Path]] = {}

    for org in config.organizations:
        org_path = config.get_org_path(org)
        result[org] = {}

        if not org_path.exists():
            continue

        for item in org_path.iterdir():
            if item.is_dir() and is_git_repo(item):
                result[org][item.name] = item

    return result


def get_github_repos(config: Config) -> Dict[str, Dict[str, Repository]]:
    """
    Get all GitHub repositories organized by org.

    Returns: {org: {repo_name: Repository}}
    """
    result: Dict[str, Dict[str, Repository]] = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        for org in config.organizations:
            task = progress.add_task(f"Fetching repos for {org}...", total=None)
            repos = list_org_repos(org)
            result[org] = {}

            for repo in repos:
                if repo.name not in config.exclude_repos:
                    result[org][repo.name] = repo

            progress.remove_task(task)

    return result


def find_misplaced_repos(
    local_repos: Dict[str, Dict[str, Path]],
    github_repos: Dict[str, Dict[str, Repository]],
) -> List[Tuple[str, str, str, Path]]:
    """
    Find repos that are in the wrong local org folder.

    Returns: List of (repo_name, current_local_org, correct_org, local_path)
    """
    misplaced = []

    # Build a map of where each repo should be according to GitHub
    github_locations: Dict[str, str] = {}
    for org, repos in github_repos.items():
        for repo_name in repos:
            github_locations[repo_name] = org

    # Check local repos against GitHub locations
    for local_org, repos in local_repos.items():
        for repo_name, path in repos.items():
            if repo_name in github_locations:
                correct_org = github_locations[repo_name]
                if correct_org != local_org:
                    misplaced.append((repo_name, local_org, correct_org, path))

    return misplaced


def find_missing_repos(
    local_repos: Dict[str, Dict[str, Path]],
    github_repos: Dict[str, Dict[str, Repository]],
) -> List[Tuple[str, str, Repository]]:
    """
    Find repos that exist on GitHub but not locally.

    Returns: List of (org, repo_name, Repository)
    """
    missing = []

    for org, repos in github_repos.items():
        local_org_repos = local_repos.get(org, {})
        for repo_name, repo in repos.items():
            if repo_name not in local_org_repos:
                missing.append((org, repo_name, repo))

    return missing


def find_orphaned_repos(
    local_repos: Dict[str, Dict[str, Path]],
    github_repos: Dict[str, Dict[str, Repository]],
) -> List[Tuple[str, str, Path]]:
    """
    Find repos that exist locally but not on GitHub.

    Returns: List of (org, repo_name, path)
    """
    orphaned = []

    # Build set of all GitHub repos
    github_repo_names: Set[str] = set()
    for repos in github_repos.values():
        github_repo_names.update(repos.keys())

    for org, repos in local_repos.items():
        for repo_name, path in repos.items():
            if repo_name not in github_repo_names:
                orphaned.append((org, repo_name, path))

    return orphaned


def sync_github_to_local(
    config: Config,
    clone_missing: bool = True,
    move_misplaced: bool = True,
    dry_run: bool = False,
) -> SyncResult:
    """
    Sync GitHub state to local folders.

    Args:
        config: Configuration object
        clone_missing: Whether to clone repos that exist on GitHub but not locally
        move_misplaced: Whether to move repos to correct org folders
        dry_run: If True, only report what would be done

    Returns: SyncResult with details of operations performed
    """
    result = SyncResult(cloned=[], moved=[], orphaned=[], errors=[])

    print_info("Fetching repository information...")
    local_repos = get_local_repos(config)
    github_repos = get_github_repos(config)

    # Ensure org directories exist
    if not dry_run:
        for org in config.organizations:
            org_path = config.get_org_path(org)
            org_path.mkdir(parents=True, exist_ok=True)

    # Handle misplaced repos
    if move_misplaced:
        misplaced = find_misplaced_repos(local_repos, github_repos)
        for repo_name, from_org, to_org, current_path in misplaced:
            if dry_run:
                print_info(f"Would move {repo_name}: {from_org} -> {to_org}")
                result.moved.append((repo_name, from_org, to_org))
            else:
                new_path = config.get_repo_path(to_org, repo_name)
                try:
                    print_info(f"Moving {repo_name}: {from_org} -> {to_org}")
                    shutil.move(str(current_path), str(new_path))

                    # Update remote URL
                    if config.auto_update_remotes:
                        new_url = build_github_url(to_org, repo_name, config.clone_protocol)
                        set_repo_remote_url(new_path, new_url)

                    result.moved.append((repo_name, from_org, to_org))
                    print_success(f"Moved {repo_name} to {to_org}")
                except Exception as e:
                    error_msg = f"Failed to move {repo_name}: {e}"
                    print_error(error_msg)
                    result.errors.append(error_msg)

    # Handle missing repos
    if clone_missing:
        missing = find_missing_repos(local_repos, github_repos)
        for org, repo_name, repo in missing:
            dest_path = config.get_repo_path(org, repo_name)
            if dry_run:
                print_info(f"Would clone {org}/{repo_name}")
                result.cloned.append(f"{org}/{repo_name}")
            else:
                if clone_repo(org, repo_name, str(dest_path), config.clone_protocol):
                    result.cloned.append(f"{org}/{repo_name}")
                else:
                    result.errors.append(f"Failed to clone {org}/{repo_name}")

    # Find orphaned repos (just report, don't delete)
    orphaned = find_orphaned_repos(local_repos, github_repos)
    for org, repo_name, path in orphaned:
        result.orphaned.append(f"{org}/{repo_name}")
        if orphaned:
            print_warning(f"Orphaned repo (not on GitHub): {org}/{repo_name}")

    return result


def init_local_structure(config: Config) -> SyncResult:
    """
    Initialize local folder structure and clone all repos.

    This creates org directories and clones all repos from GitHub.
    """
    print_info(f"Initializing local structure at: {config.base_path}")

    # Create base path
    config.base_path.mkdir(parents=True, exist_ok=True)

    # Create org directories
    for org in config.organizations:
        org_path = config.get_org_path(org)
        org_path.mkdir(parents=True, exist_ok=True)
        print_success(f"Created directory: {org_path}")

    # Clone all repos
    return sync_github_to_local(
        config,
        clone_missing=True,
        move_misplaced=True,
        dry_run=False,
    )


def get_sync_status(config: Config) -> Dict:
    """
    Get current sync status.

    Returns a dict with sync state information.
    """
    local_repos = get_local_repos(config)
    github_repos = get_github_repos(config)

    misplaced = find_misplaced_repos(local_repos, github_repos)
    missing = find_missing_repos(local_repos, github_repos)
    orphaned = find_orphaned_repos(local_repos, github_repos)

    local_count = sum(len(repos) for repos in local_repos.values())
    github_count = sum(len(repos) for repos in github_repos.values())

    return {
        "local_repos": local_count,
        "github_repos": github_count,
        "misplaced": len(misplaced),
        "missing": len(missing),
        "orphaned": len(orphaned),
        "in_sync": len(misplaced) == 0 and len(missing) == 0,
        "details": {
            "misplaced": misplaced,
            "missing": missing,
            "orphaned": orphaned,
        },
    }
