#core/Summarize.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

import os
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3
    )


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200,
    )

    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:

    llm = get_llm()

    map_prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize this portion of a meeting transcript concisely."),
        ("human", "{text}")
    ])

    map_chain = map_prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunk_summaries = [
        map_chain.invoke({"text": chunk})
        for chunk in chunks
    ]

    combined = "\n\n".join(chunk_summaries)

    combine_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert meeting summarizer. "
            "Combine these partial summaries into one professional "
            "meeting summary in bullet points."
        ),
        ("human", "{text}")
    ])

    combine_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | combine_prompt
        | llm
        | StrOutputParser()
    )

    return combine_chain.invoke(combined)


def generate_title(transcript: str) -> str:

    llm = get_llm()

    title_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Generate a concise professional meeting title "
            "(max 8 words). Only return the title."
        ),
        ("human", "{transcript}")
    ])

    title_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"transcript": x})
        | title_prompt
        | llm
        | StrOutputParser()
    )

    return title_chain.invoke(transcript).strip()