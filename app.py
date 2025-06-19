import streamlit as st
from query_engine import build_prompt, query_llm, run_sql
from utils import validate_question, load_metadata

st.title("🧠 Natural Language to SQL - Banking Data")

user_question = st.text_input("Ask a question about banking data:")

if st.button("Submit") and user_question:
    metadata = load_metadata()
    prompt = build_prompt(user_question)
    response = query_llm(prompt)
    response_list = response.split('</think>')
    query = response_list[1].strip() if response_list else response.strip()
    reasoning = response_list[0].strip()

    if "outside the scope" in response.lower():
        st.warning(response)
    else:
        st.write(reasoning)
        st.code(query, language='sql')
        try:
            results = run_sql(query)
            st.dataframe(results)
        except Exception as e:
            st.error(f"SQL execution error: {e}")
