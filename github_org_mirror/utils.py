"""Shared utilities for github-org-mirror."""

import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from rich.console import Console

console = Console()


def is_git_repo(path: Path) -> bool:
    """Check if a directory is a git repository."""
    return (path / ".git").is_dir()


def get_repo_remote_url(path: Path) -> Optional[str]:
    """Get the origin remote URL for a git repository."""
    if not is_git_repo(path):
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def set_repo_remote_url(path: Path, url: str) -> bool:
    """Set the origin remote URL for a git repository."""
    if not is_git_repo(path):
        return False
    try:
        subprocess.run(
            ["git", "-C", str(path), "remote", "set-url", "origin", url],
            capture_output=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def parse_github_remote(url: str) -> Optional[Tuple[str, str]]:
    """Parse a GitHub remote URL and return (owner, repo) tuple."""
    # Handle SSH format: git@github.com:owner/repo.git
    if url.startswith("git@github.com:"):
        path = url[15:]  # Remove 'git@github.com:'
        if path.endswith(".git"):
            path = path[:-4]
        parts = path.split("/")
        if len(parts) == 2:
            return parts[0], parts[1]

    # Handle HTTPS format: https://github.com/owner/repo.git
    if "github.com/" in url:
        path = url.split("github.com/")[1]
        if path.endswith(".git"):
            path = path[:-4]
        parts = path.split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]

    return None


def build_github_url(owner: str, repo: str, protocol: str = "ssh") -> str:
    """Build a GitHub URL for cloning."""
    if protocol == "ssh":
        return f"git@github.com:{owner}/{repo}.git"
    return f"https://github.com/{owner}/{repo}.git"


def run_gh_command(args: list, capture_output: bool = True) -> subprocess.CompletedProcess:
    """Run a GitHub CLI command."""
    cmd = ["gh"] + args
    return subprocess.run(cmd, capture_output=capture_output, text=True)


def check_gh_auth() -> bool:
    """Check if GitHub CLI is authenticated."""
    result = run_gh_command(["auth", "status"])
    return result.returncode == 0


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[green]{message}[/green]")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[red]{message}[/red]")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]{message}[/yellow]")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[blue]{message}[/blue]")
