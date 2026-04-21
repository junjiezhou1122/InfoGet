"""
Research Agent - InfoGet Knowledge Management
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

# Import InfoGet modules
from src import (
    save_source,
    load_source,
    list_sources,
    crawl_and_save,
    crawl_twitter_and_save,
    wiki_ingest,
    wiki_query,
    wiki_search,
    wiki_add,
    wiki_list,
    wiki_status,
    wiki_lint,
    is_wiki_initialized,
    ensure_wiki_initialized,
    get_all_skills_summary,
    load_skill,
)


# =====================
# InfoGet Tools (LangChain @tool)
# =====================

@tool
def crawl_webpage(url: str) -> str:
    """抓取任意网页 — 实际由 Agent 直接调 CLI（browser-harness / curl jina）

    示例：
    - browser-harness 渲染 JS: uv run browser-harness ...
    - Jina 纯文本: curl -s https://r.jina.ai/{url}
    """
    return "请直接用 CLI 命令爬取：browser-harness 或 curl https://r.jina.ai/{url}"


@tool
def save_to_sources(url: str, content: str, source_type: str = "", extra: dict = None) -> str:
    """
    保存内容到 sources/ 目录（带 frontmatter）

    Args:
        url: 源 URL
        content: 要保存的内容
        source_type: 类型（paper/blog/social/code，自动检测可省略）
        extra: 额外的 frontmatter 字段
    """
    fm_yaml, path = save_source(
        content=content,
        url=url,
        source_type=source_type or None,
        extra_frontmatter=extra
    )
    return f"Saved to {path}\n\nFrontmatter:\n{fm_yaml}"


@tool
def ingest_to_wiki(source_path: str, title: str, tags: List[str] = None,
                   category: str = "") -> str:
    """
    把 source ingest 到 wiki（AI 处理原材料）

    Args:
        source_path: sources/ 下的文件路径
        title: wiki 页面标题
        tags: 标签列表
        category: 分类
    """
    success, msg = wiki_ingest(
        source_path=source_path,
        title=title,
        tags=tags,
        category=category
    )
    return msg if success else f"Failed: {msg}"


@tool
def query_wiki(query: str, category: str = "") -> str:
    """
    查询 wiki 知识库

    Args:
        query: 搜索查询
        category: 可选的分类过滤
    """
    success, result = wiki_query(query, category=category or None)
    return result if success else f"Query failed: {result}"


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
def twitter_bookmarks(limit: int = 10) -> str:
    """Twitter 书签 — Agent 直接调 CLI: opencli twitter bookmarks --limit N"""
    return "请直接调 CLI: opencli twitter bookmarks --limit " + str(limit)


@tool
def twitter_profile(username: str, limit: int = 10) -> str:
    """Twitter 用户推文 — Agent 直接调 CLI: opencli twitter profile @username"""
    return "请直接调 CLI: opencli twitter profile " + username


@tool
def save_processed(content: str, filename: str) -> str:
    """保存处理后的报告到 processed/ 目录"""
    processed_dir = Path(__file__).parent / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    if not filename.endswith(".md"):
        filename = filename + ".md"
    path = processed_dir / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved to {path}"


@tool
def wiki_status() -> str:
    """查看 wiki 状态"""
    success, status = wiki_status()
    return status


@tool
def wiki_health_check() -> str:
    """Wiki 健康检查"""
    success, report = wiki_lint()
    return report


@tool
def list_all_sources(source_type: str = "") -> str:
    """
    列出所有 sources

    Args:
        source_type: 可选的类型过滤（paper/blog/social/code）
    """
    sources = list_sources(source_type=source_type or None)
    if not sources:
        return "No sources found"
    lines = [f"- {s['type']}: {s['source']} (crawled: {s['crawled']})" for s in sources]
    return "\n".join(lines)


@tool
def list_skills() -> str:
    """列出所有可用的 skills"""
    summaries = get_all_skills_summary()
    if not summaries:
        return "No skills found"
    lines = [f"- **{s['title']}**: {s['description'][:100]}..." for s in summaries]
    return "\n".join(lines)


@tool
def get_skill_content(skill_name: str) -> str:
    """
    获取 skill 详细内容

    Args:
        skill_name: skill 名称（如 browser-harness, arxiv, twitter）
    """
    content = load_skill(skill_name)
    if content:
        return content
    return f"Skill '{skill_name}' not found"


# =====================
# 创建 Deep Agent
# =====================

def create_research_agent():
    """创建科研情报 Agent"""

    tools = [
        # Crawling
        crawl_webpage,
        save_to_sources,
        # Wiki
        ingest_to_wiki,
        query_wiki,
        wiki_status,
        wiki_health_check,
        # Search
        search_arxiv,
        twitter_bookmarks,
        twitter_profile,
        # Utils
        save_processed,
        list_all_sources,
        list_skills,
        get_skill_content,
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
        skills=[str(Path(__file__).parent / "skills")],
        system_prompt="""你是一个顶级 AI 科研情报助手，代号 InfoGet Research Agent。

你的职责是从网络、论文、社交媒体收集科研情报，并进行结构化分析存入知识库。

核心数据流水线：
1. 爬取内容 → save_to_sources → sources/
2. AI 处理后 → ingest_to_wiki → wiki/
3. 查询知识 → query_wiki

InfoGet 工具：
- crawl_webpage: 抓取任意网页
- save_to_sources: 保存到 sources/（带 frontmatter）
- ingest_to_wiki: 把 source 消化成 wiki 知识页面
- query_wiki: 查询 wiki 知识
- search_arxiv: 搜索 arXiv 论文
- twitter_bookmarks: 抓取 Twitter 书签
- twitter_profile: 抓取用户推文
- save_processed: 保存分析报告
- list_all_sources: 列出 sources
- list_skills: 列出 skills
- get_skill_content: 查看 skill 详情

Sources 结构：
- sources/paper/hostname/date/
- sources/blog/hostname/date/
- sources/social/hostname/date/
- sources/code/hostname/date/

Wiki Frontmatter:
- title, source, tags, related_*, created, updated

工作流程：
1. 分析用户需求，确定数据源
2. 爬取内容并保存到 sources/
3. ingest 到 wiki（AI 消化）
4. 如有关联，更新 frontmatter 的 related_*
5. 生成结构化报告

输出格式：中文报告，包含核心发现和知识关联""",
        backend=backend,
        checkpointer=MemorySaver(),
    )

    return agent


# =====================
# 运行入口
# =====================

def run_research(query: str, thread_id: str = "default"):
    """运行科研任务"""
    # 确保 wiki 已初始化
    ensure_wiki_initialized()

    agent = create_research_agent()
    config = {"configurable": {"thread_id": thread_id}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]},
        config=config
    )

    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="InfoGet Research Agent")
    parser.add_argument("--query", "-q", default="列出我所有的 skills")
    parser.add_argument("--thread", "-t", default="default", help="会话线程 ID")
    args = parser.parse_args()

    print(f"[*] InfoGet Research Agent")
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
