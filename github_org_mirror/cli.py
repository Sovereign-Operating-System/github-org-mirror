"""Command-line interface for github-org-mirror."""

import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import Config, DEFAULT_CONFIG_FILE, config_exists, get_config
from .sync import get_sync_status, init_local_structure, sync_github_to_local
from .utils import check_gh_auth, print_error, print_info, print_success, print_warning
from .watcher import RepoWatcher

console = Console()


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=False, path_type=Path),
    default=None,
    help="Path to config file",
)
@click.pass_context
def main(ctx: click.Context, config: Optional[Path]) -> None:
    """GitHub Org Mirror - Two-way sync between local folders and GitHub organizations."""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config


@main.command()
@click.option(
    "--base-path",
    "-p",
    type=click.Path(path_type=Path),
    default="~/Projects/orgs",
    help="Base path for organization folders",
)
@click.option(
    "--org",
    "-o",
    "orgs",
    multiple=True,
    help="Organization to sync (can be specified multiple times)",
)
@click.option(
    "--protocol",
    type=click.Choice(["ssh", "https"]),
    default="ssh",
    help="Git clone protocol",
)
@click.option(
    "--skip-clone",
    is_flag=True,
    help="Skip cloning repos, only create folder structure",
)
@click.pass_context
def init(
    ctx: click.Context,
    base_path: Path,
    orgs: tuple,
    protocol: str,
    skip_clone: bool,
) -> None:
    """Initialize local folder structure and clone all repos."""
    # Check gh auth first
    if not check_gh_auth():
        print_error("GitHub CLI is not authenticated. Run 'gh auth login' first.")
        sys.exit(1)

    if not orgs:
        print_error("At least one organization must be specified with --org/-o")
        sys.exit(1)

    config_path = ctx.obj.get("config_path")

    # Create config
    config = Config(
        base_path=str(base_path),
        organizations=list(orgs),
        clone_protocol=protocol,
    )

    print_info(f"Initializing with {len(orgs)} organization(s)")
    print_info(f"Base path: {config.base_path}")

    # Save config
    config.save(config_path)
    print_success(f"Configuration saved to: {config_path or DEFAULT_CONFIG_FILE}")

    if skip_clone:
        # Just create directories
        config.base_path.mkdir(parents=True, exist_ok=True)
        for org in config.organizations:
            org_path = config.get_org_path(org)
            org_path.mkdir(parents=True, exist_ok=True)
            print_success(f"Created: {org_path}")
    else:
        # Full init with cloning
        result = init_local_structure(config)

        # Print summary
        console.print()
        console.print("[bold]Initialization Complete[/bold]")
        console.print(f"  Cloned: {len(result.cloned)} repos")
        if result.errors:
            console.print(f"  Errors: {len(result.errors)}")
            for error in result.errors:
                print_error(f"    {error}")


@main.command()
@click.option("--clone/--no-clone", default=True, help="Clone missing repos")
@click.option("--move/--no-move", default=True, help="Move misplaced repos")
@click.option("--dry-run", is_flag=True, help="Show what would be done without doing it")
@click.pass_context
def sync(ctx: click.Context, clone: bool, move: bool, dry_run: bool) -> None:
    """Sync GitHub state to local folders."""
    config_path = ctx.obj.get("config_path")

    if not config_exists(config_path):
        print_error("No configuration found. Run 'github-org-mirror init' first.")
        sys.exit(1)

    if not check_gh_auth():
        print_error("GitHub CLI is not authenticated. Run 'gh auth login' first.")
        sys.exit(1)

    config = get_config(config_path)

    if dry_run:
        print_warning("DRY RUN - no changes will be made")

    result = sync_github_to_local(
        config,
        clone_missing=clone,
        move_misplaced=move,
        dry_run=dry_run,
    )

    # Print summary
    console.print()
    console.print("[bold]Sync Complete[/bold]")
    console.print(f"  Cloned: {len(result.cloned)}")
    console.print(f"  Moved: {len(result.moved)}")
    console.print(f"  Orphaned: {len(result.orphaned)}")
    if result.errors:
        console.print(f"  Errors: {len(result.errors)}")


@main.command()
@click.pass_context
def watch(ctx: click.Context) -> None:
    """Watch for repo moves and sync to GitHub."""
    config_path = ctx.obj.get("config_path")

    if not config_exists(config_path):
        print_error("No configuration found. Run 'github-org-mirror init' first.")
        sys.exit(1)

    if not check_gh_auth():
        print_error("GitHub CLI is not authenticated. Run 'gh auth login' first.")
        sys.exit(1)

    config = get_config(config_path)

    def on_transfer(src_org: str, dest_org: str, repo: str) -> None:
        console.print(f"[green]Transferred: {src_org}/{repo} -> {dest_org}/{repo}[/green]")

    watcher = RepoWatcher(config, on_transfer=on_transfer)

    console.print("[bold]Starting file watcher...[/bold]")
    console.print("Move repos between org folders to trigger GitHub transfers.")
    console.print("Press Ctrl+C to stop.\n")

    watcher.run_forever()


@main.command()
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information")
@click.pass_context
def status(ctx: click.Context, verbose: bool) -> None:
    """Show current sync status."""
    config_path = ctx.obj.get("config_path")

    if not config_exists(config_path):
        print_error("No configuration found. Run 'github-org-mirror init' first.")
        sys.exit(1)

    if not check_gh_auth():
        print_error("GitHub CLI is not authenticated. Run 'gh auth login' first.")
        sys.exit(1)

    config = get_config(config_path)
    status_info = get_sync_status(config)

    # Summary table
    table = Table(title="Sync Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Local repos", str(status_info["local_repos"]))
    table.add_row("GitHub repos", str(status_info["github_repos"]))
    table.add_row("Misplaced", str(status_info["misplaced"]))
    table.add_row("Missing locally", str(status_info["missing"]))
    table.add_row("Orphaned locally", str(status_info["orphaned"]))

    sync_status = "[green]In Sync[/green]" if status_info["in_sync"] else "[yellow]Out of Sync[/yellow]"
    table.add_row("Status", sync_status)

    console.print(table)

    if verbose and not status_info["in_sync"]:
        details = status_info["details"]

        if details["misplaced"]:
            console.print("\n[bold]Misplaced Repos:[/bold]")
            for repo, from_org, to_org, _ in details["misplaced"]:
                console.print(f"  {repo}: {from_org} -> should be in {to_org}")

        if details["missing"]:
            console.print("\n[bold]Missing Locally:[/bold]")
            for org, repo, _ in details["missing"]:
                console.print(f"  {org}/{repo}")

        if details["orphaned"]:
            console.print("\n[bold]Orphaned (not on GitHub):[/bold]")
            for org, repo, _ in details["orphaned"]:
                console.print(f"  {org}/{repo}")


@main.command("config")
@click.option("--show", is_flag=True, help="Show current configuration")
@click.option("--add-org", help="Add an organization")
@click.option("--remove-org", help="Remove an organization")
@click.pass_context
def config_cmd(
    ctx: click.Context,
    show: bool,
    add_org: Optional[str],
    remove_org: Optional[str],
) -> None:
    """View or modify configuration."""
    config_path = ctx.obj.get("config_path")

    if not config_exists(config_path):
        print_error("No configuration found. Run 'github-org-mirror init' first.")
        sys.exit(1)

    config = get_config(config_path)

    if add_org:
        if add_org not in config.organizations:
            config.organizations.append(add_org)
            config.save(config_path)
            print_success(f"Added organization: {add_org}")
        else:
            print_warning(f"Organization already exists: {add_org}")
        return

    if remove_org:
        if remove_org in config.organizations:
            config.organizations.remove(remove_org)
            config.save(config_path)
            print_success(f"Removed organization: {remove_org}")
        else:
            print_warning(f"Organization not found: {remove_org}")
        return

    # Default: show configuration
    table = Table(title="Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Config file", str(config_path or DEFAULT_CONFIG_FILE))
    table.add_row("Base path", str(config.base_path))
    table.add_row("Clone protocol", config.clone_protocol)
    table.add_row("Sync interval", f"{config.sync_interval}s")
    table.add_row("Auto update remotes", str(config.auto_update_remotes))
    table.add_row("Organizations", str(len(config.organizations)))

    console.print(table)

    if config.organizations:
        console.print("\n[bold]Organizations:[/bold]")
        for org in config.organizations:
            console.print(f"  - {org}")


if __name__ == "__main__":
    main()
