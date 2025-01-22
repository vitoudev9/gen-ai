from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_aws import ChatBedrock
import boto3
import os
import streamlit as st

# install langchain, langchain_aws, boto3, streamlit
# configure AWS_Profile and check credential in console


os.environ['AWS_PROFILE'] = 'auralis'

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2"
)

modelID = "anthropic.claude-3-haiku-20240307-v1:0"


llm = ChatBedrock(
    model_id=modelID,
    client=bedrock_client,
    ##model_kwargs={"max_tokens_to_sample": 2000,"temperature":0.9}
)

memory = ConversationBufferMemory(memory_key="chat_history")

def my_chatbot():

    st.title("Auralis Chatbot")

    prompt = PromptTemplate(
        input_variables=["chat_history", "text_input"],
        template = """
        The following is a friendly conversation between a user and an AI assistant. The assistant remembers past interactions and provides helpful responses.

        Chat History:
        {chat_history}

        User: {text_input}
        AI:
        """
        #template="You are a chatbot. You are in {language}.\n\n{freeform_text}"
    )

    bedrock_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

    # Session state to store conversation history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    #if prompt := st.chat_input():
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

    input_text = st.chat_input("Type Hi to start the conversion")

    if (input_text):
        with st.chat_message("user"):
            st.markdown(input_text)
        st.session_state.chat_history.append({"role":"user", "text":input_text })

        chat_response = bedrock_chain.run({"text_input": input_text})
        with st.chat_message("assistant"):
            st.markdown(chat_response)
        st.session_state.chat_history.append({"role":"assistant", "text":chat_response })

my_chatbot()







