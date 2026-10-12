from langchain_core.messages import HumanMessage
from langchain_core import messages
import streamlit as st
from langgraph_backend import app
# st.session_state = {} dict is used to store data in session
# for maintaining state of the application
# if data is not found in st.session_state then it will create a new session
config = {'configurable':{"thread_id":"thread-1"}}
if 'messageHistory' not in st.session_state:
    st.session_state['messageHistory'] = []


for message in st.session_state['messageHistory']:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type here.....")

if user_input:
    st.session_state['messageHistory'].append({"role":"user", "content":user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = app.invoke({'message':[HumanMessage(content=user_input)]} ,config = config)
    ai_message = response['message'][-1].content
    st.session_state['messageHistory'].append({"role":"AI","content":ai_message})
    with st.chat_message('AI'):
        st.text(ai_message)
