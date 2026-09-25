import streamlit as st

from recommender import recommend_tools, compare_tools
from tool_categories import (
    get_all_categories,
    get_category_icon,
    get_category_counts,
)

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Student360 AI Advisor",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Custom CSS — Pinterest-inspired pink & rose theme
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Background ── soft warm off-white like Pinterest */
    .stApp {
        background: #fdf0f3;
    }

    /* ── Hero banner ── */
    .hero {
        background: linear-gradient(135deg, #e60050 0%, #ff4d7d 40%, #ff85a1 100%);
        border-radius: 24px;
        padding: 2.8rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 40px rgba(230, 0, 80, 0.25);
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -60px;
        right: -60px;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -80px;
        left: -40px;
        width: 260px;
        height: 260px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.7rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.5rem;
        line-height: 1.2;
        text-shadow: 0 2px 12px rgba(0,0,0,0.15);
    }
    .hero-sub {
        color: rgba(255,255,255,0.88);
        font-size: 1.05rem;
        margin: 0;
        max-width: 580px;
        line-height: 1.6;
    }
    .hero-stats {
        display: flex;
        gap: 2.5rem;
        margin-top: 1.8rem;
    }
    .hero-stat {
        text-align: center;
    }
    .hero-stat-num {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
    }
    .hero-stat-label {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.75);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.1rem;
    }

    /* ── Streamlit text-area ── */
    .stTextArea textarea {
        background: #ffffff !important;
        border: 2px solid #f9c0cf !important;
        border-radius: 14px !important;
        color: #2d1b24 !important;
        font-size: 1.02rem !important;
        padding: 1rem 1.1rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
        box-shadow: 0 2px 8px rgba(230,0,80,0.06) !important;
    }
    .stTextArea textarea:focus {
        border-color: #e60050 !important;
        box-shadow: 0 0 0 3px rgba(230,0,80,0.12) !important;
    }
    .stTextArea textarea::placeholder { color: #c4849a !important; }

    /* ── Primary button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #e60050 0%, #ff4d7d 100%) !important;
        border: none !important;
        border-radius: 14px !important;
        color: white !important;
        font-size: 1.08rem !important;
        font-weight: 700 !important;
        padding: 0.8rem 2rem !important;
        transition: transform 0.15s, box-shadow 0.15s !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 20px rgba(230,0,80,0.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(230,0,80,0.45) !important;
    }
    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
    }

    /* ── Tool card ── */
    .tool-card {
        background: #ffffff;
        border: 1.5px solid #fadadd;
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        transition: border-color 0.25s, transform 0.2s, box-shadow 0.2s;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(230,0,80,0.06);
    }
    .tool-card:hover {
        border-color: #e60050;
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(230,0,80,0.15);
    }
    .tool-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #e60050, #ff85a1, #ffb3c6);
        opacity: 0;
        transition: opacity 0.25s;
        border-radius: 20px 20px 0 0;
    }
    .tool-card:hover::before { opacity: 1; }

    /* ── Tool name ── */
    .tool-name {
        font-size: 1.35rem;
        font-weight: 800;
        color: #1a0a10;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .tool-rank {
        font-size: 0.88rem;
        font-weight: 700;
        color: #e60050;
        background: rgba(230,0,80,0.08);
        padding: 0.15rem 0.55rem;
        border-radius: 7px;
        border: 1px solid rgba(230,0,80,0.2);
        flex-shrink: 0;
    }

    /* ── Match score badge ── */
    .score-high   { background: linear-gradient(135deg,#00c853,#00bfa5); }
    .score-medium { background: linear-gradient(135deg,#ff9800,#ff6f00); }
    .score-low    { background: linear-gradient(135deg,#bdbdbd,#9e9e9e); }
    .score-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        color: white;
        padding: 0.3rem 0.9rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.88rem;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    /* ── Pills ── */
    .cat-pill {
        display: inline-block;
        background: rgba(230,0,80,0.07);
        color: #c0003a;
        border: 1px solid rgba(230,0,80,0.18);
        padding: 0.22rem 0.8rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .skill-pill {
        display: inline-block;
        background: rgba(168,85,247,0.08);
        color: #7c3aed;
        border: 1px solid rgba(168,85,247,0.2);
        padding: 0.22rem 0.8rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .free-pill {
        display: inline-block;
        background: rgba(16,185,129,0.08);
        color: #059669;
        border: 1px solid rgba(16,185,129,0.2);
        padding: 0.22rem 0.8rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ── Best-use text ── */
    .best-use {
        color: #4a2030;
        font-size: 0.95rem;
        margin: 0.7rem 0 0.3rem;
        line-height: 1.55;
    }

    /* ── Reason items ── */
    .reason-item {
        background: rgba(230,0,80,0.04);
        border-left: 3px solid #e60050;
        padding: 0.45rem 0.9rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 0.4rem;
        font-size: 0.88rem;
        color: #7a2035;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: #fff0f3 !important;
        border-right: 1.5px solid #fadadd !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #4a1020 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1a0a10 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stSlider label {
        color: #4a1020 !important;
        font-weight: 600 !important;
    }

    /* Sidebar selectbox & slider accent */
    section[data-testid="stSidebar"] .stSlider > div > div > div {
        background: #e60050 !important;
    }

    /* ── Result header ── */
    .results-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .results-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #1a0a10;
        margin: 0;
    }
    .results-count {
        background: rgba(230,0,80,0.08);
        color: #c0003a;
        border: 1px solid rgba(230,0,80,0.2);
        padding: 0.2rem 0.8rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    /* ── Input label ── */
    .task-label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #c0003a;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.5rem;
    }

    /* ── Example chips ── */
    .example-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 0.8rem;
    }
    .chip {
        background: #ffffff;
        color: #c0003a;
        border: 1.5px solid #fadadd;
        padding: 0.32rem 0.9rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: default;
        box-shadow: 0 1px 4px rgba(230,0,80,0.08);
        transition: background 0.15s;
    }
    .chip:hover { background: #fff0f3; }

    /* ── Compare card ── */
    .compare-col {
        background: #ffffff;
        border: 1.5px solid #fadadd;
        border-radius: 16px;
        padding: 1.3rem;
        box-shadow: 0 2px 10px rgba(230,0,80,0.07);
    }
    .compare-tool-name {
        font-size: 1.12rem;
        font-weight: 800;
        color: #1a0a10;
        margin-bottom: 0.8rem;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: #fff5f7 !important;
        border-radius: 10px !important;
        color: #c0003a !important;
        font-weight: 600 !important;
    }

    /* ── Misc ── */
    #MainMenu, footer { visibility: hidden; }
    hr { border-color: #fadadd !important; }

    /* scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #fdf0f3; }
    ::-webkit-scrollbar-thumb { background: #f9c0cf; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #e60050; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Hero header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🌸 Student360 AI Advisor</div>
        <p class="hero-sub">
            Tell us what you're working on and we'll instantly match you
            with the best AI tools — for writing, coding, research, design and more.
        </p>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-num">97+</div>
                <div class="hero-stat-label">AI Tools</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">13</div>
                <div class="hero-stat-label">Categories</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-num">Smart</div>
                <div class="hero-stat-label">Matching</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Sidebar — filters
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 🔍 Filters")

    categories      = get_all_categories()
    category_counts = get_category_counts()

    category_labels = []
    for cat in categories:
        if cat == "All":
            total = sum(category_counts.values())
            category_labels.append(f"{get_category_icon('All')} All  ({total})")
        else:
            count = category_counts.get(cat, 0)
            category_labels.append(f"{get_category_icon(cat)} {cat}  ({count})")

    selected_label = st.radio(
        "Category",
        options=category_labels,
        index=0,
        label_visibility="collapsed",
    )

    selected_index  = category_labels.index(selected_label)
    category_filter = categories[selected_index]

    st.divider()

    skill_level = st.selectbox(
        "🧠 Skill Level",
        ["Beginner", "Intermediate", "Advanced"],
        help="Select your experience level with AI tools",
    )

    top_n = st.slider(
        "📋 Number of results",
        min_value=3,
        max_value=10,
        value=5,
    )

    show_compare = st.toggle("⚖️ Compare mode", value=False)

    st.divider()

    st.markdown(
        """
        <div style='font-size:0.82rem;color:#b06070;line-height:1.7;'>
        💡 <b style='color:#c0003a;'>Pro tip:</b> Be specific about your
        task for smarter recommendations.<br><br>
        <i style='color:#c4849a;'>"Write a 3-page essay on climate
        change for my English assignment"</i>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --------------------------------------------------
# Main — single smart input
# --------------------------------------------------

st.markdown(
    "<div class='task-label'>🎯 What do you need help with today?</div>",
    unsafe_allow_html=True,
)

task = st.text_area(
    label="task_input",
    label_visibility="collapsed",
    placeholder=(
        "Describe your task in plain English...\n\n"
        "Examples:\n"
        "• Create a PowerPoint presentation for my DBMS project\n"
        "• Write a 5-page essay on climate change for English class\n"
        "• Solve calculus problems and show step-by-step working\n"
        "• Build a Python web scraper for my data science project\n"
        "• Translate my notes from Hindi to English and summarise them"
    ),
    height=160,
)

# Example chips
st.markdown(
    """
    <div class='example-chips'>
        <span class='chip'>📊 Make a presentation</span>
        <span class='chip'>✍️ Write an essay</span>
        <span class='chip'>💻 Debug my code</span>
        <span class='chip'>🔬 Find research papers</span>
        <span class='chip'>➗ Solve math problems</span>
        <span class='chip'>🎥 Create a video</span>
        <span class='chip'>🌍 Learn a language</span>
        <span class='chip'>📚 Study for exams</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

find_btn = st.button(
    "🌸  Find Best AI Tools",
    use_container_width=True,
    type="primary",
)

# --------------------------------------------------
# Results
# --------------------------------------------------

if find_btn:

    if not task.strip():
        st.warning("⚠️ Please describe your task above before searching.")
    else:
        with st.spinner("🌸 Finding the best AI tools for you…"):
            results = recommend_tools(
                task=task,
                skill_level=skill_level,
                category_filter=category_filter,
                top_n=top_n,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if not results:
            st.info(
                "🔎 No tools found for the selected filters. "
                "Try broadening your category or rephrasing your task."
            )
        else:
            # ── Result header ──
            st.markdown(
                f"""
                <div class='results-header'>
                    <span class='results-title'>🏆 Recommended AI Tools</span>
                    <span class='results-count'>{len(results)} results</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # ── Compare mode ──
            if show_compare:
                st.caption("☑️ Select at least 2 tools to compare side-by-side.")
                selected_for_compare = []

                for index, result in enumerate(results):
                    checked = st.checkbox(
                        f"**{index + 1}. {result['tool']}**  —  {result['score']}% match",
                        key=f"cmp_{index}",
                    )
                    if checked:
                        selected_for_compare.append(result["tool"])

                if len(selected_for_compare) >= 2:
                    compare_data = compare_tools(selected_for_compare)
                    st.divider()
                    st.markdown("### 📊 Side-by-Side Comparison")

                    cols = st.columns(len(compare_data))
                    for col, tool_info in zip(cols, compare_data):
                        with col:
                            st.markdown(
                                f"""
                                <div class='compare-col'>
                                    <div class='compare-tool-name'>
                                        {get_category_icon(tool_info['category'])} {tool_info['tool']}
                                    </div>
                                    <span class='cat-pill'>{tool_info['category']}</span><br><br>
                                    <b style='color:#c0003a;'>Best for:</b><br>
                                    <span style='color:#4a2030;font-size:0.9rem;'>{tool_info['best_use']}</span><br><br>
                                    <b style='color:#c0003a;'>Free option:</b><br>
                                    <span style='color:#4a2030;font-size:0.9rem;'>{tool_info['free_option']}</span><br><br>
                                    <b style='color:#c0003a;'>Skill level:</b><br>
                                    <span style='color:#7c3aed;font-size:0.9rem;'>{tool_info['skill_level']}</span>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                            if tool_info["url"]:
                                st.link_button("🔗 Open Tool", tool_info["url"], use_container_width=True)

                elif len(selected_for_compare) == 1:
                    st.info("Select at least one more tool to compare.")

            # ── Normal cards ──
            else:
                for index, result in enumerate(results):

                    score = result["score"]
                    if score >= 65:
                        badge_class = "score-high"
                        score_icon  = "🟢"
                    elif score >= 40:
                        badge_class = "score-medium"
                        score_icon  = "🟡"
                    else:
                        badge_class = "score-low"
                        score_icon  = "⚪"

                    cat_icon = get_category_icon(result["category"])
                    url      = result.get("url", "")
                    free_val = result.get("free_option", "")
                    free_pill = (
                        f"<span class='free-pill'>✅ {free_val[:30]}</span>"
                        if free_val else ""
                    )
                    url_btn = (
                        f'<a href="{url}" target="_blank" '
                        f'style="display:inline-block;background:rgba(230,0,80,0.07);'
                        f'color:#c0003a;border:1.5px solid rgba(230,0,80,0.2);'
                        f'padding:0.28rem 1rem;border-radius:999px;'
                        f'font-size:0.82rem;font-weight:700;text-decoration:none;'
                        f'margin-top:0.7rem;transition:background 0.15s;">'
                        f'🔗 Visit Tool →</a>'
                        if url else ""
                    )

                    st.markdown(
                        f"""
                        <div class="tool-card">
                            <div style="display:flex;justify-content:space-between;
                                        align-items:flex-start;flex-wrap:wrap;gap:0.5rem;">
                                <div class="tool-name">
                                    <span class="tool-rank">#{index + 1}</span>
                                    {cat_icon} {result['tool']}
                                </div>
                                <span class="score-badge {badge_class}">
                                    {score_icon} {score}% Match
                                </span>
                            </div>
                            <div style="margin-top:0.7rem;display:flex;
                                        flex-wrap:wrap;gap:0.35rem;align-items:center;">
                                <span class="cat-pill">{cat_icon} {result['category']}</span>
                                <span class="skill-pill">🧠 {result['skill_level']}</span>
                                {free_pill}
                            </div>
                            <p class="best-use">
                                <b style="color:#e60050;">Best for:</b> {result['best_use']}
                            </p>
                            {url_btn}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.expander(
                        f"💡 Why {result['tool']}?",
                        expanded=(index == 0),
                    ):
                        for reason in result["reasons"]:
                            if reason.startswith("[Visit Tool]"):
                                st.markdown(reason)
                            else:
                                st.markdown(
                                    f'<div class="reason-item">✓ {reason}</div>',
                                    unsafe_allow_html=True,
                                )

# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()
st.markdown(
    """
    <div style="text-align:center;color:#c4849a;font-size:0.82rem;padding:0.5rem 0 1.2rem;">
        🌸 Student360 AI Advisor — Smart matching across
        <b style="color:#e60050;">97+ curated AI tools</b>
        across 13 categories &nbsp;|&nbsp; Made with ♥ for students
    </div>
    """,
    unsafe_allow_html=True,
)
