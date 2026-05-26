import os

from dotenv import load_dotenv

from langchain_chroma import Chroma

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_core.documents import Document

from langchain_mistralai import ChatMistralAI

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.output_parsers import (
    StrOutputParser
)


load_dotenv()


CHROMA_DIR = "vector_db"

# EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# =========================
# Embeddings
# =========================
def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"}
    )


# =========================
# LLM
# =========================
def get_llm():

    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv(
            "MISTRAL_API_KEY"
        ),
        temperature=0.3
    )


# =========================
# Build Vector Store
# =========================
def build_vector_store(
    meeting_id: int,
    transcript: str
):

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=300
        )
    )

    chunks = splitter.split_text(
        transcript
    )

    docs = [
        Document(
            page_content=chunk,
            metadata={
                "meeting_id": meeting_id
            }
        )
        for chunk in chunks
    ]

    embeddings = get_embeddings()

    persist_dir = (
        f"{CHROMA_DIR}/meeting_{meeting_id}"
    )

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    return vector_store


# =========================
# Load Vector Store
# =========================
def load_vector_store(
    meeting_id: int
):

    embeddings = get_embeddings()

    persist_dir = (
        f"{CHROMA_DIR}/meeting_{meeting_id}"
    )

    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )


# =========================
# Ask Question
# =========================
def ask_question(meeting_id: int, question: str):

    vector_store = load_vector_store(
        meeting_id
    )

    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 6,
        "fetch_k": 20
    }
    )

    # Rewrite query
    rewritten_query = rewrite_query(
        question
    )

    print(
        f"Original Query: {question}"
    )

    print(
        f"Rewritten Query: {rewritten_query}"
    )

    # Retrieve documents
    docs = retriever.invoke(
        rewritten_query
    )

    context = "\n\n".join([
        doc.page_content
        for doc in docs
    ])

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an intelligent AI meeting assistant.

            Answer the user's question ONLY using the meeting transcript context.

            If the exact answer is not explicitly written,
            infer carefully from nearby context.

            Keep answers concise and accurate.

            If answer truly does not exist, say:
            "I could not find this information in the meeting."

            Context:
            {context}
            """
        ),
        (
            "human",
            "{question}"
        )
    ])

    llm = get_llm()

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke({
        "context": context,
        "question": question
    })

    return {
    "rewritten_query": rewritten_query,
    "answer": response
    }

# =========================
# Rewrite User Query
# =========================
def rewrite_query(
    question: str
):

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert AI retrieval query rewriter.

        Rewrite the user's question into the
        BEST possible semantic search query
        for retrieving information from a transcript.

        Important:
        - Preserve original meaning carefully
        - Fix grammar mistakes
        - Make vague questions explicit
        - Prefer concrete entities, places, events, and actions
        - Do NOT change intent unnecessarily
        - Keep query concise

        Examples:

        User:
        "When she suffered heartbreak?"

        Better Query:
        "Where did she suffer heartbreak?"

        User:
        "where she born?"

        Better Query:
        "Where was she born?"

        Return ONLY the rewritten query.
        """
    ),
    (
        "human",
        "{question}"
    )
])

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    rewritten_query = chain.invoke({
        "question": question
    })

    return rewritten_query.strip()