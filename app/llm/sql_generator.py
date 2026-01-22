from app.llm.mistral_client import call_mistral

SCHEMA = """
students(
  student_id,
  student_name,
  roll_no,
  class,
  section,
  email,
  phone_number,
  category,
  total_fee,
  due_amount
)

payments(
  student_id,
  installment_no,
  installment_amount,
  due_date,
  paid,
  payment_date
)
"""

BUSINESS_RULES = """
Business Rules (MANDATORY):
- "pending" means paid = 0
- "paid" means paid = 1
- "1st installment" means installment_no = 1
- "2nd installment" means installment_no = 2
- Fee due means paid = 0 AND due_date < CURRENT_DATE
- Student-related queries MUST JOIN students and payments ON student_id
"""

EXAMPLES = """
Examples:

Q: list students pending first installment
SQL:
SELECT s.student_id, s.student_name, p.installment_amount
FROM students s
JOIN payments p ON s.student_id = p.student_id
WHERE p.installment_no = 1 AND p.paid = 0;

Q: students who paid second installment
SQL:
SELECT s.student_name
FROM students s
JOIN payments p ON s.student_id = p.student_id
WHERE p.installment_no = 2 AND p.paid = 1;
"""

def generate_sql(question: str):
    prompt = f"""
You are an expert SQLite SQL generator for a School ERP.

{SCHEMA}

{BUSINESS_RULES}

{EXAMPLES}

Rules:
- Output ONLY ONE SQL SELECT query
- NEVER return all rows unless explicitly asked
- ALWAYS use WHERE clause if filtering is implied
- NO explanation, SQL only

Question:
{question}
"""
    return call_mistral(prompt)

