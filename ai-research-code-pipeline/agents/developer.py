"""
Developer Agent - Code Implementation using Open Interpreter

Implements code and executes tasks using Open Interpreter.
Works with OpenAI-compatible APIs (Ollama, vLLM, LiteLLM).
"""

import os
from interpreter import interpreter
from langchain_core.messages import AIMessage
from dotenv import load_dotenv

load_dotenv()

# Configure Open Interpreter with OpenAI-compatible endpoint
interpreter.llm.model = os.getenv("DEVELOPER_MODEL", "gpt-4o-mini")
interpreter.llm.api_key = os.getenv("OPENAI_API_KEY", "not-needed-for-local")
interpreter.llm.api_base = os.getenv("OPENAI_API_BASE")

# Safety settings
interpreter.auto_run = os.getenv("DEVELOPER_AUTO_RUN", "false").lower() == "true"
interpreter.safe_mode = os.getenv("DEVELOPER_SAFE_MODE", "ask")


def developer_node(state):
    """
    Developer node that implements code and executes tasks.
    
    Args:
        state: Current conversation state with messages
        
    Returns:
        Updated state with development output
    """
    print("=== DEVELOPER ===")
    messages = state["messages"]
    last_message = messages[-1]
    
    # Extract task from supervisor's instructions
    import json
    try:
        supervisor_json = json.loads(last_message.content)
        task = supervisor_json.get("content", last_message.content)
    except:
        task = last_message.content
    
    print(f"Developing: {task[:100]}...")
    output = interpreter.chat(task)
    print(f"Development complete")
    print("==================")
    
    # Format output
    output_text = ""
    for message in output:
        if message.get("type") == "message":
            output_text += message.get("content", "") + "\n"
        elif message.get("type") == "code":
            output_text += f"\nCode executed:\n```\n{message.get('content', '')}\n```\n"
    
    return {"messages": [AIMessage(content=f"Development Output:\n{output_text}")]}
