#Actionables, Decision, Questions

import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv
#core/extractor.py
import os

load_dotenv()

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"), temperature=0.2)

def build_chain(system_prompt: str):
    llm = get_llm()

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{text}"),

    ])

    return (RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | chat_prompt | llm | StrOutputParser())

def extract_action_items(transcript: str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst. From the meeting transcript, extract all Action items. For Each Provide: \n"
        "- Task: a clear description of the action required\n"
        "- Owner: who is responsible for this action\n"
        "- Due Date: deadline if mentioned else write 'Not specified'\n"
        "Priority: High, Medium, Low"
        "Format as a numbered list. If none found say 'No action items found.;"
    )

    return chain.invoke(transcript).strip()

def extract_key_decisions(transcript: str) -> str:
    chain = build_chain(
        "You are an expert meeting analyst. From the meeting transcript, extract all key decisions made. Format as a numbered list. If none found say 'No key decisions found."
    )

    return chain.invoke(transcript).strip()

def extract_questions(transcript: str) -> str:
    chain = build_chain(
        "From the meeting transcript, extract all unresolved questions or topics needing follow-up. Format as a numbered list. If none found say 'No open questions found.' "
        "Be very literal. Do not infer or guess."
    )

    return chain.invoke(transcript)
