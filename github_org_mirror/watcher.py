"""File system watcher for detecting repo moves between org folders."""

import threading
import time
from pathlib import Path
from typing import Callable, Dict, Optional, Set

from watchdog.events import DirMovedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .config import Config
from .transfer import transfer_repo, wait_for_transfer
from .utils import (
    build_github_url,
    is_git_repo,
    parse_github_remote,
    get_repo_remote_url,
    print_error,
    print_info,
    print_success,
    print_warning,
    set_repo_remote_url,
)


class OrgMoveHandler(FileSystemEventHandler):
    """Handles directory move events between organization folders."""

    def __init__(self, config: Config, on_transfer: Optional[Callable] = None):
        super().__init__()
        self.config = config
        self.on_transfer = on_transfer
        self.pending_moves: Dict[str, float] = {}
        self.processed_moves: Set[str] = set()
        self._lock = threading.Lock()
        # Debounce time to handle rapid successive events
        self.debounce_seconds = 2.0

    def _get_org_from_path(self, path: Path) -> Optional[str]:
        """Extract organization name from a path under base_path."""
        try:
            rel_path = path.relative_to(self.config.base_path)
            parts = rel_path.parts
            if parts:
                return parts[0]
        except ValueError:
            pass
        return None

    def _is_direct_child(self, path: Path, parent: Path) -> bool:
        """Check if path is a direct child of parent (one level deep)."""
        try:
            rel_path = path.relative_to(parent)
            return len(rel_path.parts) == 1
        except ValueError:
            return False

    def on_moved(self, event):
        """Handle directory moved events."""
        if not isinstance(event, DirMovedEvent):
            return

        src_path = Path(event.src_path)
        dest_path = Path(event.dest_path)

        # Only process moves that are direct children of org folders
        # (i.e., repo-level moves, not nested directories)
        src_org = self._get_org_from_path(src_path)
        dest_org = self._get_org_from_path(dest_path)

        if not src_org or not dest_org:
            return

        # Check if this is a repo-level move (direct child of org folder)
        src_org_path = self.config.base_path / src_org
        dest_org_path = self.config.base_path / dest_org

        if not self._is_direct_child(src_path, src_org_path):
            return
        if not self._is_direct_child(dest_path, dest_org_path):
            return

        # Same org, just a rename within the org - ignore
        if src_org == dest_org:
            print_info(f"Repo renamed within {src_org}: {src_path.name} -> {dest_path.name}")
            return

        # Check if destination is a git repo
        if not is_git_repo(dest_path):
            print_warning(f"Moved folder is not a git repo: {dest_path}")
            return

        # Debounce - avoid processing the same move multiple times
        move_key = f"{src_path}:{dest_path}"
        with self._lock:
            now = time.time()
            if move_key in self.pending_moves:
                if now - self.pending_moves[move_key] < self.debounce_seconds:
                    return
            self.pending_moves[move_key] = now

        # Process the move in a separate thread to avoid blocking
        thread = threading.Thread(
            target=self._process_move,
            args=(src_org, dest_org, src_path, dest_path),
            daemon=True,
        )
        thread.start()

    def _process_move(
        self, src_org: str, dest_org: str, src_path: Path, dest_path: Path
    ) -> None:
        """Process a repo move between organizations."""
        repo_name = dest_path.name

        # Get repo info from git remote
        remote_url = get_repo_remote_url(dest_path)
        if not remote_url:
            print_error(f"Could not get remote URL for {repo_name}")
            return

        parsed = parse_github_remote(remote_url)
        if not parsed:
            print_error(f"Could not parse GitHub remote URL: {remote_url}")
            return

        current_owner, repo = parsed

        # Verify the repo is currently in src_org
        if current_owner != src_org:
            print_warning(
                f"Repo {repo} remote shows owner as {current_owner}, "
                f"but was moved from {src_org}. Skipping transfer."
            )
            return

        print_info(f"Detected move: {src_org}/{repo} -> {dest_org}/{repo}")

        # Initiate the transfer
        if transfer_repo(src_org, repo, dest_org):
            # Wait for transfer to complete
            if wait_for_transfer(dest_org, repo, timeout=120):
                # Update local remote URL
                if self.config.auto_update_remotes:
                    new_url = build_github_url(dest_org, repo, self.config.clone_protocol)
                    if set_repo_remote_url(dest_path, new_url):
                        print_success(f"Updated remote URL to {new_url}")
                    else:
                        print_warning("Could not update remote URL automatically")

                if self.on_transfer:
                    self.on_transfer(src_org, dest_org, repo)
            else:
                print_warning(
                    f"Transfer may still be in progress. "
                    f"Remote URL not updated - do this manually if needed."
                )


class RepoWatcher:
    """Watches for repository moves between organization folders."""

    def __init__(self, config: Config, on_transfer: Optional[Callable] = None):
        self.config = config
        self.on_transfer = on_transfer
        self.observer: Optional[Observer] = None
        self._running = False

    def start(self) -> None:
        """Start watching for repository moves."""
        if self._running:
            print_warning("Watcher is already running")
            return

        if not self.config.base_path.exists():
            print_error(f"Base path does not exist: {self.config.base_path}")
            return

        handler = OrgMoveHandler(self.config, self.on_transfer)
        self.observer = Observer()
        self.observer.schedule(handler, str(self.config.base_path), recursive=True)
        self.observer.start()
        self._running = True

        print_success(f"Watching for repo moves in: {self.config.base_path}")
        print_info("Move a repo folder between org directories to trigger a transfer")

    def stop(self) -> None:
        """Stop watching."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        self._running = False
        print_info("Watcher stopped")

    def run_forever(self) -> None:
        """Run the watcher until interrupted."""
        self.start()
        try:
            while self._running:
                time.sleep(1)
        except KeyboardInterrupt:
            print_info("\nReceived interrupt signal")
        finally:
            self.stop()

    @property
    def is_running(self) -> bool:
        """Check if watcher is currently running."""
        return self._running
