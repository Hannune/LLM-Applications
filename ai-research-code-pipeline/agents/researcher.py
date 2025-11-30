"""
Researcher Agent - Information Gathering using GPT Researcher

Conducts deep research on topics using GPT Researcher.
Works with OpenAI-compatible APIs (Ollama, vLLM, LiteLLM).
"""

import asyncio
import os
from gpt_researcher import GPTResearcher
from langchain_core.messages import AIMessage
from dotenv import load_dotenv

load_dotenv()

# Configure GPT Researcher with OpenAI-compatible endpoints
os.environ["FAST_LLM"] = os.getenv("RESEARCHER_FAST_LLM", "openai:gpt-4o-mini")
os.environ["SMART_LLM"] = os.getenv("RESEARCHER_SMART_LLM", "openai:gpt-4o-mini")
os.environ["STRATEGIC_LLM"] = os.getenv("RESEARCHER_STRATEGIC_LLM", "openai:gpt-4o-mini")
os.environ["EMBEDDING"] = os.getenv("RESEARCHER_EMBEDDING", "openai:text-embedding-3-small")

# Search API key (Tavily, SerpAPI, etc.)
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")


def run_researcher_sync(query: str, report_type: str = "research_report") -> str:
    """
    Run GPT Researcher synchronously.
    
    Args:
        query: Research query
        report_type: Type of report to generate
        
    Returns:
        Research report as string
    """
    async def async_research():
        researcher = GPTResearcher(query=query, report_type=report_type)
        await researcher.conduct_research()
        return await researcher.write_report()
    
    return asyncio.run(async_research())


def researcher_node(state):
    """
    Researcher node that conducts research.
    
    Args:
        state: Current conversation state with messages
        
    Returns:
        Updated state with research report
    """
    print("=== RESEARCHER ===")
    messages = state["messages"]
    last_message = messages[-1]
    
    # Extract query from supervisor's instructions
    import json
    try:
        supervisor_json = json.loads(last_message.content)
        query = supervisor_json.get("content", last_message.content)
    except:
        query = last_message.content
    
    print(f"Researching: {query}")
    result = run_researcher_sync(query)
    print(f"Research complete: {len(result)} characters")
    print("==================")
    
    return {"messages": [AIMessage(content=f"Research Report:\n{result}")]}
