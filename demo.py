from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import boto3
import os
import streamlit as st

os.environ['AWS_PROFILE'] = 'auralis'

bedrock_client = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name="us-west-2"
)

modelID = "anthropic.claude-3-haiku-20240307-v1:0"
agentAliasID = "GM7PZJG8MI"
agentID = "4BNFDCQ7NJ"
sessionID = "2dd318f3-54d9-48c7-8b72-022759e6a79b"

memory = ConversationBufferMemory(memory_key="chat_history")

def my_chatbot():

    st.title("Auralis Chatbot")

    # Session state to store conversation history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

    input_text = st.chat_input("Type Hi to start the conversion")

    if (input_text):
        with st.chat_message("user"):
            st.markdown(input_text)
        st.session_state.chat_history.append({"role":"user", "text":input_text })

        print("sessionId= " + sessionID)
        response = bedrock_client.invoke_agent(
            enableTrace=True,
            sessionId=sessionID,
            agentAliasId=agentAliasID,
            agentId=agentID,
            inputText=input_text
        )

        chat_response = process_response(response)

        with st.chat_message("assistant"):
            st.markdown(chat_response)
        st.session_state.chat_history.append({"role":"assistant", "text":chat_response })
        print(chat_response)


def process_response(response):
    completion = ''
    for event in response.get('completion'):
        if 'chunk' in event:
            chunk = event["chunk"]
            #print('\n- chunk', chunk)
            completion = completion + chunk["bytes"].decode()
        
        elif 'trace' in event:
            trace = event["trace"]
            #print('\n- trace', trace)

    return completion

my_chatbot()







