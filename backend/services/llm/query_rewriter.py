from .client import llm_rewriter

def rewrite_query(question: str) -> str:

    prompt = f"""You are improving search queries for a software repository.
    Convert the user question into keywords that match:
- filenames
- functions
- classes
- APIs
- code examples
- documentation sections

Examples:

Question:
How do I create an API endpoint?

Better search:
FastAPI route decorator app.get app.post path operation example


Question:
Where is authentication implemented?

Better search:
JWT OAuth2 security middleware authentication dependencies


Question:
How are database models created?

Better search:
SQLAlchemy models Base declarative class database schema


Question:
{question}

Output only the search keywords:
"""
    response = llm_rewriter(prompt)

    return response.strip()