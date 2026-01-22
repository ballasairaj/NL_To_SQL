from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3
import streamlit as st
# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage
from mistralai import Mistral

# ============================
# MISTRAL CONFIGURATION
# ============================
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)


# ============================
# DATABASE SETUP
# ============================
def setup_database(db_name="student.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS STUDENT(
        NAME VARCHAR(25),
        CLASS VARCHAR(25),
        SECTION VARCHAR(25),
        MARKS INT
    );
    """)

    # Insert records only if table is empty
    cursor.execute("SELECT COUNT(*) FROM STUDENT")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO STUDENT VALUES (?,?,?,?)",
            [
                ('Krish', 'Data Science', 'A', 90),
                ('Sudhanshu', 'Data Science', 'B', 100),
                ('Darius', 'Data Science', 'A', 86),
                ('Vikash', 'DEVOPS', 'A', 50),
                ('Dipesh', 'DEVOPS', 'A', 35)
            ]
        )

    conn.commit()
    conn.close()

# ============================
# MISTRAL → SQL FUNCTION
# ============================
def get_mistral_sql(question, prompt):
    response = client.chat.complete(
        model="mistral-large-2512",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


# ============================
# SQL EXECUTION FUNCTION
# ============================
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# ============================
# PROMPT
# ============================
PROMPT = """
You are an expert in converting English questions into SQL queries.

The SQLite database is named STUDENT and has the following columns:
NAME, CLASS, SECTION, MARKS

Rules:
- Return ONLY the SQL query
- Do NOT use ``` or the word SQL
- Use correct SQLite syntax

Examples:
Question: How many students are there?
Answer: SELECT COUNT(*) FROM STUDENT;

Question: Show all Data Science students
Answer: SELECT * FROM STUDENT WHERE CLASS = "Data Science";
"""

# ============================
# STREAMLIT APP
# ============================
st.set_page_config(page_title="Mistral Text-to-SQL App")
st.header("Mistral AI – Text to SQL (Student DB)")

# Ensure DB is ready
setup_database()

question = st.text_input("Ask a question about the STUDENT database")

if st.button("Run Query"):
    if question.strip():
        try:
            sql_query = get_mistral_sql(question, PROMPT)
            st.subheader("Generated SQL Query")
            st.code(sql_query)

            result = read_sql_query(sql_query, "student.db")

            st.subheader("Query Result")
            if result:
                for row in result:
                    st.write(row)
            else:
                st.info("No records found.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")
