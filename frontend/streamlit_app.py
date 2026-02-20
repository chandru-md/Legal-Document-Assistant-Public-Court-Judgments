import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Legal RAG Assistant", page_icon="⚖️")

st.title("⚖️ Legal RAG Assistant")
st.markdown("Ask questions about constitutional court judgments.")

query = st.text_input("Enter your legal question:")

st.markdown("### Optional Filters")

case_id = st.text_input("Filter by Case ID (optional)")
category = st.selectbox("Category", ["All", "constitutional"])

if st.button("Ask"):

    if query.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing legal documents..."):

            payload = {
                "question": query,
                "case_id": case_id if case_id else None,
                "category": None if category == "All" else category
            }

            response = requests.post(
                API_URL,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()

                st.subheader("📖 Answer")
                st.write(data["answer"])

                st.subheader("📚 Sources")
                for source in data["sources"]:
                    st.write(f"- Case ID: {source}")

                st.subheader("📊 Evaluation Scores")
                st.json(data["evaluation"])

            else:
                st.error("Error connecting to backend.")