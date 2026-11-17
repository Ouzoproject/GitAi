from pathlib import Path
import re
import shutil
from git import Repo
from models import SourceFile


REPOS_DIR = Path("repos")

# Define allowed file extensions and ignored directories
ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".md",
}

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "venv",
    ".venv",
    "__pycache__",
    "docs_src"
}


# Only plain https://github.com/<owner>/<repo>[.git][/] URLs are accepted.
# GitHub owners: letters, digits, hyphens. Repos: letters, digits, ., _, -
_GITHUB_URL_RE = re.compile(
    r"^https://github\.com/"
    r"(?P<owner>[A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))/"
    r"(?P<repo>[A-Za-z0-9._-]{1,100}?)"
    r"(?:\.git)?/?$"
)


class InvalidRepoURL(ValueError):
    """Raised when the given URL is not a valid public GitHub repository URL."""


def parse_github_url(url: str) -> tuple[str, str]:
    """
    Validate a GitHub repository URL and return (owner, repo).

    Rejects anything that is not https://github.com/<owner>/<repo>, which
    blocks other hosts, file:// and ssh URLs, git option injection
    (e.g. "--upload-pack=..."), and path traversal.
    """
    match = _GITHUB_URL_RE.match(url.strip())

    if match is None:
        raise InvalidRepoURL(
            "Invalid repository URL. Use the format "
            "https://github.com/owner/repository"
        )

    owner, repo = match.group("owner"), match.group("repo")

    if repo in {".", ".."}:
        raise InvalidRepoURL("Invalid repository name.")

    return owner, repo


def parse_repo_id(repo_id: str) -> tuple[str, str]:
    """
    Validate a repository id of the form "owner/repo" and return (owner, repo).
    """
    return parse_github_url(f"https://github.com/{repo_id}")


def clone_repo(url: str) -> Path:
    """
    Clone a public GitHub repository and return its local path.

    Raises InvalidRepoURL if the URL is not a GitHub repository URL.
    """

    owner, repo = parse_github_url(url)

    # owner__repo avoids collisions between same-named repos of different owners
    repo_path = REPOS_DIR / f"{owner}__{repo}"

    # Defense in depth: never delete/write outside REPOS_DIR
    if REPOS_DIR.resolve() not in repo_path.resolve().parents:
        raise InvalidRepoURL("Invalid repository name.")

    # Remove existing copy
    if repo_path.exists():
        shutil.rmtree(repo_path)

    REPOS_DIR.mkdir(exist_ok=True)

    # Rebuild the URL from the validated parts instead of using raw user input.
    # GIT_TERMINAL_PROMPT=0 makes private/nonexistent repos fail instead of
    # waiting for credentials; depth=1 skips the full git history.
    Repo.clone_from(
        f"https://github.com/{owner}/{repo}.git",
        repo_path,
        depth=1,
        env={"GIT_TERMINAL_PROMPT": "0"},
    )

    return repo_path

def load_files(repo_path: Path) -> list[SourceFile]:
    """
    Load files from the cloned repository, filtering by allowed extensions and ignoring specified directories.
    """
    files = []

    for file_path in repo_path.rglob("*"):
        # Skip directories
        if not file_path.is_file():
            continue
        # Skip ignored folders
        if any(part in IGNORED_DIRECTORIES for part in file_path.parts):
            continue
        # Skip unsupported extensions
        if file_path.suffix not in ALLOWED_EXTENSIONS:
            continue
        try:
            content = file_path.read_text(encoding="utf-8")

            files.append(SourceFile(
                path=str(file_path.relative_to(repo_path)),
                content=content
            ))

        except Exception as e:
            print(f"Could not read {file_path}: {e}")

    return files