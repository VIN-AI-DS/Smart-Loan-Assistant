import os
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.agents import load_tools, initialize_agent, AgentType
from pydantic import BaseModel, Field
from utils import get_groq_api_key, get_serper_api_key
from translate import translation
# Set up API keys
os.environ["SERPAPI_API_KEY"] = get_serper_api_key()

# Define a Pydantic model for structured output
class FinancialTipsResponse(BaseModel):
    tips: list[str] = Field(description="List of financial tips for all loans.")
    #sources: list[str] = Field(description="List of sources or references for the tips.")

# Custom prompt to guide the agent
custom_prompt = """
You are a financial advisor in loans. Your task is to provide actionable and accurate financial tips for loans. 
Use the following guidelines:
1. Use the Search tool to find the latest information on home loan tips from reputable sources.
2. Analyze the search results and extract the most relevant financial tips.
3. Provide at least 5 tips in a clear and concise format.
4. Your response should be informative and helpful to the user.
5. You can add respond with your own knowledge about financial tips for loans. only if you dont get any relevant information from the search tool.

Question: {input}
"""

# Initialize the Groq LLM
llm = ChatGroq(
    model="mixtral-8x7b-32768",
    api_key=get_groq_api_key(),
    temperature=0.7,
)

# Load tools (Serper API for web search)
tool_names = ["serpapi"]
tools = load_tools(tool_names, llm=llm, serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

# Initialize the agent with a custom prompt
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,  # Limit the number of iterations to prevent infinite loops
    early_stopping_method="generate",  # Stop if the agent generates a final answer
)

# Function to get financial tips
def get_financial_tips(query: str) -> FinancialTipsResponse:
    """
    Get financial tips for loans using the agent.
    """
    # Run the agent with the custom prompt
    response = agent.run(custom_prompt.format(input=query))
    return FinancialTipsResponse(tips=[response], sources=["Serper API"])

# Run the agent
query = translation
response = get_financial_tips(query)
print("Financial Tips:")
res_text = response.tips
print(res_text)