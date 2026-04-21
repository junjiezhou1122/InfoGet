"""
InfoGet - Research Knowledge Management System
"""

from .source_manager import (
    extract_hostname,
    get_source_type,
    get_source_path,
    create_frontmatter,
    save_source,
    load_source,
    list_sources,
    SOURCE_TYPES,
)

from .wiki_bridge import (
    wiki_init,
    wiki_ingest,
    wiki_query,
    wiki_search,
    wiki_add,
    wiki_lint,
    wiki_graph,
    wiki_status,
    wiki_list,
    is_wiki_initialized,
    ensure_wiki_initialized,
)

from .crawler import (
    crawl_url_auto,
    crawl_arxiv_paper,
    crawl_twitter_opencli,
    crawl_and_save,
    crawl_twitter_and_save,
)

from .skills_loader import (
    list_skills,
    load_skill,
    get_skill_summary,
    search_skills,
    get_all_skills_summary,
)

__all__ = [
    "extract_hostname",
    "get_source_type",
    "get_source_path",
    "create_frontmatter",
    "save_source",
    "load_source",
    "list_sources",
    "SOURCE_TYPES",
    "wiki_init",
    "wiki_ingest",
    "wiki_query",
    "wiki_search",
    "wiki_add",
    "wiki_lint",
    "wiki_graph",
    "wiki_status",
    "wiki_list",
    "is_wiki_initialized",
    "ensure_wiki_initialized",
    "crawl_url_auto",
    "crawl_arxiv_paper",
    "crawl_twitter_opencli",
    "crawl_and_save",
    "crawl_twitter_and_save",
    "list_skills",
    "load_skill",
    "get_skill_summary",
    "search_skills",
    "get_all_skills_summary",
]
