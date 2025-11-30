"""
AI Research-Code Pipeline - Main Orchestrator

Autonomous pipeline: Idea → Research → Code → Validate
Works with OpenAI-compatible APIs (Ollama, vLLM, LiteLLM).
"""

import os
import json
from typing import Annotated, Literal, TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, AnyMessage

load_dotenv()

# Set OpenAI-compatible endpoint
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "not-needed")
if os.getenv("OPENAI_API_BASE"):
    os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")


class AgentState(TypedDict):
    """State shared across all agents in the pipeline."""
    messages: Annotated[list[AnyMessage], add_messages]


# Import agents
from agents.supervisor import supervisor_node
from agents.researcher import researcher_node
from agents.developer import developer_node


def route_supervisor(state: AgentState) -> Literal["call_researcher", "call_developer", "finish"]:
    """
    Route to next agent based on supervisor's decision.
    
    Args:
        state: Current pipeline state
        
    Returns:
        Next node to execute
    """
    last_message = state["messages"][-1]
    
    if isinstance(last_message, AIMessage):
        try:
            response_json = json.loads(last_message.content)
            action = response_json.get("next_action")
            
            if action == "call_researcher":
                return "call_researcher"
            elif action == "call_developer":
                return "call_developer"
            elif action == "finish":
                return "finish"
        except Exception as e:
            print(f"Error parsing supervisor decision: {e}")
    
    return "finish"


# Build the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("supervisor_node", supervisor_node)
graph.add_node("researcher_node", researcher_node)
graph.add_node("developer_node", developer_node)

# Define edges
graph.add_edge(START, "supervisor_node")
graph.add_edge("researcher_node", "supervisor_node")
graph.add_edge("developer_node", "supervisor_node")

# Add conditional edges from supervisor
graph.add_conditional_edges(
    "supervisor_node",
    route_supervisor,
    {
        "call_researcher": "researcher_node",
        "call_developer": "developer_node",
        "finish": END,
    }
)

# Compile the graph
pipeline = graph.compile()


def run_pipeline(query: str) -> dict:
    """
    Run the AI Research-Code Pipeline.
    
    Args:
        query: User query or task
        
    Returns:
        Pipeline execution result with all messages
    """
    print("=" * 60)
    print("AI RESEARCH-CODE PIPELINE")
    print("=" * 60)
    print(f"\nQuery: {query}\n")
    
    result = pipeline.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    print(result["messages"][-1].content)
    
    return result


if __name__ == "__main__":
    # Example: Stock trading strategy
    query = """
    Create a profitable stock trading strategy using daily data.
    
    Steps:
    1. Research popular trading strategies and indicators
    2. Implement a momentum-based strategy with RSI
    3. Backtest using finance-datareader for Korean stocks
    4. Show performance metrics
    """
    
    result = run_pipeline(query)
