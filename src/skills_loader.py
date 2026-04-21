"""
Skills Loader - Load and manage skills markdown documents
"""

import re
from pathlib import Path
from typing import Optional

SKILLS_DIR = Path(__file__).parent.parent / "skills"


def list_skills() -> list[str]:
    """List all available skills."""
    if not SKILLS_DIR.exists():
        return []

    skills = []
    for md_file in SKILLS_DIR.rglob("*.md"):
        # Get relative path from skills dir
        rel = md_file.relative_to(SKILLS_DIR)
        skills.append(str(rel))
    return skills


def load_skill(skill_name: str) -> Optional[str]:
    """
    Load a skill markdown file.

    Args:
        skill_name: e.g., "browser-harness", "arxiv", "twitter"

    Returns:
        Skill content or None if not found
    """
    # Try different patterns
    patterns = [
        SKILLS_DIR / f"{skill_name}.md",
        SKILLS_DIR / skill_name / "*.md",
        SKILLS_DIR / skill_name / "SKILL.md",
    ]

    for pattern in patterns:
        if pattern.exists():
            with open(pattern, "r", encoding="utf-8") as f:
                return f.read()

    # Search recursively
    for md_file in SKILLS_DIR.rglob("*.md"):
        if skill_name.lower() in md_file.stem.lower():
            with open(md_file, "r", encoding="utf-8") as f:
                return f.read()

    return None


def _find_skill_file(skill_name: str):
    """Find the actual file path for a skill name."""
    # Strip .md if present
    name = skill_name.replace(".md", "")

    # Direct match
    direct = SKILLS_DIR / f"{name}.md"
    if direct.exists():
        return direct

    # Stem match
    for md_file in SKILLS_DIR.rglob("*.md"):
        if md_file.stem.lower() == name.lower():
            return md_file

    # Partial match
    for md_file in SKILLS_DIR.rglob("*.md"):
        if name.lower() in md_file.stem.lower():
            return md_file
    return None


def get_skill_summary(skill_name: str) -> Optional[dict]:
    """
    Get skill summary info.

    Returns:
        dict with: name, description, commands, or None
    """
    skill_file = _find_skill_file(skill_name)
    if not skill_file:
        return None

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract title (first H1)
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    title = title_match.group(1) if title_match else skill_name

    # Extract description (first paragraph after title)
    desc_match = re.search(r"^# .+$\n\n(.+?)(?=\n\n##|\n#|$)",
                          content, re.MULTILINE | re.DOTALL)
    description = desc_match.group(1).strip() if desc_match else ""

    # Extract commands from code blocks
    commands = re.findall(r"```\w*\n(.+?)\n```", content, re.DOTALL)

    return {
        "name": skill_name,
        "title": title,
        "description": description[:200],
        "commands": commands[:5],  # First 5 commands
    }


def search_skills(query: str) -> list[str]:
    """
    Search skills by keyword.

    Args:
        query: Search query

    Returns:
        List of matching skill names
    """
    matching = []
    for skill in list_skills():
        content = load_skill(skill)
        if content and query.lower() in content.lower():
            matching.append(skill)
    return matching


def get_all_skills_summary() -> list[dict]:
    """Get summary of all skills."""
    summaries = []
    for skill in list_skills():
        summary = get_skill_summary(skill)
        if summary:
            summaries.append(summary)
    return summaries
