"""
tool_categories.py
------------------
Helper utilities for category-based tool filtering
and display inside the Streamlit app.
"""

import pandas as pd
import os

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tools.csv"
)

# Ordered list used in sidebar filter
CATEGORY_ORDER = [
    "All",
    "General AI",
    "Research",
    "Writing",
    "Presentation",
    "Design",
    "Mathematics",
    "Coding",
    "Language Learning",
    "Productivity",
    "Study Tools",
    "Video & Media",
    "Collaboration",
    "Online Learning",
]

# Emoji icon for each category (used in UI)
CATEGORY_ICONS = {
    "General AI":        "🤖",
    "Research":          "🔬",
    "Writing":           "✍️",
    "Presentation":      "📊",
    "Design":            "🎨",
    "Mathematics":       "➗",
    "Coding":            "💻",
    "Language Learning": "🌍",
    "Productivity":      "⚡",
    "Study Tools":       "📚",
    "Video & Media":     "🎥",
    "Collaboration":     "🤝",
    "Online Learning":   "🎓",
    "All":               "✨",
}


def get_all_categories():
    """Return the ordered list of available categories."""
    return CATEGORY_ORDER


def get_category_icon(category: str) -> str:
    """Return the emoji icon for a category."""
    return CATEGORY_ICONS.get(category, "📌")


def get_tools_by_category(category: str) -> pd.DataFrame:
    """
    Load tools.csv and return tools filtered by category.
    Returns all tools if category is 'All' or empty.
    """
    df = pd.read_csv(DATA_FILE).fillna("")

    if not category or category == "All":
        return df

    return df[df["Category"].str.strip() == category].reset_index(drop=True)


def get_category_counts() -> dict:
    """
    Return a dict of {category: tool_count} for every
    category in the dataset (useful for sidebar badges).
    """
    df = pd.read_csv(DATA_FILE).fillna("")
    counts = df["Category"].str.strip().value_counts().to_dict()
    return counts


def get_skill_levels() -> list:
    """Return the fixed skill-level options."""
    return ["Beginner", "Intermediate", "Advanced"]
