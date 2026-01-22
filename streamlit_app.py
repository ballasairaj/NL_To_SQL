import streamlit as st
from app.db.loader import load_excel_to_db
from app.agents.admin_agent import admin_agent
from app.agents.fee_agent import fee_agent
from app.agents.payroll_agent import payroll_agent
from app.agents.llm_router import route_query_with_llm

st.set_page_config("AI ERP Assistant", layout="wide")
st.title("AI ERP Assistant (LLM-based Routing)")

uploaded_file = st.file_uploader("Upload ERP Excel File", type=["xlsx"])

if uploaded_file:
    load_excel_to_db(uploaded_file)
    st.success("Excel data loaded successfully")

query = st.text_input("Ask your question")

if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question")
    else:
        
        intent = route_query_with_llm(query)
        print(f"Routed intent: {intent}")

        if intent == "fee":
            result = fee_agent(query)
            agent_used = "Fee Intelligence Agent"

        elif intent == "payroll":
            result = payroll_agent(query)
            agent_used = "Payroll Agent"

        elif intent == "admin":
            result = admin_agent(query)
            agent_used = "Admin Query Agent"

        else:
            raise ValueError("Unable to determine agent")
        

        st.caption(f"Agent used: {agent_used}")
        st.subheader("Answer (From Database)")
        st.json(result)

        # except Exception as e:
        #     st.error(str(e))
