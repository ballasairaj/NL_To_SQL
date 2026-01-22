from sqlalchemy import text
from app.db.database import engine
import re

def clean_sql(sql: str) -> str:
    """
    Extract the first SELECT statement from LLM output.
    """
    # Remove code fences if present
    sql = sql.replace("```sql", "").replace("```", "").strip()

    # Find first SELECT statement
    match = re.search(r"(SELECT[\s\S]+)", sql, re.IGNORECASE)
    if not match:
        raise ValueError("No SELECT query found")

    clean_query = match.group(1).strip()

    # Remove trailing semicolons
    clean_query = clean_query.rstrip(";")

    return clean_query


def looks_unfiltered(query: str) -> bool:
    q = query.upper()
    return "WHERE" not in q and "COUNT" not in q and "SUM" not in q

def execute_sql(sql: str):
    query = clean_sql(sql)

    if not query.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries allowed")

    if looks_unfiltered(query):
        raise ValueError("Query too broad. Please refine your question.")

    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.mappings().all()
        return [dict(r) for r in rows]

