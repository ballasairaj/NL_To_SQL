from app.llm.sql_generator import generate_sql
from app.db.executor import execute_sql

def admin_agent(question: str):
    sql = generate_sql(question)
    return execute_sql(sql)

