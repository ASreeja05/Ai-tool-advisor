# AI Tool Advisor

> **A context-aware recommendation system that helps students identify suitable AI tools for their specific tasks, skill level, context, and required output.**

## Overview

Students have access to a growing number of AI tools for writing, coding, presentations, research, design, data analysis, studying, and productivity. However, choosing the right tool for a particular task can be difficult.

**AI Tool Advisor** treats AI-tool selection as a recommendation problem. The user provides a task, context, skill level, and required output, and the system compares these requirements with a structured AI-tool knowledge base to generate relevant recommendations.

### Core Workflow

```text
User Task
    ↓
Task + Context + Skill Level + Required Output
    ↓
AI Tool Knowledge Base (tools.csv)
    ↓
Recommendation & Scoring Engine
    ↓
Ranked AI Tool Recommendations
    ↓
Match Score + Explanation
```

This is a **standalone personal project** focused on practical and explainable AI-tool recommendation for students.

---

## Problem Statement

The rapid growth of generative AI has created a large ecosystem of tools with overlapping capabilities. Students may struggle with:

1. **Tool overload** — many tools are available for similar tasks.
2. **Context mismatch** — a tool suitable for one task may not be suitable for another.
3. **Lack of explainability** — recommendation lists often do not explain why a tool is appropriate.

The objective of this project is to build a simple, context-aware recommendation system that maps a student's current requirement to suitable AI tools rather than presenting a generic list.

---

## Key Features

- **Task-based recommendations** driven by the user's goal.
- **Context-aware matching** for academic or project requirements.
- **Skill-level awareness** to consider user experience.
- **Output-aware matching** based on the desired result.
- **Ranked recommendations** using compatibility scores.
- **Explainable recommendations** with a reason for each suggestion.
- **Structured tool knowledge base** maintained in `tools.csv`.
- **Interactive web interface** built with Streamlit.

---

## Dataset / Knowledge Base

The project uses:

```text
tools.csv
```

This is a **curated AI-tool knowledge base**, rather than a traditional machine-learning training dataset.

The file stores structured information used by the recommendation engine to compare a user's requirements with available AI tools.

This approach makes the system easy to extend: new tools and metadata can be added to the knowledge base without retraining a machine-learning model.

> **Current limitation:** the prototype does not claim a statistically benchmarked recommendation-accuracy score. Recommendation quality depends on the completeness and quality of the curated knowledge base and scoring logic.

---

## Tools & Technologies

| Technology | Purpose |
|---|---|
| **Python** | Core application and recommendation logic |
| **Streamlit** | Interactive web application |
| **Pandas** | Structured CSV/data handling |
| **CSV** | AI-tool knowledge base |
| **Rule/Score-based Recommendation** | Requirement-to-tool matching |

### Project Structure

```text
Ai-tool-advisor/
│
├── app.py                # Streamlit application and UI
├── recommender.py        # Recommendation and scoring logic
├── tool_categories.py    # Tool category definitions/logic
├── tools.csv             # Curated AI-tool knowledge base
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Methodology

The recommendation pipeline follows a context-aware scoring approach.

### 1. User Input

The application collects:

- Task
- Context
- Skill level
- Required output

Example:

```text
Task: Create a presentation
Context: DBMS project
Skill Level: Beginner
Output: PPT
```

### 2. Requirement Representation

The input is interpreted as a set of requirements describing what the student needs.

### 3. Tool Matching

The recommendation engine compares these requirements with the metadata available for each tool in `tools.csv`.

Relevant factors include the matching criteria implemented by the current recommendation engine, such as task/category compatibility, context suitability, skill-level suitability, and output compatibility.

### 4. Scoring

A compatibility score is calculated for candidate tools based on the implemented matching criteria.

### 5. Ranking

Candidate tools are ranked according to their calculated compatibility.

### 6. Explanation

The application presents the recommendation together with an explanation of why the tool matches the user's requirements.

This makes the system more interpretable than simply displaying a list of AI tools.

---

## Example

### Input

```text
Task: Create a presentation for my DBMS
Context: DBMS project
Skill Level: Beginner
Required Output: PPT
```

### Output

The application generates a ranked list of suitable AI tools containing:

- Tool name
- Match score
- Recommendation explanation

The exact recommendations depend on the current contents of `tools.csv` and the scoring logic.

---

## Application Output

The Streamlit interface provides an interactive recommendation workflow:

```text
┌──────────────────────────────────────────────┐
│         AI Tool Advisor            │
├──────────────────────────────────────────────┤
│ Task:            [.........................]  │
│ Context:         [.........................]  │
│ Skill Level:     [ Beginner ▼ ]              │
│ Required Output: [ PPT ▼ ]                   │
│                                              │
│          [ Find Best AI Tools ]              │
├──────────────────────────────────────────────┤
│ Recommended Tools                            │
│                                              │
│ Tool A                         92%            │
│ Why this tool? ...                           │
│                                              │
│ Tool B                         86%            │
│ Why this tool? ...                           │
└──────────────────────────────────────────────┘
```

The actual recommendations and scores are generated dynamically by the application.

---

## How to Run the Project

### Prerequisites

Install Python and verify it with:

```bash
python --version
```

On Windows, you can also use:

```bash
py --version
```

### 1. Clone the Repository

```bash
git clone https://github.com/ASreeja05/Ai-tool-advisor.git
cd Ai-tool-advisor
```

### 2. Install Dependencies

On Windows:

```bash
py -m pip install -r requirements.txt
```

Alternatively:

```bash
python -m pip install -r requirements.txt
```

### 3. Run the Streamlit Application

```bash
py -m streamlit run app.py
```

or:

```bash
python -m streamlit run app.py
```

### 4. Open the Application

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open the displayed address in your browser.

---

## Results

The current prototype provides an interactive workflow for recommending AI tools based on multiple user-provided requirements.

The main output is a **ranked and explainable recommendation** rather than a generic AI-tool directory.

The prototype demonstrates how structured tool metadata and contextual scoring can be used to simplify AI-tool selection for students.

---

## Limitations

- The tool knowledge base is manually curated.
- Recommendations depend on the quality and completeness of `tools.csv`.
- The current scoring approach is not trained on a large user-feedback dataset.
- The project does not currently claim benchmarked recommendation accuracy.
- AI-tool capabilities, pricing, and availability can change over time.

---

## Future Work

### 1. Personalized Recommendations
Integrate student profiles, interests, goals, skills, and previous tool usage.

### 2. Semantic Matching
Use embeddings or semantic similarity so the system can understand natural-language tasks beyond exact keyword matching.

### 3. Feedback-Based Learning
Allow users to rate recommendations and use feedback to improve future recommendations.

### 4. Dynamic Tool Knowledge Base
Periodically update information about AI tools, capabilities, pricing, and availability.

### 5. Advanced Explainability
Show which requirements contributed to a recommendation score.

### 6. Integration
Connect the advisor with academic context, skill progress, projects, and student goals for more personalized recommendations.

### 7. Deployment
Deploy the application as a publicly accessible web application so users can interact with it without local setup.

---

## Conclusion

**AI Tool Advisor** explores a practical approach to AI-tool discovery by combining task requirements, user context, skill level, and desired output.

Instead of asking students to search through a large collection of AI tools, the system narrows the options to tools relevant to their current requirement and explains the basis of the recommendation.

The project provides a foundation for a more personalized and intelligent AI-tool discovery system for students.

---

## Author and contact

**Sreeja Akshanthala**
Email:-akshanthalasreeja@gmail.com

A project focused on AI-assisted student productivity and context-aware recommendation systems.

---

## License

This project currently does not specify an open-source license.
