# Agent Integration Examples

> **Production-ready code for router patterns, MCP tools, and A2A workflows with LOCAL LLMs**

Complete examples showing how to integrate all the components: GDELT collector, n8n workflows, MCP tools, and LOCAL LLMs. Everything runs locally with zero API costs.

## 🎯 What's Included

### 1. Router Examples (`1-router-examples/`)
- **LangGraph Router** - Intelligent task routing with state management
- **CrewAI Router** - Multi-agent crew coordination
- Automatic task classification and delegation

### 2. MCP Tools Examples (`2-mcp-tools-examples/`)
- Using GDELT as a LangChain tool
- n8n workflow integration
- Combining multiple MCP services

### 3. A2A Workflows (`3-a2a-workflows/`)
- Multi-agent collaboration patterns
- Webhook-based communication
- Agent chaining and callbacks

### 4. Full Pipeline (`4-full-pipeline/`)
- Complete end-to-end example
- Router → MCP Tools → A2A → Results
- Production-ready architecture

## 📦 Prerequisites

### Services Required

```bash
# 1. LOCAL LLM (Ollama)
ollama run qwen2.5:7b

# 2. GDELT Article Collector
cd ../gdelt-article-collector
docker-compose up -d

# 3. n8n Agent Hosting
cd ../n8n-agent-hosting
docker-compose up -d
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

Contents:
```
langchain==0.1.0
langchain-ollama==0.0.1
langgraph==0.0.20
crewai==0.1.0
requests==2.31.0
```

## 🚀 Quick Start

### Example 1: LangGraph Router

```bash
python 1-router-examples/langgraph_router.py
```

**What it does:**
- Classifies incoming tasks
- Routes to specialized agents (research, analysis, coding, writing)
- Uses GDELT for research tasks
- Returns structured results

### Example 2: MCP Tools Agent

```bash
python 2-mcp-tools-examples/mcp_tools_agent.py
```

**What it does:**
- Wraps MCP services as LangChain tools
- Agent decides which tool to use
- Combines results from multiple sources

### Example 3: A2A Workflow

```bash
python 3-a2a-workflows/multi_agent_pipeline.py
```

**What it does:**
- Agent A: Researches topic via GDELT
- Agent B: Analyzes results (triggered via n8n)
- Agent C: Writes summary
- All coordinated through webhooks

### Example 4: Full Pipeline

```bash
python 4-full-pipeline/complete_system.py
```

**What it does:**
- Complete production example
- Router classifies task
- Delegates to MCP tools
- Coordinates via n8n A2A
- Returns final result

## 📖 Detailed Examples

### LangGraph Router

```python
from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama

# Define your agents
def research_agent(state):
    # Uses GDELT service
    response = requests.post("http://localhost:8004/search", ...)
    return {"result": response.json()}

def analysis_agent(state):
    # Uses LOCAL LLM
    llm = ChatOllama(model="qwen2.5:7b")
    return {"result": llm.invoke(state["task"])}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("classify", classify_task)
workflow.add_node("research", research_agent)
workflow.add_node("analysis", analysis_agent)

# Add routing
workflow.add_conditional_edges("classify", route_to_agent)
graph = workflow.compile()

# Use it
result = graph.invoke({"task": "Find AI news"})
```

### MCP Tools as LangChain Tools

```python
from langchain.tools import tool
from langchain.agents import initialize_agent

@tool
def gdelt_search(query: str) -> str:
    """Search global news via GDELT"""
    response = requests.post("http://localhost:8004/search", 
        json={"keywords": [query], "timespan": "7d"})
    return response.json()

@tool
def n8n_workflow(task: str) -> str:
    """Trigger n8n agent workflow"""
    response = requests.post("http://localhost:8005/agent/task",
        json={"agent_type": "researcher", "task": task})
    return response.json()

tools = [gdelt_search, n8n_workflow]
agent = initialize_agent(tools, llm, verbose=True)

result = agent.run("Research quantum computing news")
```

### A2A with Callbacks

```python
import requests
from flask import Flask, request

app = Flask(__name__)

# Your callback endpoint
@app.route("/webhook/results", methods=["POST"])
def handle_results():
    data = request.json
    print(f"Agent completed: {data}")
    # Process results...
    return {"status": "received"}

# Start callback server
app.run(port=9000)

# Submit task with callback
requests.post("http://localhost:8005/agent/task", json={
    "agent_type": "researcher",
    "task": "Long-running research task",
    "callback_url": "http://localhost:9000/webhook/results"
})
```

## 🏗️ Architecture Patterns

### Pattern 1: Simple Router

```
User Input → Router → Specialized Agent → Result
```

### Pattern 2: Tool-Based

```
User Input → Agent → [Tool1, Tool2, Tool3] → Result
```

### Pattern 3: Multi-Agent A2A

```
Agent A (Research) → n8n → Agent B (Analysis) → Agent C (Writing) → Result
```

### Pattern 4: Full Pipeline

```
Input → Router → Tools → A2A Coordination → Aggregator → Final Result
```

## 🔧 Configuration

### Environment Variables

Create `.env`:

```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# Services
GDELT_URL=http://localhost:8004
N8N_A2A_URL=http://localhost:8005
GPT_RESEARCHER_URL=http://localhost:8002

# Agent Settings
MAX_ITERATIONS=10
TIMEOUT=300
```

### Service Ports

| Service | Port | Description |
|---------|------|-------------|
| Ollama | 11434 | LOCAL LLM |
| GDELT | 8004 | News search |
| n8n | 5678 | Workflow engine |
| A2A Wrapper | 8005 | Agent coordination |
| GPT Researcher | 8002 | Research service |

## 💡 Best Practices

### 1. Error Handling

```python
def safe_tool_call(tool_func, *args, **kwargs):
    try:
        return tool_func(*args, **kwargs)
    except requests.Timeout:
        return {"error": "Service timeout"}
    except Exception as e:
        return {"error": str(e)}
```

### 2. Async Operations

```python
import asyncio

async def parallel_agents():
    tasks = [
        asyncio.create_task(research_agent()),
        asyncio.create_task(analysis_agent()),
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### 3. Caching Results

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_gdelt_search(query: str, timespan: str):
    return requests.post(...)
```

### 4. Monitoring

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Task classified as: {task_type}")
logger.info(f"Agent {agent_name} activated")
logger.info(f"Result: {result[:100]}...")
```

## 🐛 Troubleshooting

### Services Not Running

```bash
# Check all services
curl http://localhost:11434/api/version  # Ollama
curl http://localhost:8004/health        # GDELT
curl http://localhost:8005/health        # n8n A2A
```

### Agent Not Routing Correctly

- Check task classification prompt
- Verify routing dictionary matches task types
- Add logging to see classification results

### Tools Not Working

- Verify service URLs are correct
- Check timeout settings
- Test tools individually first

## 📊 Performance Tips

1. **Use Smaller Models for Classification** - `qwen2.5:7b` is fast enough
2. **Parallel Tool Calls** - Use async when tools don't depend on each other
3. **Cache Frequent Queries** - Especially for GDELT searches
4. **Timeout Management** - Set appropriate timeouts for each service
5. **Batch Processing** - Process multiple tasks together when possible

## 🔗 Integration Guide

### With Existing LangChain Apps

```python
# Just add the tools
from mcp_tools_agent import gdelt_news_search, n8n_research_workflow

your_existing_agent.tools.extend([
    gdelt_news_search,
    n8n_research_workflow
])
```

### With CrewAI

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Researcher",
    goal="Find latest news",
    tools=[gdelt_news_search]
)

analyst = Agent(
    role="Analyst",
    goal="Analyze findings"
)

crew = Crew(agents=[researcher, analyst])
result = crew.kickoff()
```

### With Custom Frameworks

```python
# Just call the services directly
import requests

def my_custom_agent(task):
    # Use GDELT
    news = requests.post("http://localhost:8004/search", ...)
    
    # Use n8n
    analysis = requests.post("http://localhost:8005/agent/task", ...)
    
    # Combine results
    return combine(news, analysis)
```

## 📚 Additional Resources

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **CrewAI Docs**: https://docs.crewai.com/
- **n8n Docs**: https://docs.n8n.io/
- **Ollama Models**: https://ollama.ai/library

## 🤝 Contributing

Add your own patterns and examples! PRs welcome.

---

**100% LOCAL LLM infrastructure - Zero API costs**
