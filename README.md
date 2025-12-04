# LLM Applications

> **Complete, production-ready applications built with 100% LOCAL LLMs**

End-to-end applications demonstrating real-world use cases powered entirely by local Large Language Models. From multi-agent research systems to Korean real estate analysis - all running locally with zero API costs.

## 🎯 Why This Repository?

**Real Applications** - Not just demos, actual working software  
**100% Local** - No cloud APIs, no subscription fees  
**Privacy First** - Your data stays on your machine  
**Production Quality** - Clean code, proper error handling, comprehensive docs  
**Learn by Example** - See how to build complete LLM apps

## 📦 Applications

### 🔬 [ai-research-code-pipeline](./ai-research-code-pipeline/)
**Multi-agent system for research → code → validation workflow**

LangGraph-powered application where specialized AI agents collaborate to research topics, write code implementations, and validate results - all using LOCAL LLMs.

**Agents:**
- **Supervisor**: Coordinates the workflow and delegates tasks
- **Researcher**: Uses GPT Researcher to gather information from multiple sources
- **Developer**: Writes code with Open Interpreter based on research findings

**Architecture:**
```
User Query
    ↓
Supervisor Agent (LOCAL LLM)
    ↓
├── Researcher Agent → GPT Researcher → Multi-source research
│       ↓
├── Developer Agent → Open Interpreter → Code generation
│       ↓
└── Validation → Execute & verify → Results
```

**Example workflow:**
```python
# User: "Research and implement a stock data analyzer"

# 1. Researcher gathers data about stock APIs, best practices
# 2. Developer writes Python code based on research
# 3. System executes and validates the code
# 4. Returns working implementation + documentation
```

**Use Case**: Automated software development, research automation, proof-of-concept generation

**Tech Stack:**
- LangGraph for workflow orchestration
- OpenAI-compatible API (works with Ollama/vLLM/LiteLLM)
- GPT Researcher for web research
- Open Interpreter for code execution

---

### 🏠 [korean-realestate-ai-pipeline](./korean-realestate-ai-pipeline/)
**AI-powered analysis of Korean apartment transaction data**

Jupyter notebook-based pipeline demonstrating LOCAL LLM analysis of real government data (공공데이터포털). Shows practical LLM application for financial/market analysis.

**Analysis Capabilities:**
1. **Market Trend Analysis** - LLM interprets location-based pricing patterns
2. **Price Prediction** - Statistical analysis + LLM reasoning for forecasts
3. **Location Recommendations** - Budget-based neighborhood suggestions
4. **Deal Quality Assessment** - Evaluate specific transactions for fairness
5. **Visualization + Interpretation** - Charts explained by LLM
6. **Buyer Type Analysis** - Market dynamics from transaction patterns
7. **Investment Strategy** - 6-month plans with LLM reasoning
8. **Custom Queries** - Interactive data exploration with LLM

**Example:**
```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen2.5:7b", base_url="http://localhost:11434")

# Analyze market data
prompt = f"""
Analyze this Korean real estate data:
{location_stats.to_string()}

Provide:
1. Top 3 areas by price
2. Market trends
3. Investment recommendations
"""

analysis = llm.invoke(prompt)
print(analysis.content)
```

**Data Source:** 공공데이터포털 (Public Data Portal) - Korean government apartment transaction records

**Use Case**: Financial analysis, market research, investment decision support

**Tech Stack:**
- Jupyter notebooks for interactive analysis
- Pandas for data processing
- Matplotlib for visualizations
- LangChain + Ollama for LOCAL LLM integration
- Sample data included (works without API keys)

---

## 🏗️ Application Architecture Comparison

### ai-research-code-pipeline (Agentic)
```
┌─────────────────────────────────────────┐
│          LangGraph Workflow             │
│  ┌──────────┐    ┌──────────┐          │
│  │Supervisor│───▶│Researcher│          │
│  │  Agent   │    │  Agent   │          │
│  └────┬─────┘    └────┬─────┘          │
│       │               │                 │
│       ▼               ▼                 │
│  ┌─────────┐    ┌──────────┐          │
│  │Developer│    │GPT       │          │
│  │  Agent  │    │Researcher│          │
│  └─────────┘    └──────────┘          │
└─────────────────────────────────────────┘
         ↓
    LOCAL LLM (Ollama/vLLM/LiteLLM)
```

### korean-realestate-ai-pipeline (Analytical)
```
┌─────────────────────────────────────────┐
│         Jupyter Notebook                │
│  ┌──────────┐    ┌──────────┐          │
│  │Data Load │───▶│Statistical│          │
│  │& Process │    │ Analysis  │          │
│  └────┬─────┘    └────┬─────┘          │
│       │               │                 │
│       ▼               ▼                 │
│  ┌─────────┐    ┌──────────┐          │
│  │LLM      │───▶│Results + │          │
│  │Analysis │    │ Insights │          │
│  └─────────┘    └──────────┘          │
└─────────────────────────────────────────┘
         ↓
    LOCAL LLM (Ollama)
```

## 🚀 Quick Start

### 1. AI Research-Code Pipeline

```bash
# Prerequisites
ollama pull qwen2.5:7b  # or any OpenAI-compatible LLM

# Install
cd ai-research-code-pipeline
pip install -r requirements.txt
cp .env.example .env

# Configure
# Edit .env to set OPENAI_API_BASE=http://localhost:11434/v1

# Run
python main.py

# Example query:
# "Research pandas DataFrame operations and implement a data analyzer"
```

### 2. Korean Real Estate Analysis

```bash
# Prerequisites
ollama pull qwen2.5:7b

# Install
cd korean-realestate-ai-pipeline
pip install -r requirements.txt
cp .env.example .env

# Run Jupyter
jupyter notebook

# Open notebooks/main_analysis.ipynb
# Run all cells to see LLM analysis in action
```

## 💡 Use Case Examples

### Research Automation
**Application**: ai-research-code-pipeline  
**Scenario**: Research and implement new features

```python
query = """
Research the latest best practices for API rate limiting in Python,
then implement a decorator that enforces rate limits with exponential backoff.
"""

result = supervisor_agent.invoke(query)
# Returns: Research summary + working code + test cases
```

### Financial Analysis
**Application**: korean-realestate-ai-pipeline  
**Scenario**: Analyze investment opportunities

```python
# Load your transaction data
df = pd.read_csv("apartment_transactions.csv")

# Get LLM analysis
prompt = f"""
Given this data: {df.describe()}
Recommend best neighborhoods for 500M KRW budget.
"""

recommendation = llm.invoke(prompt)
```

### Market Intelligence
**Both Applications**  
**Scenario**: Combine research + analysis

1. Use ai-research-code-pipeline to research market analysis techniques
2. Generate custom analysis code
3. Apply to korean-realestate-ai-pipeline data
4. Get comprehensive market intelligence report

## 🔧 Configuration

Both applications use OpenAI-compatible APIs:

```env
# Works with Ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=ollama

# Works with vLLM
OPENAI_API_BASE=http://localhost:8000/v1
OPENAI_API_KEY=EMPTY

# Works with LiteLLM Gateway
OPENAI_API_BASE=http://localhost:4000/v1
OPENAI_API_KEY=EMPTY

# Model selection
LLM_MODEL=qwen2.5:7b  # or llama3.1:8b, mistral:7b, etc.
```

## 📊 Application Comparison

| Feature | ai-research-code-pipeline | korean-realestate-ai-pipeline |
|---------|---------------------------|-------------------------------|
| **Type** | Multi-agent workflow | Data analysis notebook |
| **Complexity** | High | Medium |
| **Setup Time** | 15 minutes | 10 minutes |
| **Use Case** | Research + coding | Financial analysis |
| **Interface** | Python script | Jupyter notebook |
| **Output** | Code + docs | Insights + visualizations |
| **Best For** | Automation, development | Analysis, research |

## 🛠️ Development

### Building Your Own Application

Follow this structure:

```
your-app/
├── README.md              # Comprehensive documentation
├── .env.example          # Configuration template
├── requirements.txt      # Dependencies
├── main.py               # Entry point (or main notebook)
├── agents/               # Agent implementations (if multi-agent)
└── tests/                # Unit tests
```

### Best Practices

1. **Use environment variables** - Make LLM endpoints configurable
2. **Support multiple backends** - Test with Ollama, vLLM, LiteLLM
3. **Include sample data** - Let users try without setup
4. **Document workflows** - Explain agent interactions clearly
5. **Handle errors gracefully** - LLM calls can fail
6. **Provide examples** - Show real usage scenarios

## 🐛 Troubleshooting

### LLM not responding
```bash
# Check if LLM server is running
curl http://localhost:11434/api/tags  # Ollama
curl http://localhost:8000/v1/models  # vLLM

# Check OPENAI_API_BASE in .env
grep OPENAI_API_BASE .env
```

### Agent workflow errors
```bash
# Enable debug logging
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT=http://localhost:8000

# Check LangGraph state
python -c "from main import graph; print(graph.get_state())"
```

### Notebook kernel issues
```bash
# Install ipykernel
pip install ipykernel

# Add kernel
python -m ipykernel install --user --name=llm-env
```

## 🎓 Learning Resources

### Understanding Multi-Agent Systems
See `ai-research-code-pipeline/` for:
- LangGraph workflow orchestration
- Agent communication patterns
- Tool integration (GPT Researcher, Open Interpreter)
- Error handling in agent systems

### Understanding LLM Data Analysis
See `korean-realestate-ai-pipeline/` for:
- Prompt engineering for analysis
- Combining traditional stats with LLM insights
- Visualization interpretation with LLMs
- Structured output parsing

## 🤝 Contributing

Portfolio showcasing complete LLM applications. Feedback welcome:

1. Share your adaptations or forks
2. Report bugs or issues
3. Suggest new application ideas

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent frameworks
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [GPT Researcher](https://github.com/assafelovic/gpt-researcher) - Automated research
- [Open Interpreter](https://github.com/KillianLucas/open-interpreter) - Code execution
- [Pandas](https://pandas.pydata.org/) - Data analysis

## 🔗 Related Repositories

**Infrastructure**: [local-llm-infrastructure](https://github.com/Hannune/Local-LLM-Infrastructure) - Deploy and manage local LLMs  
**Components**: [llm-components](https://github.com/Hannune/LLM-Components) - Reusable building blocks

---

**Real applications, real results - all powered by LOCAL LLMs** 🚀

These are complete applications you can learn from, adapt, and deploy in your own projects.
