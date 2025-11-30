# Korean Real Estate AI Pipeline

> Analyze Korean apartment transaction data using **100% LOCAL LLMs** - No API costs, complete privacy

Comprehensive analysis pipeline for Korean real estate market data using local LLMs (Ollama). Get AI-powered insights on apartment prices, market trends, and investment opportunities - all running locally on your machine.

## ✨ Features

- 🏠 **Korean Real Estate Data Collection** - Direct API integration with 국토교통부 (Ministry of Land)
- 🤖 **LOCAL LLM Analysis** - Zero API costs using Ollama
- 📊 **Market Intelligence** - Price trends, location analysis, investment recommendations
- 🔒 **Complete Privacy** - All data and analysis stays on your machine
- 📈 **Visualization** - Charts with AI-powered interpretations
- 💡 **Investment Insights** - Deal quality assessment, strategy generation

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull a model (choose one)
ollama pull qwen2.5:7b      # Recommended - good Korean support
ollama pull llama3.1:8b     # Alternative
ollama pull gemma2:9b       # Alternative
```

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd korean-realestate-ai-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# (Optional) Add API key if you want to fetch real data from 공공데이터포털
```

### Usage

```bash
# Start Jupyter
jupyter notebook

# Open notebooks/main_analysis.ipynb
# Run all cells to see LOCAL LLM analysis in action
```

## 📁 Project Structure

```
korean-realestate-ai-pipeline/
├── notebooks/
│   └── main_analysis.ipynb              # ⭐ Main showcase notebook
├── data/                                # Your collected data (gitignored)
├── reference/
│   └── api용_법정동코드_서울_경기.csv    # Location codes reference
├── .env.example                         # Environment template
├── requirements.txt                     # Python dependencies
└── README.md
```

## 📓 Main Notebook

### 🌟 main_analysis.ipynb - LOCAL LLM Showcase

Comprehensive showcase demonstrating LOCAL LLM capabilities for Korean real estate analysis:

#### Analysis Modules

1. **Market Trend Analysis**
   - Location-based price statistics
   - LLM interprets patterns and trends
   - Investment recommendations

2. **Price Prediction**
   - Statistical analysis of current prices
   - LLM predicts next month's direction
   - Confidence levels with reasoning

3. **Location Recommendations**
   - Neighborhood comparison
   - Budget-based suggestions (e.g., 40M KRW)
   - Value proposition analysis

4. **Deal Quality Assessment**
   - Evaluate specific transactions
   - Fair price determination
   - Negotiation potential scoring

5. **Visualization + Interpretation**
   - Price distribution charts
   - LLM explains patterns
   - Market segmentation insights

6. **Buyer Type Analysis**
   - Individual vs. institutional buyers
   - Market dynamics insights
   - Strategic implications

7. **Investment Strategy**
   - 6-month plans
   - Budget allocation
   - Risk management

8. **Custom Queries**
   - Ask your own questions
   - Data-driven answers

## 🎯 Use Cases

### For Developers
- Learn LOCAL LLM integration patterns
- See real-world data analysis workflows
- Understand Korean real estate APIs

### For Investors
- Market trend analysis
- Location comparison
- Deal quality assessment
- Investment strategy generation

### For Data Scientists
- Hybrid approach: traditional stats + LLM insights
- Prompt engineering examples
- Visualization best practices

## 🔧 Configuration

### Environment Variables

```bash
# Local LLM (Ollama)
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=qwen2.5:7b

# Data directories
DATA_DIR=./data
REFERENCE_DIR=./reference

# Analysis settings
MAX_ANALYSIS_RECORDS=1000
```

### Customize for Your Needs

```python
# In notebooks/main_analysis.ipynb

# Use your own data
df = pd.read_csv("../data/your_data.csv")

# Change model
llm = ChatOllama(
    model="llama3.1:8b",  # or gemma2:9b, mistral:7b
    base_url="http://localhost:11434"
)

# Adjust prompts
prompt = f"""Your custom analysis prompt here..."""
```

## 📊 Sample Output

```
=== Market Trend Analysis ===
Location Statistics:
                mean  count
새롬동       47000.0      1
종촌동       37500.0      1
반곡동       38100.0      1

LLM Analysis:
1. Top 3 Areas by Price:
   - 새롬동: 47,000만원 (highest premium)
   - 반곡동: 38,100만원 (middle tier)
   - 종촌동: 37,500만원 (entry point)

2. Market Trends:
   - Price spread indicates market segmentation
   - 새롬동 commands 25% premium over 종촌동
   - Relatively stable pricing across locations

3. Investment Recommendations:
   - Growth potential: 반곡동 (balanced price/value)
   - Value entry: 종촌동 (lowest entry point)
   - Premium hold: 새롬동 (established area)
```

## 🌐 Data Source

The notebook uses sample Korean apartment transaction data for demonstration.

For real data:
- **Source**: 공공데이터포털 (Public Data Portal) - https://www.data.go.kr/
- **Data**: 국토교통부 아파트 실거래가 (Ministry of Land apartment transaction records)
- **Format**: CSV files with apartment transaction records
- **Coverage**: Nationwide apartment sales data

## 🔒 Privacy & Security

✅ **100% Local Processing**
- LLM runs on your machine (Ollama)
- No data sent to external APIs
- No usage tracking

✅ **Data Control**
- You own all data files
- `.gitignore` excludes sensitive files
- API keys in `.env` (not committed)

## 🎓 Learning Resources

### Understanding the Code

```python
# Key pattern: LOCAL LLM initialization
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:7b",
    base_url="http://localhost:11434"  # Always localhost
)

# Pattern: Structured prompts
prompt = f"""
Analyze this data:
{data_summary}

Provide:
1. Key insights
2. Recommendations
3. Risk factors
"""

response = llm.invoke(prompt)
```

### Why This Approach Works

1. **Cost Efficiency**: Zero API costs for unlimited analysis
2. **Privacy**: Sensitive financial data stays local
3. **Flexibility**: Try different models, adjust prompts freely
4. **Reproducibility**: Same data, same model = same results
5. **Offline Capability**: Works without internet (after model download)

## 🛠️ Troubleshooting

### Common Issues

**Ollama not connecting**
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# Restart if needed
systemctl restart ollama  # Linux
brew services restart ollama  # macOS
```

**Model not found**
```bash
# List available models
ollama list

# Pull model if missing
ollama pull qwen2.5:7b
```

**Data loading errors**
- Notebook includes sample data by default
- To use your own CSV: update the data loading cell
- Ensure CSV has required columns (aptNm, umdNm, dealAmount, etc.)

## 📈 Future Enhancements

Potential additions:
- [ ] Time series forecasting with LOCAL LLMs
- [ ] Multi-city comparative analysis
- [ ] Automated report generation
- [ ] Real-time price alerts
- [ ] Integration with local RAG systems

## 🤝 Contributing

This is a personal portfolio project, but suggestions are welcome:
1. Open an issue describing your idea
2. Share your use case or enhancement
3. Provide sample code if applicable

## 📄 License

MIT License - feel free to use for learning and personal projects.

## 💬 Contact

- **Purpose**: Developer portfolio / learning resource
- **Focus**: LOCAL LLM applications for real-world data
- **Goal**: Demonstrate practical AI without API costs

---

**Key Takeaway**: Real AI analysis doesn't need cloud APIs or subscription costs. LOCAL LLMs can provide valuable insights for complex domains like real estate - privately, affordably, and effectively.

Built with ❤️ using 100% LOCAL LLMs (Ollama)
