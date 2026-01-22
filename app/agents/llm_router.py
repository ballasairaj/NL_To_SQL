from app.llm.mistral_client import call_mistral

def route_query_with_llm(user_query: str) -> str:
    prompt = f"""
You are an expert in converting english questions to the SQL query!
And also you are an intent classifier for a School ERP system.

Your task:
Classify the user query into ONE of the following categories:

- fee       → student fees, installments, due amounts, payments
- payroll   → staff salary, payroll, deductions, leaves
- admin     → totals, summaries, analytics, comparisons

Rules (STRICT):
- Output ONLY one word: fee OR payroll OR admin
- Do NOT explain
- Do NOT add punctuation
- Do NOT add extra text

User query:
{user_query}
"""
    response = call_mistral(prompt)
    return response.strip().lower()
