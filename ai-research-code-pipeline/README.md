# AI Research-Code Pipeline

**Autonomous AI pipeline: From idea to implementation - 100% LOCAL LLMs**

An intelligent agent system that takes a high-level task, researches it, implements the code, and validates results—all using local LLMs (Ollama, vLLM, LiteLLM) with OpenAI-compatible APIs.

## Architecture

```
User Query
    ↓
┌───────────────┐
│  Supervisor   │  Decides next action
│    Agent      │  (Ollama/vLLM/LiteLLM)
└───────┬───────┘
        │
    ┌───┴────┬──────────┐
    │        │          │
┌───▼────┐ ┌▼────────┐ ┌▼─────────┐
│Research│ │Developer│ │  Finish  │
│ Agent  │ │  Agent  │ │          │
└───┬────┘ └────┬────┘ └──────────┘
    │           │
┌───▼─────┐ ┌──▼──────────┐
│GPT      │ │Open         │
│Researcher│ │Interpreter  │
└─────────┘ └─────────────┘
   LOCAL        LOCAL
```

## Features

- **OpenAI-Compatible** - Works with Ollama, vLLM, LiteLLM, or OpenAI
- **Autonomous Pipeline** - Supervisor orchestrates research and development
- **Deep Research** - Uses GPT Researcher for information gathering
- **Code Execution** - Open Interpreter implements and validates
- **LangGraph Workflow** - Structured multi-agent coordination
- **100% Local Option** - Run entirely on your hardware with local LLMs

## Quick Start

### Prerequisites
- Python 3.10+
- Local LLM server running (Ollama/vLLM/LiteLLM)
- Tavily API key (free tier available)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Setup Local LLM

**Option A: Ollama**
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Pull models
ollama pull qwen2.5:7b
ollama pull nomic-embed-text

# Ollama serves on http://localhost:11434
```

**Option B: vLLM**
```bash
# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8000
```

**Option C: LiteLLM**
```bash
# Use existing LiteLLM gateway
# See: ../../local-llm-infrastructure/litellm-local-gateway
```

### 4. Run Pipeline
```bash
python main.py
```

## Configuration

### .env Settings

```bash
# Local LLM with Ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=not-needed
SUPERVISOR_MODEL=qwen2.5:7b
DEVELOPER_MODEL=qwen2.5:7b

# Or use LiteLLM gateway
OPENAI_API_BASE=http://localhost:4000
SUPERVISOR_MODEL=qwen2.5:7b

# Or use OpenAI
OPENAI_API_BASE=
OPENAI_API_KEY=sk-...
SUPERVISOR_MODEL=gpt-4o-mini
```

## Usage

### Example 1: Stock Trading Strategy
```python
from main import run_pipeline

query = """
Create a profitable stock trading strategy using daily data.

Steps:
1. Research popular trading strategies and indicators
2. Implement a momentum-based strategy with RSI
3. Backtest using finance-datareader for Korean stocks
4. Show performance metrics
"""

result = run_pipeline(query)
```

**What Happens:**
1. Supervisor analyzes the task
2. Researcher gathers info on trading strategies
3. Developer implements the strategy code
4. Developer backtests and shows results
5. Supervisor decides task is complete

### Example 2: Data Analysis
```python
query = """
Analyze sales data and create visualizations.

1. Research best practices for sales analysis
2. Create Python code to load and analyze data
3. Generate charts showing trends
4. Provide insights and recommendations
"""

result = run_pipeline(query)
```

### Example 3: Web Scraping Project
```python
query = """
Build a web scraper for product prices.

1. Research ethical web scraping techniques
2. Implement scraper using BeautifulSoup
3. Store data in SQLite database
4. Show sample results
"""

result = run_pipeline(query)
```

## Workflow

1. **User Query** → Supervisor receives task
2. **Supervisor Decision** → Calls researcher or developer
3. **Research Phase** → GPT Researcher gathers information
4. **Development Phase** → Open Interpreter implements code
5. **Validation** → Code runs and results are checked
6. **Iteration** → Supervisor may request refinements
7. **Completion** → Final output delivered

## Agents

### Supervisor Agent
- **Role**: Orchestrator
- **Model**: Configurable (default: qwen2.5:7b)
- **Decisions**: call_researcher, call_developer, or finish
- **Output**: JSON with next action

### Researcher Agent
- **Tool**: GPT Researcher
- **Model**: Configurable (default: qwen2.5:7b)
- **Task**: Deep research on topics
- **Output**: Comprehensive reports

### Developer Agent
- **Tool**: Open Interpreter
- **Model**: Configurable (default: qwen2.5:7b)
- **Task**: Code implementation and execution
- **Output**: Code + execution results

## Use Cases

### 1. Automated Trading Strategies
Research → Implement → Backtest → Report

### 2. Data Science Projects
Research methods → Write analysis code → Generate visualizations

### 3. Machine Learning Experiments
Research algorithms → Implement models → Train and evaluate

### 4. Web Development
Research frameworks → Build application → Test functionality

### 5. System Administration
Research solutions → Write automation scripts → Execute and verify

## Safety

### Open Interpreter Settings
```bash
# Ask before running code (safest)
DEVELOPER_AUTO_RUN=false
DEVELOPER_SAFE_MODE=ask

# Auto-run safe operations only
DEVELOPER_AUTO_RUN=true
DEVELOPER_SAFE_MODE=auto

# No restrictions (use with caution!)
DEVELOPER_AUTO_RUN=true
DEVELOPER_SAFE_MODE=off
```

## Performance

### With Local LLMs (Ollama)
- **Latency**: ~2-5s per LLM call
- **Cost**: $0 (completely free)
- **Privacy**: 100% local, no data leaves your machine
- **Throughput**: Depends on hardware

### With OpenAI
- **Latency**: ~1-2s per call
- **Cost**: ~$0.50-2 per complex task
- **Privacy**: Data sent to OpenAI
- **Throughput**: High

## Troubleshooting

### Cannot connect to local LLM
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Verify endpoint in .env
OPENAI_API_BASE=http://localhost:11434/v1
```

### GPT Researcher fails
- Ensure TAVILY_API_KEY is set
- Check internet connection
- Verify LLM endpoint is correct

### Open Interpreter asks for confirmation
- This is normal with `DEVELOPER_SAFE_MODE=ask`
- Set to `auto` for automatic safe operations
- Or manually confirm each code execution

### Model not found
```bash
# Pull the model in Ollama
ollama pull qwen2.5:7b

# Or update .env to use available model
SUPERVISOR_MODEL=llama3.1:8b
```

## Advanced

### Custom Agents
Add new agents by:
1. Create `agents/your_agent.py`
2. Define `your_agent_node(state)` function
3. Add to graph in `main.py`
4. Update supervisor prompt

### Integration with MCP Services
Use the MCP agent services we built:
```python
# Point to dockerized services
OPENAI_API_BASE=http://localhost:8001  # Open Interpreter Service
RESEARCHER_URL=http://localhost:8002    # GPT Researcher Service
```

### LangGraph Visualization
```python
from IPython.display import Image, display
display(Image(pipeline.get_graph().draw_mermaid_png()))
```

## Comparison: Local vs Cloud

| Feature | Local LLMs | OpenAI |
|---------|-----------|---------|
| Cost | Free | ~$0.50-2/task |
| Speed | 2-5s/call | 1-2s/call |
| Privacy | 100% local | Cloud-based |
| Quality | Good (7B models) | Excellent (GPT-4) |
| Setup | More complex | Simple |
| Best For | Portfolio, learning | Production |

## Requirements

- Python 3.10+
- 8GB RAM minimum (16GB recommended for local LLMs)
- GPU optional but recommended for faster local inference
- Internet connection (for research phase)

## License

MIT

## Credits

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [GPT Researcher](https://github.com/assafelovic/gpt-researcher) - Research
- [Open Interpreter](https://github.com/KillianLucas/open-interpreter) - Code execution
- [Ollama](https://ollama.ai) - Local LLM serving
