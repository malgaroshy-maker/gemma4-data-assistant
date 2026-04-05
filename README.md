# 💎 Gemma 4 E4B: Multimodal Data Assistant

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemma 4](https://img.shields.io/badge/Model-Gemma%204%20E4B-4285F4.svg?style=flat-square)](https://ai.google.dev/gemma)
[![llama.cpp](https://img.shields.io/badge/Server-llama.cpp-orange.svg?style=flat-square)](https://github.com/ggml-org/llama.cpp)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/malgaroshy-maker/gemma4-data-assistant/pulls)

**A local-first, agentic AI application for private data analysis using Google's Gemma 4 E4B model with multimodal capabilities.**

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Usage](#-usage) • [Configuration](#-configuration) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Architecture](#-architecture)
- [Usage](#-usage)
  - [Data Upload & Analysis](#data-upload--analysis)
  - [Voice Commands](#voice-commands)
  - [Vision Analysis](#vision-analysis)
  - [Agentic Tool Use](#agentic-tool-use)
- [Configuration](#-configuration)
  - [llama-server Setup](#llama-server-setup)
  - [Multimodal Configuration](#multimodal-configuration)
  - [Streamlit Settings](#streamlit-settings)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🌟 Overview

Gemma Data Assistant is a production-ready Streamlit application that enables **private, local-first data analysis** using Google's Gemma 4 E4B model. Unlike cloud-based solutions, all processing happens on your machine—ensuring complete data privacy while delivering state-of-the-art AI capabilities.

The application leverages:
- **Per-Layer Embeddings (PLE)** for efficient 4B parameter inference
- **Native multimodal reasoning** for voice, vision, and text inputs
- **128K context window** for analyzing large datasets
- **Agentic tool execution** for autonomous code generation and visualization

---

## ✨ Features

### 🧠 Advanced Reasoning
- Real-time visualization of AI reasoning via `<|think|>` token processing
- Adjustable reasoning depth: Quick, Standard, or Deep Analysis
- Self-correction and internal math validation before responses

### 🤖 Autonomous Data Agent
- **Dynamic Visualization**: Generates Matplotlib/Seaborn charts on-demand
- **Code Execution**: AI writes and executes Python code with `pandas`, `matplotlib`, `seaborn`
- **Data Transformation**: Multi-step filtering, grouping, and statistical analysis
- **Persistent Results**: Charts and tables survive session reruns

### 🎙️ Multimodal Inputs
- **Voice-to-Text**: Local speech recognition via `SpeechRecognition` library
- **Image Analysis**: Upload screenshots/charts for comparative analysis
- **Text Chat**: Traditional conversational interface with context awareness

### 📊 Data Intelligence
- **Auto-profiling**: Schema detection, column types, and statistical summaries (mean, sum, min, max, std)
- **Context Optimization**: Fast Context mode (100 rows + full statistics) for 70% latency reduction
- **Export Capabilities**: Download transformed data as Excel files
- **Demo Datasets**: 5 pre-loaded datasets for immediate testing

### 🎨 Professional UI
- **Dark Mode**: Google DeepMind-inspired design system
- **Health Check**: Server connectivity validation
- **Context Meter**: Real-time token usage visualization
- **Responsive Design**: Optimized for all screen sizes

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Details |
|-------------|---------|
| **Python** | 3.10 or higher |
| **RAM** | 8GB minimum, 16GB recommended (for 128K context) |
| **llama.cpp** | Installed with `llama-server` binary |
| **Model** | Gemma 4 E4B GGUF from [Unsloth HuggingFace](https://huggingface.co/unsloth/gemma-4-e4b-it-gguf) |
| **OS** | Windows, macOS, or Linux |

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/malgaroshy-maker/gemma4-data-assistant.git
cd gemma4-data-assistant
```

2. **Install dependencies**:
```bash
# Using the automated launcher (creates virtual environment)
./run_app.bat  # Windows
# OR manually:
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. **Download the model** (if not already cached):
```bash
# Models are typically cached at:
# Windows: C:\Users\<user>\.cache\huggingface\hub\
# macOS/Linux: ~/.cache/huggingface/hub/
```

### Running the App

**Step 1: Start the llama-server**
```bash
# Use the pre-configured launcher
./start_llama_server.bat

# Or run manually (update paths to your model locations)
llama-server \
  -m "path/to/gemma-4-E4B-it-Q4_K_XL.gguf" \
  --mmproj "path/to/mmproj-BF16.gguf" \
  --ctx-size 131072 \
  --port 8080
```

**Step 2: Launch the Streamlit app**
```bash
streamlit run app.py
```

**Step 3: Access the application**
- Open your browser to `http://localhost:8501`
- Upload a CSV/Excel file or select a demo dataset
- Start analyzing with AI!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web App (app.py)                │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Data    │  │   Chat   │  │  Voice   │  │  Vision  │   │
│  │  Loader  │  │ Interface│  │  Input   │  │  Input   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │              │              │              │         │
│  ┌────┴──────────────┴──────────────┴──────────────┴─────┐ │
│  │              Session State Manager                     │ │
│  │  • Messages  • Data Context  • Tool Results           │ │
│  └────────────────────────┬──────────────────────────────┘ │
│                           │                                 │
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │              OpenAI-Compatible Client                 │ │
│  │         (connects to localhost:8080/v1)               │ │
│  └────────────────────────┬──────────────────────────────┘ │
└───────────────────────────┼─────────────────────────────────┘
                            │ HTTP API
┌───────────────────────────┼─────────────────────────────────┐
│                    llama.cpp Server                          │
├───────────────────────────┼─────────────────────────────────┤
│  ┌────────────────────────┴──────────────────────────────┐ │
│  │              Gemma 4 E4B Model (GGUF)                 │ │
│  │         + Multimodal Projector (mmproj)               │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Upload** → CSV/Excel parsed by `pandas` → Object columns converted to strings
2. **Context Building** → Schema + statistics (`describe()`, `sum()`) → Injected into system prompt
3. **Fast Context** (optional) → Only top 100 rows sent → 70% latency reduction
4. **AI Processing** → OpenAI client → `llama-server` on port 8080 → Streaming response
5. **Tool Execution** → AI generates Python code → `exec()` with `df`, `pd`, `plt`, `sns` in globals
6. **Result Persistence** → Charts saved as base64 → Stored in `session_state.messages` → Survives reruns

---

## 📖 Usage

### Data Upload & Analysis

1. Navigate to the **Sidebar** → **Upload Data**
2. Select a CSV or Excel file
3. For Excel files, choose the sheet to analyze
4. The app automatically:
   - Profiles the dataset (rows, columns, types)
   - Calculates statistics (mean, sum, min, max)
   - Builds the context window
   - Displays a health check summary

### Voice Commands

1. Click the **🎙️ microphone icon** next to the chat input
2. Speak your question clearly
3. The app transcribes locally using `SpeechRecognition.recognize_google()`
4. Transcribed text replaces the typed prompt
5. **MD5 hash deduplication** prevents repeated processing

**Example commands:**
- "Show me a bar chart of sales by region"
- "What is the average salary by department?"
- "Find outliers in the performance scores"

### Vision Analysis

1. Use the **🖼️ Add context image** file uploader
2. Select a PNG, JPG, or JPEG image
3. The image is encoded to base64 and sent with your prompt
4. **Hash deduplication** prevents infinite reruns

**Use cases:**
- Upload external charts for comparison with your data
- Share dashboard screenshots for AI analysis
- Provide visual context for data-driven questions

### Agentic Tool Use

The AI can autonomously execute Python code through the `execute_python_code` tool:

**Available in execution context:**
- `df`: Your loaded DataFrame
- `pd`: Pandas library
- `plt`: Matplotlib pyplot
- `sns`: Seaborn library

**Example AI-generated code:**
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create correlation heatmap
numeric_df = df.select_dtypes(include=['number'])
corr = numeric_df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
```

Results (charts, code, DataFrames) are **persisted in chat history** and re-rendered on every rerun.

---

## ⚙️ Configuration

### llama-server Setup

The `llama-server` is the backend inference engine. Key configuration options:

| Flag | Description | Example |
|------|-------------|---------|
| `-m` | Path to GGUF model file | `gemma-4-E4B-it-Q4_K_XL.gguf` |
| `--mmproj` | Path to multimodal projector | `mmproj-BF16.gguf` |
| `--ctx-size` | Context window size | `131072` (128K tokens) |
| `--port` | Server port | `8080` |
| `--host` | Bind address | `0.0.0.0` |
| `-ngl` | GPU layers to offload | `999` (all layers) |

**Multimodal Note**: The `--mmproj` flag is **required** for voice/vision features. Without it, image/audio inputs will return 500 errors.

### Multimodal Configuration

llama.cpp supports multimodal inputs through the `libmtmd` library. Key points:

- **Two files required**: Language model (`.gguf`) + Multimodal projector (`.gguf`)
- **GPU offloading**: Projector is offloaded to GPU by default
- **Disable offloading**: Add `--no-mmproj-offload` if experiencing GPU memory issues
- **Supported modalities**: Image and audio (audio is experimental)

### Streamlit Settings

Create `.streamlit/config.toml` for persistent settings:

```toml
[server]
port = 8501
headless = true

[theme]
base = "dark"
primaryColor = "#60A5FA"
backgroundColor = "#0F172A"
secondaryBackgroundColor = "#1E293B"
textColor = "#F1F5F9"
font = "sans serif"

[browser]
gatherUsageStats = false
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_URL` | llama-server endpoint | `http://localhost:8080/v1` |
| `MODEL_NAME` | Model identifier | `unsloth/gemma-4-e4b-it-gguf:Q4_K_XL` |

---

## 📁 Project Structure

```
gemma-data-assistant/
├── app.py                          # Main Streamlit application (~640 lines)
├── start_llama_server.bat          # Pre-configured server launcher
├── run_app.bat                     # Windows app launcher (auto-creates venv)
├── run_app.ps1                     # PowerShell app launcher
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── AGENTS.md                       # Agent onboarding guide
├── user-manual.md                  # User guide with demo scenarios
├── gemma4-doc.md                   # Gemma 4 model documentation
├── design-system/                  # UI/UX design system
│   ├── gemma-data-assistant/
│   │   └── MASTER.md
│   └── gemma-data-assistant-v2/
│       └── MASTER.md
└── .streamlit/                     # Streamlit configuration (optional)
    └── config.toml
```

### Key Files

| File | Purpose |
|------|---------|
| `app.py` | Single-file Streamlit app with all logic |
| `start_llama_server.bat` | Launches `llama-server` with correct model paths |
| `run_app.bat` | Creates venv, installs deps, runs app |
| `AGENTS.md` | Technical documentation for AI agents |
| `requirements.txt` | All Python dependencies |

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test with both CSV and Excel files
- Ensure compatibility with `llama-server` on port 8080
- Update `AGENTS.md` for architectural changes

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google DeepMind** for the Gemma 4 model series
- **llama.cpp** community for the inference engine
- **Streamlit** team for the amazing UI framework
- **Unsloth** for optimized GGUF model conversions

---

<div align="center">

**Developed by [Mahamed Algaroshy](https://github.com/malgaroshy-maker)**  
*Electrical Engineer & AI Enthusiast*

[⭐ Star this repo](https://github.com/malgaroshy-maker/gemma4-data-assistant/stargazers) • [🐛 Report Bug](https://github.com/malgaroshy-maker/gemma4-data-assistant/issues) • [💡 Request Feature](https://github.com/malgaroshy-maker/gemma4-data-assistant/issues)

</div>
