import json
import os
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from utils import get_groq_api_key, get_sarvam_api_key
from tts import financial_tips_agent
from translate import translation
from translate3 import native_support
from tts1 import native_audio
from translate3 import native_support
import wave
import requests
import base64

# Initialize HuggingFace embeddings
model_name = "sentence-transformers/all-mpnet-base-v2"
hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={'device': 'cpu'}, encode_kwargs={'normalize_embeddings': False})

# Extract text from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    pdf = PdfReader(pdf_path)
    return "".join(page.extract_text() or "" for page in pdf.pages)

# Split text into chunks
def split_text(raw_text: str):
    model = SentenceTransformer(model_name)
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n#{1,6}", "'''\n", "\n\*\*\*+\n", "\n---+\n", "\n___+\n", "\n\n", "\n", " ", ""],
        chunk_size=model.max_seq_length,
        chunk_overlap=150,
        add_start_index=True,
        strip_whitespace=True,
    )
    return text_splitter.split_text(raw_text)

# Create FAISS vector store
def create_vectorstore(texts):
    return FAISS.from_texts(texts, embedding=hf)

# Define state for the agent
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

MISSION_CONTROL_PROMPT = """
You are a mission controller, responsible for analyzing user input and determining the correct intent.
Your only task is to classify the query into one of the following categories:

1. **Loan Eligibility check(loan_eligibility)**: 
    -If the user is seeking information about loans.
    -Examples:
        - "Am I eligible for a home loan?"
        - "What are the eligibility criteria for a personal loan?"
        - "Can I get a car loan with my credit score?"

2. **Financial Tips(financial_tips)**:
    -If the user is looking for financial advice or tips.
    -Examples:
        - "What are some tips for managing personal finances?"
        - "How can I save money on groceries?"
        - "What are the best investment strategies for beginners?"

4. **Unknown(unknown)**:
    -If the query does not fit into any of the above categories.
    -Examples:
        - "What is the capital of France?"
        - "How many planets are there in the solar system?"
        - "Who is the author of Harry Potter?"

**Important Guidelines**:
-**Only classify the query into one of the above categories.**
-**Do not provide detailed answers or explanations.**
-**If unsure, classify the query as 'Unknown'.**
-**Your output must follow this format:**
json
{
    "intent": "<one of the labels>",
    "query": "<user query>",
    "confidence": "<confidence score>"
}
"""
# Initialize LLM
llm = ChatGroq(model="mixtral-8x7b-32768", api_key=get_groq_api_key(), temperature=0.5)

class Decision(BaseModel):
    intent: str
    query: str
    confidence: float

structured_llm = llm.with_structured_output(Decision)

def mission_control_agent(state: State):
    messages = [
        SystemMessage(content=MISSION_CONTROL_PROMPT),
        HumanMessage(content=state["messages"][-1].content)
    ]
    output = structured_llm.invoke(messages)
    return {"messages": [AIMessage(content=json.dumps(output.model_dump()))]}

graph_builder.add_node("mission_control", mission_control_agent)

ROUTE_MAP = {
    "loan_eligibility": "loan_eligibility_agent",
    "financial_tips": "financial_tips_agent",
    "unknown": "unknown_agent"
}

def router(state: State):
    mission_control_output = json.loads(state["messages"][-1].content)
    intent = mission_control_output.get("intent", "unknown")
    return {"next_agent": ROUTE_MAP.get(intent, "unknown_agent")}

graph_builder.add_node("router", router)
graph_builder.add_edge("mission_control", "router")

def get_next_agent(state):
    return state["next_agent"]

graph_builder.add_conditional_edges(
    "router", get_next_agent,
    {
        "loan_eligibility_agent": "loan_eligibility_agent",
        "financial_tips_agent": "financial_tips_agent",
        "unknown_agent": "unknown_agent",
        END: END
    }
)

def loan_eligibility_agent(state: State):
    try:
        intent_data = json.loads(state["messages"][-1].content)
        query = intent_data.get("query", "no query found")

        llm = ChatGroq(model="mixtral-8x7b-32768", api_key=get_groq_api_key(), temperature=0.5)
        chain = load_qa_chain(llm=llm, chain_type="stuff")

        pdf_path = "C:\\Users\\arun5\\Desktop\\TGBH-HACK\\RAG\\pdfs\\ICICI\\ICICI BANK LOAN INFORMATION(1).pdf"
        raw_text = extract_text_from_pdf(pdf_path)
        texts = split_text(raw_text)
        doc_search = create_vectorstore(texts)

        docs = doc_search.similarity_search(query)
        response_text = "No relevant details found." if not docs else chain.invoke({
            "input_documents": docs,
            "question": query,
            "system_message": "Provide only key eligibility details in simple bullet points without extra explanations."
        })['output_text']

        return {"messages": [AIMessage(content=f"Loan Eligibility Agent Response:\nQuery: {query}\n\n{response_text}")]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Error: {str(e)}")]}



def unknown_agent(state: State):
  """A simple unknown agent"""
  intent_data = json.loads(state["messages"][-1].content)
  print("intent",intent_data)
  query = intent_data.get("query", "no query found")
  confidence = intent_data.get("confidence", 0.0)
  return {"messages": [AIMessage(content=f"Sorry, I can only help you with Loan_eligibility queries, financial_tips related queries. Query: {query}, Confidence: {confidence}")]}

graph_builder.add_node("loan_eligibility_agent", loan_eligibility_agent)
graph_builder.add_node("unknown_agent", unknown_agent)
graph_builder.add_edge("loan_eligibility_agent", END)
graph_builder.add_edge("unknown_agent", END)
graph_builder.add_node("financial_tips_agent", financial_tips_agent)
graph_builder.add_edge("financial_tips_agent", END)


graph_builder.set_entry_point("mission_control")
graph = graph_builder.compile()

state = {"messages": [HumanMessage(content=translation)]}  # Sample input
result = graph.invoke(state)
final_res = result["messages"][-1].content
native_lang = native_support(final_res)
translated_lst = ""
for i in native_lang:
    translated_lst += (str(i) + "\n")


native_audio(translated_lst)