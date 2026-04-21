"""
Source Manager - Sources storage logic with frontmatter
"""

import json
import yaml
from pathlib import Path
from datetime import date
from urllib.parse import urlparse
from typing import Optional

# Source types
SOURCE_TYPES = ["paper", "blog", "social", "code"]


def extract_hostname(url: str) -> str:
    """Extract hostname from URL."""
    parsed = urlparse(url)
    hostname = parsed.netloc or parsed.path
    # Remove leading www.
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname


def get_source_type(url: str) -> str:
    """Guess source type from URL."""
    hostname = extract_hostname(url).lower()

    # Paper sources
    if any(x in hostname for x in ["arxiv", "openreview", "pubmed", " semanticscholar"]):
        return "paper"

    # Blog sources
    if any(x in hostname for x in ["medium", "blogspot", "wordpress", "substack", "neelnanda"]):
        return "blog"

    # Social sources
    if any(x in hostname for x in ["twitter", "x.com", "reddit", "mastodon"]):
        return "social"

    # Code sources
    if any(x in hostname for x in ["github", "gitlab", "bitbucket"]):
        return "code"

    # Default to blog for unknown
    return "blog"


def get_source_path(url: str, source_type: Optional[str] = None, crawled_date: Optional[str] = None) -> Path:
    """
    Generate sources/ path: type/hostname/YYYY-MM-DD/

    Example: sources/paper/arxiv.org/2024-04-21/
    """
    if source_type is None:
        source_type = get_source_type(url)

    if crawled_date is None:
        crawled_date = date.today().isoformat()

    hostname = extract_hostname(url)

    return Path(f"sources/{source_type}/{hostname}/{crawled_date}")


def create_frontmatter(url: str, source_type: Optional[str] = None, extra: Optional[dict] = None) -> dict:
    """Create frontmatter metadata for a source."""
    if source_type is None:
        source_type = get_source_type(url)

    fm = {
        "source": url,
        "type": source_type,
        "hostname": extract_hostname(url),
        "crawled": date.today().isoformat(),
    }

    if extra:
        fm.update(extra)

    return fm


def save_source(content: str, url: str, filename: Optional[str] = None,
                source_type: Optional[str] = None, format: str = "md",
                extra_frontmatter: Optional[dict] = None) -> tuple[str, Path]:
    """
    Save content to sources/ directory with frontmatter.

    Args:
        content: The content to save
        url: Source URL
        filename: Optional filename (default: extracted from URL)
        source_type: Source type (auto-detected if None)
        format: File format (md, json, xml, txt)
        extra_frontmatter: Additional frontmatter fields

    Returns:
        (frontmatter_yaml, full_path)
    """
    source_type = source_type or get_source_type(url)
    path = get_source_path(url, source_type)
    path.mkdir(parents=True, exist_ok=True)

    # Generate filename from URL if not provided
    if filename is None:
        parsed = urlparse(url)
        # Use path component or hostname
        path_part = parsed.path.strip("/").replace("/", "-")
        if path_part:
            # Limit length
            path_part = path_part[:100]
            filename = f"{path_part}.{format}"
        else:
            filename = f"{extract_hostname(url)}.{format}"

    full_path = path / filename

    # Create frontmatter
    fm = create_frontmatter(url, source_type, extra_frontmatter)

    # Write file with frontmatter
    if format == "md":
        yaml_content = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"---\n{yaml_content}---\n\n{content}")
    else:
        # Non-markdown: save as separate files
        # Save frontmatter as .meta.yaml
        meta_path = full_path.with_suffix(f".{format}.meta.yaml")
        with open(meta_path, "w", encoding="utf-8") as f:
            yaml.dump(fm, f, default_flow_style=False, allow_unicode=True)
        # Save content
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

    return yaml.dump(fm), full_path


def load_source(source_path: Path) -> tuple[dict, str]:
    """
    Load source file and return (frontmatter, content).
    """
    if source_path.suffix == ".md":
        with open(source_path, "r", encoding="utf-8") as f:
            raw = f.read()

        if raw.startswith("---"):
            parts = raw.split("---", 2)
            fm = yaml.safe_load(parts[1])
            content = parts[2].strip()
        else:
            fm = {}
            content = raw
    else:
        # Non-markdown: load content and meta
        meta_path = source_path.with_suffix(".meta.yaml")
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                fm = yaml.safe_load(f)
        else:
            fm = {}
        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()

    return fm, content


def list_sources(source_type: Optional[str] = None, hostname: Optional[str] = None) -> list[dict]:
    """
    List all sources, optionally filtered by type and/or hostname.

    Returns:
        List of dicts with: path, url, type, crawled, hostname
    """
    sources_dir = Path("sources")
    if not sources_dir.exists():
        return []

    results = []

    # Determine search path
    if source_type:
        search_paths = [sources_dir / source_type]
    else:
        search_paths = [sources_dir / st for st in SOURCE_TYPES if (sources_dir / st).exists()]

    for sp in search_paths:
        if not sp.exists():
            continue

        for date_dir in sp.iterdir():
            if not date_dir.is_dir():
                continue
            if hostname and date_dir.name != hostname:
                continue

            for file in date_dir.iterdir():
                if file.is_file():
                    # Try to load frontmatter
                    fm_path = file.with_suffix(".meta.yaml") if file.suffix != ".md" else None
                    if fm_path and fm_path.exists():
                        with open(fm_path, "r", encoding="utf-8") as f:
                            fm = yaml.safe_load(f)
                    elif file.suffix == ".md":
                        with open(file, "r", encoding="utf-8") as f:
                            raw = f.read()
                        if raw.startswith("---"):
                            parts = raw.split("---", 2)
                            fm = yaml.safe_load(parts[1])
                        else:
                            fm = {}
                    else:
                        fm = {}

                    results.append({
                        "path": str(file),
                        "source": fm.get("source", ""),
                        "type": fm.get("type", ""),
                        "hostname": fm.get("hostname", ""),
                        "crawled": fm.get("crawled", ""),
                    })

    return results
