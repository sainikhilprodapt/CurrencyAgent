# agent.py - LangChain Agent Implementation

import os
from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool

# Load environment variables
load_dotenv()

def create_currency_agent():
    """Create and return the currency converter and news agent executor."""
    
    # Configure LLM
    llm = ChatGoogleGenerativeAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="gemini-1.5-pro",
        temperature=0,
    )

    # Configure tools
    tools = [
        TavilySearchResults(
            api_key=os.getenv("TAVILY_API_KEY"),
            max_results=5
        ),
        PythonREPLTool()
    ]

    # Define the agent prompt
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessage(content=(
    "You are a Currency Information Assistant specialized in providing current exchange rates and related news."
    "When given a currency pair:"
    "1. First use the Tavily search tool to fetch the current exchange rate from the web on the current day for the specified currency pair"
    "2. Use PythonREPLTool for any calculations or data processing needed on the exchange rate information"
    "3. Then use the Tavily search tool again to find 3-4 recent news articles related to the specified currencies and market trends"
    "4. Present both the exchange rate, any calculated values, and news articles in a clear, organized markdown format"
    "\n\n"
    "FORMAT YOUR RESPONSE IN STRUCTURED MARKDOWN with the following sections:"
    "- A heading with the currency pair"
    "- A section showing the current exchange rate with the date"
    "- A bulleted list of recent news articles with the following format for each article:"
    "  * **[Headline as a link to the article]** - _Source name_ - A 1-2 sentence summary of the article"
    "- Any additional calculated information in a formatted table if applicable"
    "\n\n"
    "IMPORTANT: When mentioning 'today' or 'current date' in your response, always display the date as February 12, 2025."
    "\n\n"
    "You should not make assumptions about exchange rates or news - always use the Tavily search tool to retrieve current information."
    "Process requests sequentially, not in parallel, to ensure accuracy."
    "When searching for exchange rates, construct the appropriate URL for xe.com based on the currency pair provided."
    "For news, focus on recent financial news related to the specified currencies."
    "Use PythonREPLTool for any numerical operations, such as converting amounts between currencies or calculating percentage changes."
            )),
            HumanMessagePromptTemplate.from_template("{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    # Create the agent
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        verbose=True,
        max_iterations=20,
        tools=tools,
    )
    
    return agent_executor

def get_currency_info(agent_executor, from_currency, to_currency):
    """
    Get currency conversion and news using the agent.
    
    Args:
        agent_executor: The LangChain agent executor
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'INR')
        
    Returns:
        str: Markdown formatted result with exchange rate and news
    """
    # Format the query for the agent
    query = f"Convert {from_currency} to {to_currency}"
    
    # Execute the agent
    response = agent_executor.invoke({"input": query})
    return response["output"]

# For testing the agent directly
if __name__ == "__main__":
    agent = create_currency_agent()
    result = get_currency_info(agent, "USD", "EUR")
    print(result)