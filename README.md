# GitHub Org Mirror

Two-way sync between local folders and GitHub organizations. Move repos locally between org folders, and they automatically transfer on GitHub. Changes on GitHub sync back to your local structure.

## Features

- **Local to GitHub**: Move a repo folder between org directories locally, and it automatically transfers on GitHub
- **GitHub to Local**: Sync repos from GitHub to the correct local org folders
- **File Watcher**: Daemon that monitors for folder moves and triggers transfers in real-time
- **Multi-org Support**: Manage repos across multiple GitHub organizations
- **Cross-platform**: Works on Linux, macOS, and Windows

## Prerequisites

- Python 3.8+
- [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated
- Owner/admin access to the organizations you want to manage

## Installation

```bash
# Clone the repository
git clone https://github.com/Sovereign-Operating-System/github-org-mirror.git
cd github-org-mirror

# Install the package
pip install -e .
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/Sovereign-Operating-System/github-org-mirror.git
```

## Quick Start

### 1. Initialize your local structure

```bash
# Initialize with your organizations
github-org-mirror init \
  --base-path ~/Projects/orgs \
  --org MyOrg1 \
  --org MyOrg2 \
  --org MyOrg3
```

This will:
- Create `~/Projects/orgs/` with subdirectories for each org
- Clone all repos from each organization
- Save your configuration

### 2. Start the watcher

```bash
github-org-mirror watch
```

Now when you move a repo folder from one org directory to another, the tool will:
1. Detect the move
2. Transfer the repo on GitHub
3. Update the local git remote URL

### 3. Sync from GitHub

If repos were transferred on GitHub's web interface:

```bash
github-org-mirror sync
```

This moves local folders to match GitHub's current state.

## Commands

| Command | Description |
|---------|-------------|
| `github-org-mirror init` | Initialize folder structure and clone repos |
| `github-org-mirror watch` | Start daemon to watch for local moves |
| `github-org-mirror sync` | Sync GitHub state to local folders |
| `github-org-mirror status` | Show current sync status |
| `github-org-mirror config` | View or modify configuration |

## Configuration

Configuration is stored in `~/.config/github-org-mirror/config.yaml`:

```yaml
base_path: /home/user/Projects/orgs
organizations:
  - MyOrg1
  - MyOrg2
  - MyOrg3
sync_interval: 300
exclude_repos:
  - .github
auto_update_remotes: true
clone_protocol: ssh
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `base_path` | Root directory for org folders | `~/Projects/orgs` |
| `organizations` | List of GitHub organizations | `[]` |
| `sync_interval` | Seconds between GitHub polls | `300` |
| `exclude_repos` | Repos to ignore | `[".github"]` |
| `auto_update_remotes` | Update git remotes after transfer | `true` |
| `clone_protocol` | `ssh` or `https` | `ssh` |

### Managing Organizations

```bash
# Add an organization
github-org-mirror config --add-org NewOrg

# Remove an organization
github-org-mirror config --remove-org OldOrg

# View current config
github-org-mirror config --show
```

## How It Works

### Local to GitHub Sync

1. The watcher monitors your base directory for folder moves
2. When a repo folder moves between org directories, it detects the change
3. It verifies the folder is a git repo and extracts the current owner
4. Calls GitHub's transfer API via `gh api`
5. Waits for the transfer to complete
6. Updates the local git remote URL

### GitHub to Local Sync

1. Queries each org for its current repos via `gh repo list`
2. Compares with local folder structure
3. Moves misplaced local folders to correct org directories
4. Clones any repos missing locally
5. Reports orphaned repos (local but not on GitHub)

## Limitations

- **Transfer Cooldown**: GitHub has a ~24 hour cooldown between transfers of the same repo
- **Admin Required**: You must have admin/owner access to transfer repos
- **Archived Repos**: Archived repos cannot be transferred
- **Same-name Repos**: If two orgs have repos with the same name, behavior may be unexpected

## Development

```bash
# Clone and install in development mode
git clone https://github.com/Sovereign-Operating-System/github-org-mirror.git
cd github-org-mirror
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black github_org_mirror
ruff check github_org_mirror
```

## License

MIT License - see [LICENSE](LICENSE) for details.
