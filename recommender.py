"""
recommender.py
--------------
Smart recommendation engine for Student360 AI Advisor.

Improvements over v1:
  - Intent detection: maps user query to likely categories
  - Synonym expansion: expands task keywords before matching
  - Category affinity boost: tools whose category matches detected intent score higher
  - Richer corpus: Best use + Tasks + Category + Tool name all contribute
  - Better weighted blending of TF-IDF + keyword + intent signals
"""

import pandas as pd
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------------------------------
# Load AI tool dataset
# --------------------------------------------------

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tools.csv"
)


def load_tools():
    df = pd.read_csv(DATA_FILE)
    df = df.fillna("")
    return df


# --------------------------------------------------
# Text normalization
# --------------------------------------------------

def normalize(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# --------------------------------------------------
# Synonym / intent expansion map
# Maps common student phrases → extra keywords injected into their query
# --------------------------------------------------

EXPANSIONS = {
    # Presentations
    "presentation": "slides ppt powerpoint deck present gamma decktopus beautiful",
    "ppt":          "presentation slides powerpoint deck gamma decktopus",
    "powerpoint":   "presentation slides ppt deck gamma microsoft",
    "slides":       "presentation deck ppt slide show gamma google slides",
    "slide deck":   "presentation slides ppt powerpoint gamma",

    # Writing / Essays
    "essay":        "write writing draft essay academic paragraph grammarly jenni writesonic",
    "write":        "writing essay draft paragraph grammarly jenni writesonic copy",
    "writing":      "essay draft grammar grammarly quillbot jenni writesonic wordtune",
    "report":       "writing document report essay academic draft jenni writesonic",
    "paragraph":    "writing essay draft grammarly wordtune quillbot",
    "thesis":       "academic writing research essay jenni paperpal grammarly",

    # Research
    "research":     "papers academic literature review find sources perplexity elicit scispace semantic",
    "paper":        "research academic literature review find sources perplexity elicit scispace",
    "literature":   "research papers review elicit scispace semantic scholar connected",
    "references":   "research papers citation bibliography elicit scite semantic",
    "bibliography": "research papers citation references elicit scite perplexity",
    "citation":     "research papers references scite semantic scholar elicit",
    "journal":      "academic research paper literature elicit scispace semantic scholar",

    # Coding / Programming
    "code":         "coding programming debug python javascript github copilot cursor codeium replit",
    "coding":       "programming debug python javascript github copilot cursor codeium replit phind",
    "programming":  "code debug python java javascript github copilot cursor codeium replit",
    "debug":        "coding error fix bug python javascript github copilot cursor phind codeium",
    "python":       "coding programming debug script github copilot cursor codeium replit phind",
    "javascript":   "coding programming web development github copilot cursor codeium",
    "web scraper":  "coding python programming automation github copilot replit cursor",
    "software":     "coding programming development github copilot cursor codeium",
    "app":          "coding programming development software build github copilot replit",
    "error":        "debug coding fix bug programming github copilot phind stackoverflow cursor",
    "bug":          "debug coding fix error programming github copilot phind cursor",

    # Mathematics
    "math":         "mathematics calculate equation algebra calculus symbolab mathway wolfram photomath",
    "mathematics":  "math equations algebra calculus symbolab mathway wolfram photomath khanmigo",
    "calculus":     "math mathematics differentiation integration limits symbolab mathway wolfram",
    "algebra":      "math mathematics equations solve symbolab mathway wolfram photomath khanmigo",
    "geometry":     "math mathematics shapes angles symbolab mathway wolfram photomath",
    "statistics":   "math mathematics data analysis probability symbolab mathway wolfram julius",
    "equation":     "math mathematics solve algebra calculus symbolab mathway wolfram",
    "formula":      "math mathematics science wolfram alpha symbolab mathway",
    "graph":        "math desmos graphing plot visualize equations functions",
    "calculus problems": "calculus math symbolab mathway wolfram khanmigo photomath step by step",

    # Design / Visuals
    "design":       "visual graphics image create canva poster logo microsoft designer",
    "poster":       "design visual graphics canva microsoft designer ideogram adobe express",
    "image":        "design generate picture illustration canva dall-e adobe firefly microsoft designer",
    "logo":         "design graphic branding canva ideogram adobe express microsoft designer",
    "infographic":  "design visual data canva microsoft designer adobe express",
    "banner":       "design graphic canva microsoft designer ideogram adobe express",
    "artwork":      "design image illustration midjourney stable diffusion adobe firefly leonardo",
    "illustration": "design image art midjourney stable diffusion adobe firefly leonardo dall-e",
    "thumbnail":    "design image visual canva microsoft designer youtube thumbnail",
    "flyer":        "design poster graphic canva microsoft designer adobe express",

    # Video & Media
    "video":        "video create edit media runway lumen5 pictory synthesia descript",
    "voiceover":    "voice text-to-speech audio murf elevenlabs narrate",
    "audio":        "voice speech text-to-speech elevenlabs murf otter transcribe",
    "music":        "audio background suno ai music generation sound",
    "transcribe":   "transcription audio speech to text otter fireflies descript lecture",
    "recording":    "transcribe audio lecture otter fireflies descript voice to text",

    # Study Tools
    "flashcard":    "study revision spaced repetition anki quizlet brainscape knowt studyfetch",
    "quiz":         "study test revision flashcard quizlet anki knowt studyfetch notebooklm",
    "study":        "revision exam flashcard quiz notes notebooklm quizlet anki mindgrasp",
    "exam":         "study revision test flashcard quiz preparation anki quizlet brainscape",
    "revision":     "study exam flashcard quiz notes anki quizlet brainscape knowt",
    "notes":        "study note-taking summarize notebooklm mindgrasp notion knowt otter",
    "summarize":    "summary notes study quillbot notebooklm mindgrasp chatgpt claude",
    "summary":      "summarize notes study quillbot notebooklm mindgrasp chatgpt claude",
    "mindmap":      "visual mind map concept map miro mapify brainstorm organize",
    "homework":     "help study solve explain chatgpt socratic khanmigo quizlet photomath",

    # Language Learning
    "language":     "learn speak translate language duolingo hellotalk speak elsa beelinguapp",
    "translate":    "translation language deepl google translate multilingual text",
    "french":       "language learning duolingo hellotalk beelinguapp speak foreign language",
    "spanish":      "language learning duolingo hellotalk beelinguapp speak foreign language",
    "english":      "writing grammar grammarly quillbot language learning elsa speak pronunciation",
    "vocabulary":   "language learning words duolingo quizlet anki flashcard memorize",
    "pronunciation": "language speaking elsa speak duolingo pronunciation practice accent",

    # Productivity
    "schedule":     "plan organize time management notion motion reclaim calendar study planner",
    "plan":         "schedule organize project notion taskade motion study plan",
    "organize":     "notes productivity notion obsidian mem organize study material",
    "calendar":     "schedule plan time management motion reclaim study planner",
    "deadline":     "schedule plan time management motion reclaim notion task",
    "project":      "management collaborate plan notion taskade miro team work",
    "collaborate":  "team group project taskade miro notion real-time collaboration",

    # General
    "explain":      "understand concept chatgpt gemini claude explainpaper khanmigo socratic",
    "understand":   "explain concept chatgpt gemini claude notebooklm explainpaper khanmigo",
    "learn":        "study course online coursera edx udemy linkedin chatgpt khanmigo",
    "help":         "assist chatgpt gemini claude general AI homework",
    "generate":     "create make produce AI tool chatgpt gemini content",
    "create":       "make generate design produce AI tool",
    "convert":      "transform change format translate text video audio",
    "improve":      "better enhance grammar writing grammarly wordtune quillbot hemingway",
    "proofread":    "grammar check writing grammarly languagetool hemingway wordtune",
    "brainstorm":   "ideas generate chatgpt gemini claude notion miro creative",
}

# Intent → Category mapping with weights
# Detects what kind of task the user wants based on keywords in their query
INTENT_CATEGORIES = {
    "Presentation": [
        "presentation", "ppt", "powerpoint", "slides", "slide", "deck",
        "present", "slideshow", "slide deck"
    ],
    "Writing": [
        "essay", "write", "writing", "report", "paragraph", "thesis",
        "draft", "article", "blog", "content", "proofread", "grammar",
        "paraphrase", "rephrase", "translate", "summarize", "summary"
    ],
    "Research": [
        "research", "paper", "papers", "literature", "academic", "journal",
        "citation", "bibliography", "references", "scholarly", "thesis",
        "review", "sources", "study papers"
    ],
    "Coding": [
        "code", "coding", "programming", "program", "python", "javascript",
        "java", "html", "css", "sql", "debug", "error", "bug", "function",
        "script", "software", "app", "develop", "algorithm", "web scraper",
        "data structure", "api"
    ],
    "Mathematics": [
        "math", "mathematics", "calculate", "calculus", "algebra",
        "geometry", "statistics", "equation", "formula", "solve",
        "differentiate", "integrate", "graph", "plot", "probability",
        "trigonometry", "matrices", "numeric"
    ],
    "Design": [
        "design", "poster", "image", "logo", "infographic", "banner",
        "artwork", "illustration", "thumbnail", "flyer", "graphic",
        "visual", "picture", "draw", "art", "creative", "canva"
    ],
    "Video & Media": [
        "video", "voiceover", "audio", "music", "transcribe", "recording",
        "subtitle", "caption", "animation", "film", "speech", "voice",
        "podcast", "edit video"
    ],
    "Study Tools": [
        "flashcard", "quiz", "study", "exam", "revision", "notes",
        "summarize", "summary", "mindmap", "mind map", "homework",
        "learn", "memorize", "recall", "test", "practice"
    ],
    "Language Learning": [
        "language", "translate", "french", "spanish", "german",
        "japanese", "english", "vocabulary", "pronunciation", "speaking",
        "foreign", "multilingual", "duolingo", "accent"
    ],
    "Productivity": [
        "schedule", "plan", "organize", "calendar", "deadline", "time",
        "task", "manage", "productivity", "planner", "reminder", "efficient"
    ],
    "Research": [
        "research", "find papers", "paper", "literature", "academic",
        "journal", "citation", "reference", "scholarly"
    ],
    "Collaboration": [
        "collaborate", "team", "group", "project", "together", "share",
        "co-work", "brainstorm together"
    ],
    "General AI": [
        "explain", "understand", "help", "assist", "question", "answer",
        "clarify", "doubt", "general", "chat", "conversation"
    ],
}


def detect_intent(task: str) -> dict:
    """
    Detect which categories the user's task maps to.
    Returns {category: score} where score is 0-1.
    """
    task_lower = task.lower()
    scores = {}

    for category, keywords in INTENT_CATEGORIES.items():
        hits = sum(1 for kw in keywords if kw in task_lower)
        if hits > 0:
            scores[category] = min(hits / 3.0, 1.0)  # cap at 1.0

    return scores


def expand_query(task: str) -> str:
    """
    Expand the user's query with synonyms and related keywords.
    This dramatically improves TF-IDF matching on short queries.
    """
    task_lower = task.lower()
    extra = []

    for trigger, expansion in EXPANSIONS.items():
        if trigger in task_lower:
            extra.append(expansion)

    if extra:
        return task + " " + " ".join(extra)
    return task


# --------------------------------------------------
# Keyword extraction
# --------------------------------------------------

STOP_WORDS = {
    "i", "want", "to", "a", "an", "the", "for", "my", "and", "of",
    "in", "on", "with", "need", "please", "can", "me", "is", "are",
    "be", "do", "this", "that", "it", "have", "use", "get", "some",
    "just", "also", "from", "at", "or", "but", "so", "we", "you",
    "he", "she", "they", "will", "about", "how", "what", "which",
    "who", "its", "give", "show", "using", "should", "must", "could",
    "would", "make", "create", "help", "need", "let",
}


def get_keywords(text: str) -> set:
    words = normalize(text).split()
    return {w for w in words if w not in STOP_WORDS and len(w) > 2}


# --------------------------------------------------
# TF-IDF similarity
# --------------------------------------------------

def tfidf_similarity(query: str, corpus_texts: list) -> list:
    if not query.strip():
        return [0.0] * len(corpus_texts)

    all_texts = [normalize(query)] + [normalize(t) for t in corpus_texts]

    try:
        vectorizer   = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        query_vec    = tfidf_matrix[0]
        corpus_mat   = tfidf_matrix[1:]
        scores       = cosine_similarity(query_vec, corpus_mat).flatten()
        return scores.tolist()
    except ValueError:
        return [0.0] * len(corpus_texts)


# --------------------------------------------------
# Keyword overlap score
# --------------------------------------------------

def keyword_match(student_text: str, tool_text: str) -> float:
    student_kw = get_keywords(student_text)
    tool_kw    = get_keywords(tool_text)
    if not student_kw:
        return 0.0
    return len(student_kw & tool_kw) / len(student_kw)


# --------------------------------------------------
# Skill-level match
# --------------------------------------------------

def skill_match(tool_skill_levels: str, student_skill: str) -> float:
    if not tool_skill_levels.strip():
        return 0.5
    levels = [lvl.strip().lower() for lvl in tool_skill_levels.split(",")]
    return 1.0 if student_skill.lower() in levels else 0.2


# --------------------------------------------------
# Generate explanation reasons
# --------------------------------------------------

def generate_reason(tool: dict, task_score: float, s_match: float,
                    intent_boost: float) -> list:
    reasons = []

    if task_score >= 0.55:
        reasons.append("Excellent match for your requested task")
    elif task_score >= 0.35:
        reasons.append("Strong match for your requested task")
    elif task_score >= 0.15:
        reasons.append("Relevant to your requested task")

    if intent_boost > 0.3:
        reasons.append(f"Specifically designed for {tool.get('Category', 'this type of task')}")
    elif intent_boost > 0:
        reasons.append(f"Useful for {tool.get('Category', 'your task type')}")

    if s_match == 1.0:
        reasons.append("Matches your experience level")
    elif s_match == 0.5:
        reasons.append("Suitable for all skill levels")

    free_val = str(tool.get("Free option", "")).lower()
    if free_val.startswith("yes"):
        reasons.append("Has a free plan or free tier")

    tasks = str(tool.get("Useful student tasks", "")).strip()
    if tasks:
        first = tasks.split(",")[0].strip()
        if first and len(first) > 5:
            reasons.append(f"Can help you: {first.lower()}")

    url = str(tool.get("URL", "")).strip()
    if url:
        reasons.append(f"[Visit Tool]({url})")

    if not reasons:
        reasons.append("General relevance to your request")

    return reasons


# --------------------------------------------------
# Main recommendation engine
# --------------------------------------------------

def recommend_tools(
    task: str,
    skill_level: str = "Beginner",
    category_filter: str = "All",
    top_n: int = 5,
    # Legacy params kept for backwards compatibility
    context: str = "",
    output_type: str = "",
) -> list:
    """
    Given a free-text task description, return the top-N AI tools ranked by
    relevance using TF-IDF + keyword matching + intent detection + category boost.
    """
    df = load_tools()

    # Category filter (sidebar selection)
    if category_filter and category_filter != "All":
        df = df[df["Category"].str.strip() == category_filter]

    if df.empty:
        return []

    # ── Step 1: Expand the user query with synonyms ──
    expanded_task = expand_query(task)

    # ── Step 2: Detect user intent → category signals ──
    intent_scores = detect_intent(task)  # use raw task for intent, not expanded

    # ── Step 3: Build rich corpus per tool ──
    corpus = [
        " ".join([
            str(row.get("AI tool", "")),          # tool name exact match
            str(row.get("AI tool", "")),          # doubled for weight
            str(row.get("Category", "")),
            str(row.get("Best use", "")),
            str(row.get("Best use", "")),          # doubled for weight
            str(row.get("Useful student tasks", "")),
        ])
        for _, row in df.iterrows()
    ]

    # ── Step 4: TF-IDF on expanded query vs corpus ──
    tfidf_scores = tfidf_similarity(expanded_task, corpus)

    # ── Step 5: Keyword overlap on expanded query ──
    kw_scores = [keyword_match(expanded_task, c) for c in corpus]

    results = []

    for i, (_, tool) in enumerate(df.iterrows()):

        # Blend TF-IDF (65%) + keyword (35%)
        base_score = 0.65 * tfidf_scores[i] + 0.35 * kw_scores[i]

        # Intent / category boost
        tool_category = str(tool.get("Category", "")).strip()
        intent_boost  = intent_scores.get(tool_category, 0.0)

        # Skill match
        s_match = skill_match(str(tool.get("Skill level", "")), skill_level)

        # Free option bonus (small, tie-break only)
        free_bonus = (
            1.0 if str(tool.get("Free option", "")).lower().startswith("yes")
            else 0.0
        )

        # ── Final weighted score ──
        # base_score:    how well the tool text matches the query     60%
        # intent_boost:  does the tool category match detected intent 25%
        # s_match:       skill level alignment                        10%
        # free_bonus:    has a free plan                               5%
        final_score = (
            base_score   * 0.60
            + intent_boost * 0.25
            + s_match      * 0.10
            + free_bonus   * 0.05
        )

        reasons = generate_reason(tool, base_score, s_match, intent_boost)

        results.append({
            "tool":        str(tool.get("AI tool", "")),
            "category":    tool_category,
            "score":       round(final_score * 100),
            "reasons":     reasons,
            "best_use":    str(tool.get("Best use", "")),
            "free_option": str(tool.get("Free option", "")),
            "skill_level": str(tool.get("Skill level", "")),
            "url":         str(tool.get("URL", "")),
        })

    # Sort: highest score first, then alphabetically as tie-break
    results.sort(key=lambda x: (-x["score"], x["tool"]))

    return results[:top_n]


# --------------------------------------------------
# Comparison helper
# --------------------------------------------------

def compare_tools(tool_names: list) -> list:
    df   = load_tools()
    rows = df[df["AI tool"].isin(tool_names)]

    return [
        {
            "tool":        str(row.get("AI tool", "")),
            "category":    str(row.get("Category", "")),
            "best_use":    str(row.get("Best use", "")),
            "tasks":       str(row.get("Useful student tasks", "")),
            "free_option": str(row.get("Free option", "")),
            "skill_level": str(row.get("Skill level", "")),
            "url":         str(row.get("URL", "")),
        }
        for _, row in rows.iterrows()
    ]
