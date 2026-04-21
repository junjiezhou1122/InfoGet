"""
Crawler - 爬取后保存到 sources 的工具

注意：实际爬取由 Agent 直接调用 CLI（browser-harness, curl, opencli 等）
此模块仅处理爬取后的保存逻辑（带 frontmatter）。
"""

from datetime import date
from pathlib import Path
from typing import Optional

from .source_manager import save_source, get_source_type


def crawl_and_save(url: str, content: str, filename: Optional[str] = None,
                   format: str = "md", extra_frontmatter: Optional[dict] = None) -> tuple[bool, str, str]:
    """
    将已爬取的内容保存到 sources/。

    Agent 直接调 CLI 爬取，爬完后调此函数保存。
    """
    source_type = get_source_type(url)
    fm_yaml, saved_path = save_source(
        content=content,
        url=url,
        filename=filename,
        source_type=source_type,
        format=format,
        extra_frontmatter=extra_frontmatter
    )
    return True, content, saved_path


def crawl_twitter_and_save(command: str, content: str, tag: str = "bookmarks") -> tuple[bool, str, str]:
    """
    将已爬取的 Twitter 内容保存到 sources/。
    """
    if "bookmarks" in command:
        url = "https://twitter.com/bookmarks"
    elif "profile" in command:
        parts = command.split()
        username = parts[1].lstrip("@") if len(parts) >= 2 else "unknown"
        url = f"https://twitter.com/{username}"
    else:
        url = "https://twitter.com/unknown"

    fm_yaml, saved_path = save_source(
        content=content,
        url=url,
        filename=f"twitter-{tag}-{date.today().isoformat()}.json",
        source_type="social",
        format="json",
        extra_frontmatter={"tag": tag, "command": command}
    )
    return True, content, saved_path
