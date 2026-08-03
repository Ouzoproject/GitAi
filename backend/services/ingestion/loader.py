from pathlib import Path
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


def clone_repo(url: str) -> Path:
    """
    Clone a GitHub repository and return its local path.
    """

    repo_name = url.split("/")[-1].replace(".git", "")

    repo_path = REPOS_DIR / repo_name

    # Remove existing copy
    if repo_path.exists():
        shutil.rmtree(repo_path)

    REPOS_DIR.mkdir(exist_ok=True)

    Repo.clone_from(url, repo_path)

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

    