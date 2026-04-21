"""
Crawler - Crawler integration for various sources
"""

import subprocess
import json
from pathlib import Path
from typing import Optional
from datetime import date

# Import source_manager
from .source_manager import save_source, get_source_type


def crawl_url_browser_harness(url: str) -> tuple[bool, str]:
    """
    Crawl a URL using browser-harness.

    Returns:
        (success, markdown_content)
    """
    try:
        result = subprocess.run(
            ["uv", "run", "browser-harness"],
            input=f'''
import asyncio
from crawl4ai import AsyncWebCrawler

async def crawl():
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url="{url}")
        if result.success:
            return result.markdown
        return f"Error: {{result.error_message}}"

print(asyncio.run(crawl()))
''',
            capture_output=True,
            text=True,
            timeout=120,
            cwd=Path(__file__).parent.parent
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def crawl_url_jina(url: str) -> tuple[bool, str]:
    """
    Crawl a URL using Jina AI reader API (fallback).

    Returns:
        (success, markdown_content)
    """
    try:
        jina_url = f"https://r.jina.ai/{url}"
        result = subprocess.run(
            ["curl", "-s", "-L", jina_url, "-H", "Accept: text/markdown"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0 and result.stdout:
            return True, result.stdout
        else:
            return False, "Empty response or error"
    except Exception as e:
        return False, str(e)


def crawl_arxiv_paper(arxiv_id: str) -> tuple[bool, str]:
    """
    Crawl arXiv paper metadata via API.

    Args:
        arxiv_id: e.g., "1706.03762"

    Returns:
        (success, xml_content)
    """
    try:
        url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def crawl_twitter_opencli(command: str) -> tuple[bool, str]:
    """
    Crawl Twitter using opencli.

    Args:
        command: e.g., "bookmarks --limit 10" or "profile username --limit 10"

    Returns:
        (success, json_content)
    """
    try:
        parts = command.split()
        cmd = ["opencli", "twitter"] + parts
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def crawl_url_auto(url: str, prefer: str = "browser") -> tuple[bool, str]:
    """
    Auto-detect best crawl method for URL.

    Args:
        url: URL to crawl
        prefer: "browser", "jina", or "auto"

    Returns:
        (success, content)
    """
    # If arXiv, use API directly
    if "arxiv.org" in url:
        # Extract arXiv ID
        parts = url.split("/")
        if parts[-1]:
            arxiv_id = parts[-1].replace(".abs", "").replace(".pdf", "")
        else:
            arxiv_id = parts[-2]
        return crawl_arxiv_paper(arxiv_id)

    # Try browser-harness first
    if prefer in ["browser", "auto"]:
        success, content = crawl_url_browser_harness(url)
        if success and content and "Error" not in content[:50]:
            return success, content

    # Fallback to Jina
    return crawl_url_jina(url)


def crawl_and_save(url: str, filename: Optional[str] = None,
                   format: str = "md", extra_frontmatter: Optional[dict] = None) -> tuple[bool, str, str]:
    """
    Crawl URL and save to sources/.

    Args:
        url: Source URL
        filename: Optional filename
        format: File format (md, json, xml)
        extra_frontmatter: Additional frontmatter fields

    Returns:
        (success, content, saved_path)
    """
    # Determine source type
    source_type = get_source_type(url)

    # Special handling for arXiv
    if "arxiv.org" in url:
        success, content = crawl_arxiv_paper(url.split("/")[-1])
        format = "xml"
    else:
        success, content = crawl_url_auto(url)

    if not success:
        return False, content, ""

    # Save to sources
    fm_yaml, saved_path = save_source(
        content=content,
        url=url,
        filename=filename,
        source_type=source_type,
        format=format,
        extra_frontmatter=extra_frontmatter
    )

    return True, content, saved_path


def crawl_twitter_and_save(command: str, tag: str = "bookmarks") -> tuple[bool, str, str]:
    """
    Crawl Twitter and save to sources/.

    Args:
        command: opencli twitter command, e.g., "bookmarks --limit 10"
        tag: Tag for the source, e.g., "bookmarks", "profile-username"

    Returns:
        (success, content, saved_path)
    """
    success, content = crawl_twitter_opencli(command)

    if not success:
        return False, content, ""

    # Generate URL from command
    if "bookmarks" in command:
        url = "https://twitter.com/bookmarks"
    elif "profile" in command:
        # Extract username from command
        parts = command.split()
        if len(parts) >= 2:
            username = parts[1].lstrip("@")
            url = f"https://twitter.com/{username}"
        else:
            url = "https://twitter.com/unknown"
    else:
        url = "https://twitter.com/unknown"

    # Save to sources
    fm_yaml, saved_path = save_source(
        content=content,
        url=url,
        filename=f"twitter-{tag}-{date.today().isoformat()}.json",
        source_type="social",
        format="json",
        extra_frontmatter={"tag": tag, "command": command}
    )

    return True, content, saved_path
