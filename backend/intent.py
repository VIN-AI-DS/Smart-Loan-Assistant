from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel
import json
import os
from utils import get_groq_api_key
from tts import financial_tips_agent
from translate import translation
from rag import loan_eligibility_agent


class State(TypedDict):
    """
    State for the agent.
    """
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
3. **Loan application Guidance(loan_application)**:
    -If the user is seeking information about the loan application process.
    -Examples:
        - "How do I apply for a home loan?"
        - "What documents are required for a personal loan application?"
        - "Can I apply for a loan online?"

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
```json
{
    "intent": "<one of the labels>",
    "query": "<user query>",
    "confidence": "<confidence score>"
}
"""
llm = ChatGroq(
  model="mixtral-8x7b-32768",
  api_key=get_groq_api_key(),
  temperature=0.5,
)

class Decision(BaseModel):
  intent: str
  query: str
  confidence: float

structured_llm = llm.with_structured_output(Decision)

def mission_control_agent(state: State):
  """Extracts intent from user input using a structured prompt and returns parsed JSON as an AIMessage.
  """
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
  """Routes the user query to the appropriate functions based on Mission control's classification"""
  mission_control_output = json.loads(state["messages"][-1].content)
  intent = mission_control_output.get("intent", "unknown")
  query = mission_control_output.get("query", "No context found")
  confidence = mission_control_output.get("confidence", 0.0)

  return {
      "next_agent": ROUTE_MAP.get(intent, "unknown_agent"),
      "query": query,
      "confidence": confidence
  }

graph_builder.add_node("router", router)

graph_builder.add_edge("mission_control", "router")

def get_next_agent(state):
  return state["next_agent"]

graph_builder.add_conditional_edges(
  "router",
  get_next_agent,
  {
  "loan_eligibility_agent": "loan_eligibility_agent",
  "financial_tips_agent": "financial_tips_agent",
  "unknown_agent": "unknown_agent",
  END: END
  }
)

def unknown_agent(state: State):
  """A simple unknown agent"""
  intent_data = json.loads(state["messages"][-1].content)
  print("intent",intent_data)
  query = intent_data.get("query", "no query found")
  confidence = intent_data.get("confidence", 0.0)
  return {"messages": [AIMessage(content=f"Sorry, I can only help you with Loan_eligibility queries, financial_tips related queries. Query: {query}, Confidence: {confidence}")]}



graph_builder.add_node("loan_eligibility_agent", loan_eligibility_agent)
graph_builder.add_node("financial_tips_agent", financial_tips_agent)
graph_builder.add_node("unknown_agent", unknown_agent)

graph_builder.add_edge("loan_eligibility_agent", END)
graph_builder.add_edge("financial_tips_agent", END)
graph_builder.add_edge("unknown_agent", END)

graph_builder.set_entry_point("mission_control")

graph = graph_builder.compile()

translation_output = type(translation)
print(translation_output)
if isinstance(translation_output, dict):
    translation_output = translation_output.get("text", "No translation found")

state = {"messages": [HumanMessage(content=str(translation_output))]}
result = graph.invoke(state)
print(result["messages"][-1].content)