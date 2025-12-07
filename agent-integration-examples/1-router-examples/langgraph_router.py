"""
LangGraph Router Example
Intelligent task routing to specialized agents
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import requests


# State definition
class AgentState(TypedDict):
    task: str
    task_type: Literal["research", "analysis", "coding", "writing"]
    result: str
    error: str


# Initialize LLM (LOCAL)
llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434"
)


def classify_task(state: AgentState) -> AgentState:
    """Classify the incoming task"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Classify the task into ONE category:
        - research: finding information, news, data collection
        - analysis: analyzing data, summarizing, interpreting
        - coding: programming, debugging, code generation
        - writing: creative writing, reports, documentation
        
        Respond with ONLY the category name."""),
        ("human", "{task}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"task": state["task"]})
    task_type = response.content.strip().lower()
    
    print(f"📋 Task classified as: {task_type}")
    
    return {**state, "task_type": task_type}


def research_agent(state: AgentState) -> AgentState:
    """Handle research tasks using GDELT"""
    print("🔍 Research Agent activated")
    
    try:
        # Call GDELT service
        response = requests.post(
            "http://localhost:8004/search",
            json={
                "keywords": [state["task"]],
                "timespan": "7d",
                "max_results": 10
            },
            timeout=30
        )
        
        data = response.json()
        
        if data["success"]:
            articles = data["articles"][:5]
            result = f"Found {data['count']} articles.\n\nTop 5:\n"
            for i, article in enumerate(articles, 1):
                result += f"{i}. {article.get('title', 'No title')}\n"
                result += f"   Source: {article.get('domain', 'Unknown')}\n"
                result += f"   URL: {article.get('url', '')}\n\n"
            
            return {**state, "result": result}
        else:
            return {**state, "error": "Research failed"}
            
    except Exception as e:
        return {**state, "error": f"Research error: {str(e)}"}


def analysis_agent(state: AgentState) -> AgentState:
    """Handle analysis tasks"""
    print("📊 Analysis Agent activated")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert data analyst. Provide clear, structured analysis."),
        ("human", "{task}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"task": state["task"]})
    
    return {**state, "result": response.content}


def coding_agent(state: AgentState) -> AgentState:
    """Handle coding tasks"""
    print("💻 Coding Agent activated")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert programmer. Provide clean, well-commented code."),
        ("human", "{task}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"task": state["task"]})
    
    return {**state, "result": response.content}


def writing_agent(state: AgentState) -> AgentState:
    """Handle writing tasks"""
    print("✍️  Writing Agent activated")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional writer. Create clear, engaging content."),
        ("human": "{task}")
    ])
    
    chain = prompt | llm
    response = chain.invoke({"task": state["task"]})
    
    return {**state, "result": response.content}


def route_task(state: AgentState) -> str:
    """Route to appropriate agent based on task type"""
    routing = {
        "research": "research_agent",
        "analysis": "analysis_agent",
        "coding": "coding_agent",
        "writing": "writing_agent"
    }
    
    return routing.get(state["task_type"], "analysis_agent")


# Build the graph
def create_router_graph():
    """Create the LangGraph router"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("classify", classify_task)
    workflow.add_node("research_agent", research_agent)
    workflow.add_node("analysis_agent", analysis_agent)
    workflow.add_node("coding_agent", coding_agent)
    workflow.add_node("writing_agent", writing_agent)
    
    # Set entry point
    workflow.set_entry_point("classify")
    
    # Add conditional routing
    workflow.add_conditional_edges(
        "classify",
        route_task,
        {
            "research_agent": "research_agent",
            "analysis_agent": "analysis_agent",
            "coding_agent": "coding_agent",
            "writing_agent": "writing_agent"
        }
    )
    
    # All agents end the workflow
    workflow.add_edge("research_agent", END)
    workflow.add_edge("analysis_agent", END)
    workflow.add_edge("coding_agent", END)
    workflow.add_edge("writing_agent", END)
    
    return workflow.compile()


# Example usage
if __name__ == "__main__":
    graph = create_router_graph()
    
    # Test cases
    test_tasks = [
        "Find recent news about artificial intelligence",
        "Analyze the trends in quantum computing",
        "Write a Python function to calculate fibonacci numbers",
        "Write a blog post about machine learning"
    ]
    
    for task in test_tasks:
        print(f"\n{'='*60}")
        print(f"Task: {task}")
        print(f"{'='*60}")
        
        result = graph.invoke({
            "task": task,
            "task_type": "",
            "result": "",
            "error": ""
        })
        
        if result.get("error"):
            print(f"❌ Error: {result['error']}")
        else:
            print(f"\n✅ Result:\n{result['result'][:500]}...")
