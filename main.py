import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
from faq import faq_chain, ingest_faq_data
from sql import sql_chain
from router import router 

st.set_page_config(page_title="E-Commerce Chatbot", page_icon=":guardsman:", layout="wide")
st.title("E-Commerce Chatbot")


ingest_faq_data("faq_data.csv")


# Initialize session state for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
query = st.chat_input("Ask a question about products or FAQs...")

# Process user query
if query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    # Route the query
    route_result = router(query)
    print(f"Router result for '{query}': {route_result.name if route_result else 'No route found'}")

    response = ""
    if route_result and route_result.name == "faq":
        response = faq_chain(query)
    elif route_result and route_result.name == "sql":
        response = sql_chain(query)
    else:
        response = "Sorry, I did not understand your question. Please try rephrasing your question or ask about product information or FAQs."

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
