"""Configuration management for github-org-mirror."""

import os
from pathlib import Path
from typing import List, Optional

import yaml

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "github-org-mirror"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"


class Config:
    """Configuration handler for github-org-mirror."""

    def __init__(
        self,
        base_path: str = "~/Projects/orgs",
        organizations: Optional[List[str]] = None,
        sync_interval: int = 300,
        exclude_repos: Optional[List[str]] = None,
        auto_update_remotes: bool = True,
        clone_protocol: str = "ssh",
    ):
        self.base_path = Path(base_path).expanduser().resolve()
        self.organizations = organizations or []
        self.sync_interval = sync_interval
        self.exclude_repos = exclude_repos or [".github"]
        self.auto_update_remotes = auto_update_remotes
        self.clone_protocol = clone_protocol  # 'ssh' or 'https'

    def to_dict(self) -> dict:
        """Convert config to dictionary for serialization."""
        return {
            "base_path": str(self.base_path),
            "organizations": self.organizations,
            "sync_interval": self.sync_interval,
            "exclude_repos": self.exclude_repos,
            "auto_update_remotes": self.auto_update_remotes,
            "clone_protocol": self.clone_protocol,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create Config from dictionary."""
        return cls(
            base_path=data.get("base_path", "~/Projects/orgs"),
            organizations=data.get("organizations", []),
            sync_interval=data.get("sync_interval", 300),
            exclude_repos=data.get("exclude_repos", [".github"]),
            auto_update_remotes=data.get("auto_update_remotes", True),
            clone_protocol=data.get("clone_protocol", "ssh"),
        )

    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to YAML file."""
        config_path = path or DEFAULT_CONFIG_FILE
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "Config":
        """Load configuration from YAML file."""
        config_path = path or DEFAULT_CONFIG_FILE
        if not config_path.exists():
            return cls()
        with open(config_path) as f:
            data = yaml.safe_load(f) or {}
        return cls.from_dict(data)

    def get_org_path(self, org: str) -> Path:
        """Get the local path for an organization."""
        return self.base_path / org

    def get_repo_path(self, org: str, repo: str) -> Path:
        """Get the local path for a repository."""
        return self.base_path / org / repo

    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        if not self.organizations:
            errors.append("No organizations configured")
        if self.sync_interval < 60:
            errors.append("Sync interval should be at least 60 seconds")
        if self.clone_protocol not in ("ssh", "https"):
            errors.append("Clone protocol must be 'ssh' or 'https'")
        return errors


def get_config(config_path: Optional[Path] = None) -> Config:
    """Load and return the configuration."""
    return Config.load(config_path)


def config_exists(path: Optional[Path] = None) -> bool:
    """Check if configuration file exists."""
    config_path = path or DEFAULT_CONFIG_FILE
    return config_path.exists()
