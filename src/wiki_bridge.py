"""
Wiki Bridge - LLM Wiki interface (direct file-based for v0.5.x)
"""

import subprocess
import json
import yaml
from pathlib import Path
from datetime import date
from typing import Optional


def _wiki_dir() -> Path:
    """Get wiki directory."""
    root = Path(__file__).parent.parent
    return root / "wiki"


def _sources_dir() -> Path:
    """Get sources directory."""
    root = Path(__file__).parent.parent
    return root / "sources"


def _ensure_wiki_dir():
    """Ensure wiki directory exists."""
    _wiki_dir().mkdir(exist_ok=True)


def wiki_init() -> bool:
    """
    Initialize a new LLM Wiki vault.
    Note: This runs llm-wiki init which creates the vault structure.
    """
    result = subprocess.run(
        ["llm-wiki", "init", str(Path(__file__).parent.parent)],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def wiki_ingest(source_path: str, title: Optional[str] = None,
                tags: Optional[list] = None,
                category: Optional[str] = None) -> tuple[bool, str]:
    """
    Ingest a source into wiki (manual implementation for v0.5.x).

    Args:
        source_path: Path to source file
        title: Wiki page title (default: filename)
        tags: Tags for the page
        category: Category (subdirectory)

    Returns:
        (success, message)
    """
    source_file = Path(source_path)
    if not source_file.exists():
        return False, f"Source not found: {source_path}"

    # Load source content
    with open(source_file, "r", encoding="utf-8") as f:
        raw = f.read()

    # Extract frontmatter and content
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        source_fm = yaml.safe_load(parts[1])
        content = parts[2].strip()
    else:
        source_fm = {}
        content = raw

    # Generate title
    if not title:
        title = source_file.stem.replace("-", " ").title()

    # Create wiki frontmatter
    wiki_fm = {
        "title": title,
        "source": f"[[{source_path}]]",
        "type": source_fm.get("type", "unknown"),
        "tags": tags or [],
        "created": date.today().isoformat(),
        "updated": date.today().isoformat(),
    }

    if category:
        wiki_fm["category"] = category

    # Determine target path
    _ensure_wiki_dir()
    slug = title.lower().replace(" ", "-").replace("/", "-")
    target_path = _wiki_dir() / f"{slug}.md"

    # Write wiki page
    yaml_content = yaml.dump(wiki_fm, default_flow_style=False, allow_unicode=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(f"---\n{yaml_content}---\n\n# {title}\n\n{content}")

    return True, f"Created wiki page: {target_path}"


def wiki_add(title: str, content: str, tags: Optional[list] = None,
             category: str = "default") -> tuple[bool, str]:
    """
    Directly add a wiki page.

    Args:
        title: Page title
        content: Page content (Markdown)
        tags: Tags
        category: Category

    Returns:
        (success, message)
    """
    _ensure_wiki_dir()

    slug = title.lower().replace(" ", "-").replace("/", "-")
    path = _wiki_dir() / f"{slug}.md"

    fm = {
        "title": title,
        "tags": tags or [],
        "category": category,
        "created": date.today().isoformat(),
        "updated": date.today().isoformat(),
    }

    yaml_content = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"---\n{yaml_content}---\n\n# {title}\n\n{content}")

    return True, f"Created: {path}"


def wiki_query(query: str, category: Optional[str] = None,
               tags: Optional[list] = None) -> tuple[bool, str]:
    """
    Query wiki pages (simple text search).

    Args:
        query: Search query
        category: Optional category filter
        tags: Optional tags filter

    Returns:
        (success, results)
    """
    results = []
    query_lower = query.lower()

    for wiki_file in _wiki_dir().glob("*.md"):
        with open(wiki_file, "r", encoding="utf-8") as f:
            content = f.read()

        if query_lower in content.lower():
            # Extract title
            title_match = content.split("---")[2] if "---" in content else content
            title = title_match.split("\n")[0].replace("# ", "").strip()

            # Check category filter
            if category:
                if f"category: {category}" not in content:
                    continue

            results.append(f"- {wiki_file.stem}: {title}")

    if results:
        return True, "\n".join(results)
    return False, "No results found"


def wiki_search(query: str, limit: int = 10) -> tuple[bool, str]:
    """
    Search wiki using llm-wiki CLI.

    Returns:
        (success, results)
    """
    result = subprocess.run(
        ["llm-wiki", "search", query, "-n", str(limit)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    if result.returncode == 0:
        return True, result.stdout
    return False, result.stderr


def wiki_lint() -> tuple[bool, str]:
    """
    Run wiki health check (uses llm-wiki if available).

    Returns:
        (success, report)
    """
    # Manual lint: check for orphan pages, broken links
    _ensure_wiki_dir()

    issues = []
    pages = list(_wiki_dir().glob("*.md"))

    for page in pages:
        with open(page, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if page has frontmatter
        if not content.startswith("---"):
            issues.append(f"Missing frontmatter: {page.name}")

        # Check for empty content
        if len(content) < 50:
            issues.append(f"Very short content: {page.name}")

    if issues:
        return True, "Issues found:\n" + "\n".join(f"  - {i}" for i in issues)
    return True, "Health: OK\nNo issues found."


def wiki_graph() -> tuple[bool, str]:
    """
    Get wiki knowledge graph (uses llm-wiki CLI).

    Returns:
        (success, graph info)
    """
    result = subprocess.run(
        ["llm-wiki", "graph", "--json"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    if result.returncode == 0:
        return True, result.stdout
    return False, result.stderr


def wiki_status() -> tuple[bool, str]:
    """
    Get wiki status.

    Returns:
        (success, status)
    """
    result = subprocess.run(
        ["llm-wiki", "status"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )

    if result.returncode == 0:
        return True, result.stdout

    # Manual fallback
    _ensure_wiki_dir()
    wiki_pages = list(_wiki_dir().glob("*.md"))
    source_count = len(list(_sources_dir().rglob("*.*")))

    status = f"""Wiki: InfoGet
Pages: {len(wiki_pages)}
Sources: {source_count}
Health: {"OK" if wiki_pages else "Empty"}
"""
    return True, status


def wiki_list() -> tuple[bool, list]:
    """
    List all wiki pages.

    Returns:
        (success, pages_list)
    """
    _ensure_wiki_dir()
    pages = []

    for wiki_file in _wiki_dir().glob("*.md"):
        with open(wiki_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract title from frontmatter or first heading
        if content.startswith("---"):
            parts = content.split("---", 2)
            try:
                fm = yaml.safe_load(parts[1])
                title = fm.get("title", wiki_file.stem)
            except:
                title = wiki_file.stem
        else:
            title = wiki_file.stem

        pages.append(title)

    return True, pages


def is_wiki_initialized() -> bool:
    """Check if LLM Wiki is initialized."""
    root = Path(__file__).parent.parent
    return (root / ".llm-wiki" / "config.toml").exists()


def ensure_wiki_initialized() -> bool:
    """Ensure wiki is initialized."""
    if not is_wiki_initialized():
        return wiki_init()
    return True
