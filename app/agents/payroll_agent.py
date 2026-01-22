from app.llm.sql_generator import generate_sql
from app.db.executor import execute_sql

SCHEMA = """
payroll(employee_id, employee_name, designation, department, gross_salary, leaves_taken, deductions, net_salary)
"""

def payroll_agent(question: str):
    sql = generate_sql(question, SCHEMA)
    return execute_sql(sql)
