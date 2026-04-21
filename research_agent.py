"""
Research Agent - Deep Agents Framework
Skill-driven research agent using LangChain/LangGraph
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

# Add crawl4ai to path
CRAWL4AI_PATH = Path(__file__).parent.parent / "crawl4ai"
sys.path.insert(0, str(CRAWL4AI_PATH))

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain.tools import tool


# =====================
# 工具定义 (LangChain @tool)
# =====================

@tool
def twitter_bookmarks(limit: int = 10) -> str:
    """抓取当前用户的 Twitter 书签，返回 JSON 格式推文列表"""
    cmd = ["opencli", "twitter", "bookmarks", "-f", "json", "--limit", str(limit)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"


@tool
def twitter_profile(username: str, limit: int = 10) -> str:
    """抓取指定 Twitter 用户的最新推文"""
    cmd = ["opencli", "twitter", "profile", username, "-f", "json", "--limit", str(limit)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"


@tool
def crawl_webpage(url: str) -> str:
    """抓取任意网页返回 Markdown 内容"""
    try:
        from crawl4ai import AsyncWebCrawler
        async def _crawl():
            async with AsyncWebCrawler(verbose=False) as crawler:
                result = await crawler.arun(url=url)
                if result.success:
                    return result.markdown
                return f"Crawl failed: {result.error_message}"
        import asyncio
        return asyncio.run(_crawl())
    except Exception:
        try:
            resp = subprocess.run(["curl", "-s", f"https://r.jina.ai/{url}"],
                                  capture_output=True, text=True, timeout=30)
            return resp.stdout if resp.returncode == 0 else "Fallback failed"
        except Exception:
            return "Crawl error"


@tool
def run_opencli(command: str) -> str:
    """执行 opencli 命令并返回结果"""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            return result.stdout
        return f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception: {str(e)}"


@tool
def save_raw(data: str, filename: str) -> str:
    """保存 JSON 到 data/raw/ 目录"""
    raw_dir = Path(__file__).parent / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    path = raw_dir / f"{filename}.json"
    try:
        parsed = json.loads(data)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)
        return f"Saved to {path}"
    except json.JSONDecodeError:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        return f"Saved text to {path}"


@tool
def save_processed(content: str, filename: str) -> str:
    """保存处理后的报告到 data/processed/ 目录 (Markdown 格式)"""
    processed_dir = Path(__file__).parent / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    # 确保文件名有 .md 后缀
    if not filename.endswith(".md"):
        filename = filename + ".md"
    path = processed_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved to {path}"


@tool
def search_arxiv(query: str, max_results: int = 5, category: str = "") -> str:
    """搜索 arXiv 论文，返回标题、作者、摘要和链接"""
    import xml.etree.ElementTree as ET
    import urllib.parse
    import re

    if category:
        q = f"cat:{category}+AND+{query}"
    else:
        q = query

    url = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(q)}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

    try:
        resp = subprocess.run(["curl", "-s", "--max-time", "20", url], capture_output=True, text=True)
        if resp.returncode != 0:
            return f"Error: {resp.stderr}"

        root = ET.fromstring(resp.stdout)
        results = []
        for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title")
            title = title.text.strip().replace("\n", " ") if title is not None else ""
            summary = entry.find("{http://www.w3.org/2005/Atom}summary")
            summary = summary.text.strip() if summary is not None else ""
            summary = re.sub(r"\s+", " ", summary)[:400]
            paper_id = entry.find("{http://www.w3.org/2005/Atom}id")
            paper_id = paper_id.text.strip().split("/")[-1] if paper_id is not None else ""
            published = entry.find("{http://www.w3.org/2005/Atom}published")
            published = published.text[:10] if published is not None else ""
            link = f"https://arxiv.org/abs/{paper_id}"
            authors = [a.find("{http://www.w3.org/2005/Atom}name").text for a in entry.findall("{http://www.w3.org/2005/Atom}author") if a.find("{http://www.w3.org/2005/Atom}name") is not None]
            author_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")
            results.append(f"**{title}**\n  作者: {author_str} | 日期: {published}\n  摘要: {summary}...\n  链接: {link}")

        if not results:
            return "未找到相关论文"
        return "\n\n".join(results)
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def search_conference_papers(conference: str, year: int = 2025, query: str = "", max_results: int = 10) -> str:
    """搜索顶级会议论文（CVPR/ICCV/ECCV/ICLR/AAAI/NeurIPS/ICML/ACL/EMNLP/MICCAI），基于 DBLP API 无需认证"""
    import urllib.parse
    import urllib.request
    import xml.etree.ElementTree as ET

    VENUE_MAP = {
        "CVPR": "cvpr", "ICCV": "iccv", "ECCV": "eccv",
        "ICLR": "iclr", "AAAI": "aaai", "NeurIPS": "nips",
        "ICML": "icml", "ACL": "acl", "EMNLP": "emnlp",
        "MICCAI": "miccai",
    }

    venue_key = VENUE_MAP.get(conference.upper())
    if not venue_key:
        return f"不支持的会议: {conference}，支持的: {', '.join(VENUE_MAP.keys())}"

    q_param = f"toc:db/conf/{venue_key}/{venue_key}{year}.bht"
    if query:
        q_param = f"{q_param}+AND+{urllib.parse.quote(query)}"

    url = f"https://dblp.org/search/publ/api?q={q_param}&format=xml&h={max_results}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            xml_data = resp.read()

        root = ET.fromstring(xml_data)
        ns = {"dblp": "https://dblp.org/pid/xs/dblp.xsd"}
        results = []

        for hit in root.findall(".//dblp/hit"):
            info = hit.find("info", ns)
            if info is None:
                continue

            title = info.find("title", ns)
            title = title.text.strip() if title is not None else "N/A"
            year_el = info.find("year", ns)
            year_str = year_el.text if year_el is not None else str(year)

            authors = []
            for author in info.findall("authors/author", ns):
                if author.text:
                    authors.append(author.text)
            author_str = ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else "")

            url_el = info.find("url", ns)
            paper_url = url_el.text if url_el is not None else f"https://dblp.org/rec/conf/{venue_key}/{year_str}"

            results.append(f"**{title}**\n  作者: {author_str} | 年份: {year_str} | 会议: {conference}\n  链接: {paper_url}")

        if not results:
            return f"未找到 {conference} {year} 相关论文"
        return "\n\n".join(results)
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def fetch_newsletter(url: str) -> str:
    """抓取 Newsletter 最新文章列表（支持 Substack RSS），返回标题、摘要和链接"""
    import xml.etree.ElementTree as ET
    import html
    import re

    rss_urls = [
        url if url.endswith(".xml") else url.rstrip("/") + "/feed",
        url.rstrip("/") + "/feed.xml",
    ]

    for rss_url in rss_urls:
        try:
            resp = subprocess.run(
                ["curl", "-s", "--max-time", "15", rss_url],
                capture_output=True, text=True
            )
            if resp.returncode == 0 and resp.stdout.strip():
                root = ET.fromstring(resp.stdout)
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                articles = []
                for entry in root.iter("entry")[:10]:
                    title = "".join(entry.itertext("title")) or ""
                    link = (entry.find("link", ns) or entry.find("link")) or ""
                    link = link.get("href", link.text) if hasattr(link, "get") else str(link)
                    summary = "".join(entry.itertext("summary")) or "".join(entry.itertext("content")) or ""
                    published = "".join(entry.itertext("published")) or ""
                    title = html.unescape(title)
                    summary = re.sub(r"<[^>]+>", "", html.unescape(summary))[:300]
                    articles.append(f"- **{title}** ({published})\n  {summary}\n  链接: {link}")
                if articles:
                    return "\n\n".join(articles)
        except Exception:
            pass

    return crawl_webpage_with_curl(url)


def crawl_webpage_with_curl(url: str) -> str:
    """Fallback crawl using jina.ai proxy"""
    try:
        resp = subprocess.run(["curl", "-s", f"https://r.jina.ai/{url}"],
                              capture_output=True, text=True, timeout=30)
        return resp.stdout if resp.returncode == 0 else "Curl fallback failed"
    except Exception:
        return "Crawl error"


@tool
def fetch_rss(url: str, max_items: int = 10) -> str:
    """解析任意 RSS/Atom 订阅源，返回标题、链接、描述和发布时间。支持 Blog、YouTube、Podcast、Twitter/X 等各类 RSS。

    适用场景：
    - Blog/Newsletter RSS (如 https://blog.langchain.dev/feed)
    - YouTube 频道 RSS (如 https://youtube.com/feeds/videos.xml?channel_id=xxx)
    - Podcast RSS (如 https://rsshub.example.com/podcast/xxx)
    - Twitter/X RSS (如 https://api.xgo.ing/rss/user/xxx)

    注意：部分 Blog 的 RSS URL 可能需要加 /feed 后缀，或使用 RSSHub 代理
    """
    import xml.etree.ElementTree as ET
    import html
    import re

    try:
        resp = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "20",
             "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
             url],
            capture_output=True,
            text=True
        )
        if resp.returncode != 0:
            return f"Error fetching RSS: {resp.stderr}"

        xml_content = resp.stdout
        if not xml_content.strip():
            return "Empty response from RSS feed"

        # 尝试解析 XML
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            return f"XML parse error: {str(e)}\n\nRaw content (first 500 chars):\n{xml_content[:500]}"

        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "media": "http://search.yahoo.com/mrss/",
            "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        }

        channel = root.find("channel")
        if channel is None:
            # 可能是 Atom feed
            feed_title = root.find("title")
            feed_title = feed_title.text if feed_title is not None else "Unknown Feed"
            entries = root.findall(".//atom:entry", ns) or root.findall("entry")
        else:
            feed_title = channel.find("title")
            feed_title = feed_title.text if feed_title is not None else "Unknown Feed"
            entries = channel.findall("item") or channel.findall("entry")

        results = [f"# {html.unescape(feed_title)}\n"]

        for i, entry in enumerate(entries[:max_items]):
            if i >= max_items:
                break

            # 获取标题
            title = entry.find("title")
            title = html.unescape(title.text.strip()) if title is not None and title.text else "No Title"

            # 获取链接
            link = entry.find("link")
            if link is not None:
                if link.get("href"):
                    link_text = link.get("href")
                elif link.text:
                    link_text = link.text.strip()
                else:
                    link_text = ""
            else:
                link_text = ""

            # 获取描述/摘要
            desc = entry.find("description") or entry.find("summary") or entry.find("content:encoded")
            if desc is None:
                # 尝试 itunes 摘要
                desc = entry.find("{http://www.itunes.com/dtds/podcast-1.0.dtd}summary")
            desc_text = ""
            if desc is not None and desc.text:
                desc_text = re.sub(r"<[^>]+>", "", html.unescape(desc.text))
                desc_text = desc_text[:300] + "..." if len(desc_text) > 300 else desc_text

            # 获取发布时间
            pub_date = entry.find("pubDate") or entry.find("published") or entry.find("updated")
            pub_text = ""
            if pub_date is not None and pub_date.text:
                pub_text = pub_date.text.strip()[:16]  # 简化日期

            # YouTube 特殊处理
            yt_video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId")
            if yt_video_id is not None:
                video_id = yt_video_id.text
                link_text = f"https://www.youtube.com/watch?v={video_id}"
                # YouTube 标题可能在 media:group/media:title
                yt_title = entry.find("{http://search.yahoo.com/mrss/}group/{http://search.yahoo.com/mrss/}title")
                if yt_title is not None and yt_title.text:
                    title = html.unescape(yt_title.text.strip())
                thumb = entry.find("{http://search.yahoo.com/mrss/}thumbnail")
                thumb_url = thumb.get("url") if thumb is not None else f"https://i1.ytimg.com/vi/{video_id}/hqdefault.jpg"
                results.append(f"## [{title}]({link_text})\n📅 {pub_text} | 🎥 YouTube\n![Thumbnail]({thumb_url})\n")
            elif link_text:
                results.append(f"## [{title}]({link_text})\n📅 {pub_text}\n{desc_text}\n")
            else:
                results.append(f"## {title}\n📅 {pub_text}\n{desc_text}\n")

        if len(results) == 1:
            return "No items found in RSS feed"

        return "\n\n".join(results)

    except Exception as e:
        return f"RSS fetch error: {str(e)}"


# =====================
# Skill 目录
# =====================

SKILLS_DIR = Path(__file__).parent / "skills"
SKILLS_DIR.mkdir(exist_ok=True)


# =====================
# 创建 Deep Agent
# =====================

def create_research_agent():
    """创建科研情报 Agent"""

    tools = [
        run_opencli,
        save_raw,
        save_processed,
        twitter_bookmarks,
        twitter_profile,
        crawl_webpage,
        search_arxiv,
        search_conference_papers,
        fetch_newsletter,
        fetch_rss,
    ]

    backend = FilesystemBackend(
        root_dir=str(Path(__file__).parent),
        virtual_mode=True
    )

    # MiniMax 使用 OpenAI 兼容接口
    llm = ChatOpenAI(
        model=os.environ.get("MINIMAX_MODEL", "MiniMax-M2.7"),
        openai_api_key=os.environ.get("MINIMAX_API_KEY", ""),
        openai_api_base=os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1"),
    )

    agent = create_deep_agent(
        name="research-agent",
        model=llm,
        tools=tools,
        skills=[str(SKILLS_DIR)],
        system_prompt="""你是一个顶级 AI 科研情报助手，代号 Deep Research Agent。

你的职责是从 Twitter、网络、arXiv 和会议论文中收集科研情报，并进行结构化分析。

核心能力：
- run_opencli: 执行 opencli 命令（如 opencli twitter bookmarks -f json）
- save_raw: 保存 JSON 原始数据到 data/raw/
- save_processed: 保存 Markdown 报告到 data/processed/
- twitter_bookmarks: 抓取 Twitter 书签
- twitter_profile: 追踪特定用户的最新动态
- crawl_webpage: 深入抓取高价值网页内容
- search_arxiv: 搜索最新学术论文
- search_conference_papers: 搜索顶级会议论文 (CVPR/ICLR/NeurIPS等)
- fetch_newsletter: 抓取 Newsletter 最新内容

数据保存规范：
- 原始数据 → save_raw → data/raw/*.json
- 分析报告 → save_processed → data/processed/*.md

Skill 知识：
- skills/opencli/SKILL.md: opencli 通用技能
- skills/opencli-twitter/SKILL.md: Twitter 专用技能

工作流程：
1. 分析用户需求，确定需要哪些数据源
2. 按优先级调用工具获取信息
3. 综合所有信息生成结构化报告

输出格式：最终报告使用中文，包含：
- 核心发现
- 详细分析
- 关键链接
- 技术趋势判断""",
        backend=backend,
        checkpointer=MemorySaver(),
    )

    return agent


# =====================
# 运行入口
# =====================

def run_research(query: str, thread_id: str = "default"):
    """运行科研任务"""
    agent = create_research_agent()

    config = {"configurable": {"thread_id": thread_id}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Deep Research Agent")
    parser.add_argument("--query", "-q", default="分析我的 Twitter 书签，找出 AI 领域的技术趋势")
    parser.add_argument("--thread", "-t", default="default", help="会话线程 ID")
    args = parser.parse_args()

    print(f"[*] Deep Research Agent")
    print(f"[*] Query: {args.query}")
    print(f"[*] Thread: {args.thread}")
    print("=" * 60)

    result = run_research(args.query, args.thread)

    print("\n[*] Result:")
    print("=" * 60)
    for msg in result.get("messages", []):
        if hasattr(msg, "content") and msg.content:
            print(msg.content)

    # 保存结果
    raw_dir = Path(__file__).parent / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    output_path = raw_dir / f"research_result_{args.thread}.json"

    messages_for_save = [
        {"role": m.type, "content": m.content}
        for m in result.get("messages", [])
        if hasattr(m, "content") and m.content
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "query": args.query,
            "thread": args.thread,
            "messages": messages_for_save
        }, f, ensure_ascii=False, indent=2)

    print(f"\n[*] Saved to {output_path}")