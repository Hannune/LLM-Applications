"""
Supervisor Agent - Orchestrates the AI Research-Code Pipeline

Coordinates idea generation, research, development, and review.
Works with OpenAI-compatible APIs (Ollama, vLLM, LiteLLM).
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are a supervisor agent orchestrating an AI pipeline with specialized agents:
- Researcher: Gathers information using GPT Researcher
- Developer: Implements code using Open Interpreter

Analyze the conversation and decide the next action:
- call_researcher: Need to gather information or research a topic
- call_developer: Need to implement code or execute tasks
- finish: Task is complete

Respond ONLY with strict JSON:
{
  "next_action": "call_researcher" | "call_developer" | "finish",
  "content": "instructions or summary for the next step"
}

Do NOT add any text outside JSON.
"""

# Initialize LLM (OpenAI-compatible)
llm = ChatOpenAI(
    model=os.getenv("SUPERVISOR_MODEL", "gpt-4o-mini"),
    temperature=0,
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY", "not-needed-for-local")
)


def supervisor_node(state):
    """
    Supervisor node that decides next action in the pipeline.
    
    Args:
        state: Current conversation state with messages
        
    Returns:
        Updated state with supervisor's decision
    """
    print("=== SUPERVISOR ===")
    messages = state["messages"]
    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    full_messages = [system_message] + messages
    
    response = llm.invoke(full_messages)
    print(f"Decision: {response.content}")
    print("==================")
    
    return {"messages": [AIMessage(content=response.content)]}
