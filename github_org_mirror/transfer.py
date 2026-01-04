"""GitHub repository transfer operations."""

import json
import subprocess
import time
from dataclasses import dataclass
from typing import List, Optional

from .utils import (
    build_github_url,
    print_error,
    print_info,
    print_success,
    print_warning,
    run_gh_command,
)


@dataclass
class Repository:
    """Represents a GitHub repository."""

    name: str
    owner: str
    full_name: str
    clone_url: str
    ssh_url: str
    is_private: bool
    is_archived: bool
    default_branch: str


def list_org_repos(org: str) -> List[Repository]:
    """List all repositories for an organization."""
    result = run_gh_command(
        [
            "repo",
            "list",
            org,
            "--limit",
            "500",
            "--json",
            "name,owner,nameWithOwner,url,sshUrl,isPrivate,isArchived,defaultBranchRef",
        ]
    )

    if result.returncode != 0:
        print_error(f"Failed to list repos for {org}: {result.stderr}")
        return []

    try:
        repos_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print_error(f"Failed to parse repo list for {org}")
        return []

    repos = []
    for repo in repos_data:
        default_branch = "main"
        if repo.get("defaultBranchRef"):
            default_branch = repo["defaultBranchRef"].get("name", "main")

        repos.append(
            Repository(
                name=repo["name"],
                owner=repo["owner"]["login"],
                full_name=repo["nameWithOwner"],
                clone_url=repo["url"] + ".git",
                ssh_url=repo.get("sshUrl", f"git@github.com:{repo['nameWithOwner']}.git"),
                is_private=repo.get("isPrivate", False),
                is_archived=repo.get("isArchived", False),
                default_branch=default_branch,
            )
        )

    return repos


def transfer_repo(owner: str, repo: str, new_owner: str) -> bool:
    """
    Transfer a repository to a new owner/organization.

    Note: GitHub has a ~24 hour cooldown between transfers of the same repo.
    """
    print_info(f"Transferring {owner}/{repo} to {new_owner}...")

    # Use GitHub API to initiate transfer
    result = run_gh_command(
        [
            "api",
            f"/repos/{owner}/{repo}/transfer",
            "-X",
            "POST",
            "-f",
            f"new_owner={new_owner}",
        ]
    )

    if result.returncode != 0:
        error_msg = result.stderr
        if "transfer is already pending" in error_msg.lower():
            print_warning(f"Transfer already pending for {repo}")
            return True
        if "must wait" in error_msg.lower() or "cooldown" in error_msg.lower():
            print_warning(f"Transfer cooldown active for {repo}. Please wait ~24 hours.")
            return False
        print_error(f"Failed to transfer {owner}/{repo}: {error_msg}")
        return False

    print_success(f"Transfer initiated for {repo} to {new_owner}")
    return True


def wait_for_transfer(new_owner: str, repo: str, timeout: int = 60) -> bool:
    """Wait for a repository transfer to complete."""
    print_info(f"Waiting for transfer to complete...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        # Check if repo exists in new location
        result = run_gh_command(["repo", "view", f"{new_owner}/{repo}", "--json", "name"])

        if result.returncode == 0:
            print_success(f"Transfer complete: {new_owner}/{repo}")
            return True

        time.sleep(2)

    print_warning(f"Transfer not complete within {timeout}s. It may still be processing.")
    return False


def clone_repo(
    owner: str,
    repo: str,
    dest_path: str,
    protocol: str = "ssh",
) -> bool:
    """Clone a repository to a local path."""
    url = build_github_url(owner, repo, protocol)

    result = subprocess.run(
        ["git", "clone", url, dest_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        # Check if it's just because the directory exists
        if "already exists" in result.stderr:
            print_warning(f"Repository {repo} already exists at {dest_path}")
            return True
        print_error(f"Failed to clone {owner}/{repo}: {result.stderr}")
        return False

    print_success(f"Cloned {owner}/{repo}")
    return True


def get_repo_info(owner: str, repo: str) -> Optional[Repository]:
    """Get information about a specific repository."""
    result = run_gh_command(
        [
            "repo",
            "view",
            f"{owner}/{repo}",
            "--json",
            "name,owner,nameWithOwner,url,sshUrl,isPrivate,isArchived,defaultBranchRef",
        ]
    )

    if result.returncode != 0:
        return None

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    default_branch = "main"
    if data.get("defaultBranchRef"):
        default_branch = data["defaultBranchRef"].get("name", "main")

    return Repository(
        name=data["name"],
        owner=data["owner"]["login"],
        full_name=data["nameWithOwner"],
        clone_url=data["url"] + ".git",
        ssh_url=data.get("sshUrl", f"git@github.com:{data['nameWithOwner']}.git"),
        is_private=data.get("isPrivate", False),
        is_archived=data.get("isArchived", False),
        default_branch=default_branch,
    )


def check_user_org_access(org: str) -> bool:
    """Check if user has access to transfer repos in an organization."""
    result = run_gh_command(["api", f"/orgs/{org}/memberships/${{user}}"])
    if result.returncode != 0:
        # Try checking if it's the user's own account
        result = run_gh_command(["api", "/user"])
        if result.returncode == 0:
            try:
                user_data = json.loads(result.stdout)
                return user_data.get("login") == org
            except json.JSONDecodeError:
                pass
        return False
    return True
