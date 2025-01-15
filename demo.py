from langchain.chains import LLMChain
from langchain_community.chat_models import BedrockChat
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

def my_chatbot(language,freeform_text):
    prompt = PromptTemplate(
        input_variables=["language", "freeform_text"],
        template="You are a chatbot. You are in {language}.\n\n{freeform_text}"
    )

    bedrock_chain = LLMChain(llm=llm, prompt=prompt)

    response=bedrock_chain({'language':language, 'freeform_text':freeform_text})
    return response

#print(my_chatbot("english","who is buddha?"))

st.title("Bedrock Chatbot")

language = st.sidebar.selectbox("Language", ["english", "spanish"])

if language:
    freeform_text = st.sidebar.text_area(label="what is your question?",
    max_chars=100)

if freeform_text:
    response = my_chatbot(language,freeform_text)
    st.write(response['text'])