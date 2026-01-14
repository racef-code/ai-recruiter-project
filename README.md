# 🤖 AI Smart Recruiter

> A local AI-powered hiring assistant that matches resumes to job descriptions using Vector Embeddings and Llama 3.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## ✨ Highlights

- ⚡ **50-80% faster** with intelligent model caching
- 🔒 **100% local** - No data sent to cloud
- 🎯 **Smart matching** using semantic similarity
- 🤖 **AI explanations** powered by Llama 3
- 📝 **Professional logging** for debugging

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone <your-repo>
cd llm-project_recruter_ai
pip install -r requirements.txt

# 2. Start Ollama (if using AI explanations)
ollama pull llama3

# 3. Run the app
streamlit run app.py
```

## 📂 Project Structure

```
llm project_recruter_ai/
├── 📱 app.py                    # Main Streamlit application
├── ⚙️ config.py                 # Configuration management
├── 📝 logger.py                 # Logging system
├── 📦 requirements.txt          # Dependencies (pinned)
│
├── 📂 resume_matcher/           # Core business logic
│   ├── resume_parser.py         # PDF text extraction
│   ├── matcher.py               # Semantic matching (cached)
│   └── explainer.py             # AI explanations
│
├── 📂 docs/                     # 📚 Documentation
│   ├── CHANGELOG.md             # Version history
│   └── IMPROVEMENTS_SUMMARY.md  # Detailed improvements
│
├── 📂 scripts/                  # 🛠️ Utility scripts
│   ├── test_improvements.py    # Automated tests
│   └── run_test.py              # Test runner
│
├── 📂 data/                     # Sample resumes
├── 📂 uploads/                  # Temporary uploads
└── 📂 logs/                     # Application logs
```

## ⚙️ Configuration

Create a `.env` file (optional):

```bash
# Copy template
cp .env.example .env

# Edit with your values
MODEL_NAME=all-MiniLM-L6-v2
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
MAX_FILE_SIZE_MB=10
```

Or edit `config.py` directly.

## 🎯 Features

| Feature | Description |
|---------|-------------|
| **Smart Matching** | Semantic similarity using sentence-transformers |
| **PDF Parsing** | Automatic text extraction from resumes |
| **Visual Ranking** | Color-coded scores and rankings |
| **AI Explanations** | Llama 3 explains why candidates match |
| **Model Caching** | 50-80% faster after first load |
| **Logging** | Structured logs in `logs/` directory |

## 📊 Performance

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| First analysis | 5-7s | ~5s | Baseline |
| Subsequent | 5-7s | <1s | **~80% faster** |
| Memory | Variable | Optimized | Shared model |

## 🧪 Testing

```bash
# Run automated tests
python scripts/test_improvements.py

# View logs
cat logs/app_$(date +%Y%m%d).log
```

## 📚 Documentation

- [📖 Full Documentation](docs/)
- [📋 Changelog](docs/CHANGELOG.md)
- [📊 Improvements Summary](docs/IMPROVEMENTS_SUMMARY.md)

## 🛠️ Requirements

- Python 3.8+
- Ollama (optional, for AI explanations)
- ~500MB disk space (for model cache)

## 🤝 Contributing

Contributions welcome! Please check the documentation for guidelines.

## 📝 License

MIT License - see LICENSE file for details.

## 💬 Support

For issues or questions, please open an issue on GitHub.

---

**Made with ❤️ using Python, Streamlit, and AI**
