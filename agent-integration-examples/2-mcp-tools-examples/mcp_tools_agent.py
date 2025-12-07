"""
MCP Tools Integration Example
Using LOCAL LLM services as tools for agents
"""

import requests
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain_ollama import ChatOllama


# Initialize LOCAL LLM
llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434"
)


@tool
def gdelt_news_search(query: str) -> str:
    """Search GDELT for news articles about a topic"""
    try:
        response = requests.post(
            "http://localhost:8004/search",
            json={
                "keywords": [query],
                "timespan": "7d",
                "max_results": 5
            },
            timeout=30
        )
        
        data = response.json()
        if data["success"]:
            articles = data["articles"][:3]
            result = f"Found {data['count']} articles. Top 3:\n\n"
            for i, art in enumerate(articles, 1):
                result += f"{i}. {art.get('title')}\n   {art.get('url')}\n\n"
            return result
        return "No articles found"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def n8n_research_workflow(topic: str) -> str:
    """Trigger n8n research workflow for in-depth analysis"""
    try:
        response = requests.post(
            "http://localhost:8005/agent/task",
            json={
                "agent_type": "researcher",
                "task": f"Research {topic}",
                "context": {"depth": "detailed"}
            },
            timeout=60
        )
        
        data = response.json()
        return str(data.get("response", "Research completed"))
    except Exception as e:
        return f"Error: {str(e)}"


# Create agent with tools
tools = [gdelt_news_search, n8n_research_workflow]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


# Example usage
if __name__ == "__main__":
    queries = [
        "What's the latest news about AI?",
        "Research quantum computing developments"
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}\n")
        
        result = agent.run(query)
        print(f"\nResult: {result}")
