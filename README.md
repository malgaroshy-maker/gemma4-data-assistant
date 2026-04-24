# 💎 Gemma 4 E4B: Multimodal Data Assistant

[🇺🇸 English](README.md) | [🇸🇦 العربية](#-مساعد-البيانات-متعدد-الوسائط-gemma-4-e4b)

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
  - [Environment Variables](#environment-variables)
- [Internationalization (i18n)](#-internationalization-i18n)
  - [Arabic Support](#arabic-support)
  - [RTL Layout](#rtl-layout)
  - [Adding New Languages](#adding-new-languages)
- [Project Structure](#-project-structure)
- [Known Limitations](#-known-limitations)
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
- **Voice-to-Text**: Fully offline speech recognition via Gemma 4 E4B's native ASR (Conformer audio encoder)
- **Image Analysis**: Upload screenshots/charts for comparative analysis
- **Text Chat**: Traditional conversational interface with context awareness

### 📊 Data Intelligence
- **Auto-profiling**: Schema detection, column types, and statistical summaries (mean, sum, min, max, std)
- **Context Optimization**: Fast Context mode (100 rows + full statistics) for 70% latency reduction
- **Export Capabilities**: Download transformed data as Excel files, plus AI-generated Excel reports with tables and charts
- **Demo Datasets**: 5 pre-loaded datasets for immediate testing

### 🌐 Bilingual Support (English / العربية)
- **Full Arabic UI**: Every label, button, and message translated
- **RTL Layout**: Complete right-to-left layout mirroring for Arabic
- **Arabic Charts**: Matplotlib charts with properly rendered Arabic text (reshaping + bidi)
- **Dynamic Language Switching**: Switch between English and Arabic instantly without restart
- **Arabic Font Support**: Auto-detects Noto Sans Arabic or falls back to system fonts (Arial, Tahoma, Segoe UI)

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
# Use the optimized launcher (recommended for RTX 4060 8GB)
./llama-opencode.bat

# Or use the legacy launcher
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

> ✅ **Fully Offline**: Voice input uses Gemma 4 E4B's native ASR. No internet connection required.

1. Click the **🎙️ microphone icon** next to the chat input
2. Speak your question clearly
3. The app transcribes using Gemma 4's built-in Conformer audio encoder via llama-server's `/v1/audio/transcriptions` endpoint
4. Transcribed text is displayed for confirmation before sending
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
- `openpyxl`: Excel workbook creation

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
maxUploadSize = 200

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

## 🌐 Internationalization (i18n)

### Arabic Support

The app supports **full bilingual mode** (English / العربية) with a language selector in the sidebar.

**What's translated:**
- All UI labels, buttons, and headers
- Chat input placeholder and status messages
- Error and success notifications
- Pro tips and demo descriptions
- Chart labels and titles (via `arabic-reshaper` + `python-bidi`)

**How it works:**
1. **Translation Dictionary**: `translations.py` contains all UI strings in both languages
2. **RTL CSS**: When Arabic is selected, comprehensive CSS injects `direction: rtl` across all elements
3. **Arabic Charts**: Matplotlib text is automatically reshaped and reordered (right-to-left) before rendering
4. **Font Detection**: Auto-detects Noto Sans Arabic from Windows font directories, falls back to Arial/Tahoma/Segoe UI
5. **Lazy Initialization**: Arabic font/reshaper setup runs only when Arabic is first selected (performance optimization)

### RTL Layout

The RTL implementation includes:
- Sidebar mirrored to the right side
- Chat messages right-aligned
- Tables and metrics right-aligned
- Feature tips with right border accent
- Code blocks remain LTR (for Python readability)

### Adding New Languages

To add a new language:

1. Add translations to `translations.py`:
```python
"fr": {
    "config_header": "⚙️ Configuration",
    # ... all other keys
},
```

2. Update the language selector in `app.py`:
```python
lang_options = {"en": "🇬🇧 English", "ar": "🇸🇦 العربية", "fr": "🇫🇷 Français"}
```

3. Add RTL CSS if needed (for RTL languages like Hebrew, Urdu, etc.)

---

## 📁 Project Structure

```
gemma4-data-assistant/
├── app.py                          # Main Streamlit application (~1200 lines)
├── translations.py                 # Bilingual translation dictionary (EN/AR)
├── llama-opencode.bat              # Optimized server launcher (128K, flash attn)
├── start_llama_server.bat          # Legacy server launcher
├── run_app.bat                     # Windows app launcher (auto-creates venv)
├── run_app.ps1                     # PowerShell app launcher
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── AGENTS.md                       # Agent onboarding guide
├── user-manual.md                  # User guide with demo scenarios
├── gemma4-doc.md                   # Gemma 4 model documentation
├── design-system/                  # UI/UX design system
│   ├── gemma4-data-assistant/
│   │   └── MASTER.md
│   └── gemma-data-assistant-v2/
│       └── MASTER.md
└── .streamlit/                     # Streamlit configuration
    └── config.toml
```

### Key Files

| File | Purpose |
|------|---------|
| `app.py` | Single-file Streamlit app with all logic |
| `translations.py` | Translation dictionary (EN/AR) with `t()` helper |
| `llama-opencode.bat` | Optimized for RTX 4060 8GB: flash attn, KV cache quantization |
| `start_llama_server.bat` | Legacy launcher — auto-detects model from HuggingFace cache |
| `run_app.bat` | Creates venv, installs deps, runs app |
| `AGENTS.md` | Technical documentation for AI agents |
| `requirements.txt` | All Python dependencies including `arabic-reshaper` + `python-bidi` |

---

## ⚠️ Known Limitations

### Voice Input — Fully Offline
The voice-to-text feature now uses Gemma 4 E4B's **native ASR** via llama-server's `/v1/audio/transcriptions` endpoint. All processing is done locally — no internet connection required.

Since llama.cpp merged the Gemma 4 audio conformer encoder (PR #21421) and the OpenAI-compatible transcription API (PR #21863), the former limitations are resolved. Voice input works completely offline with support for both English and Arabic.

For full details, see [AUDIO_STATUS.md](AUDIO_STATUS.md).

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

<br><br>

# 💎 مساعد البيانات متعدد الوسائط Gemma 4 E4B

[🇺🇸 English](README.md) | [🇸🇦 العربية](#-مساعد-البيانات-متعدد-الوسائط-gemma-4-e4b)

<div align="right">

**تطبيق ذكاء اصطناعي محلي ووكيل (Agentic) لتحليل البيانات الخاصة باستخدام نموذج Google Gemma 4 E4B مع قدرات متعددة الوسائط.**

[المميزات](#-المميزات) • [البدء السريع](#-البدء-السريع) • [المعمارية](#-المعمارية) • [الاستخدام](#-الاستخدام) • [الإعدادات](#-الإعدادات) • [المساهمة](#-المساهمة)

</div>

---

## 📋 جدول المحتويات

- [نظرة عامة](#-نظرة-عامة)
- [المميزات](#-المميزات)
- [البدء السريع](#-البدء-السريع)
  - [المتطلبات الأساسية](#المتطلبات-الأساسية)
  - [التثبيت](#التثبيت)
  - [تشغيل التطبيق](#تشغيل-التطبيق)
- [المعمارية](#-المعمارية)
- [الاستخدام](#-الاستخدام)
  - [رفع البيانات وتحليلها](#رفع-البيانات-وتحليلها)
  - [الأوامر الصوتية](#الأوامر-الصوتية)
  - [التحليل البصري](#التحليل-البصري)
  - [استخدام الأدوات الذكية](#استخدام-الأدوات-الذكية)
- [الإعدادات](#-الإعدادات)
  - [إعداد llama-server](#إعداد-llama-server)
  - [إعداد الوسائط المتعددة](#إعداد-الوسائط-المتعددة)
  - [إعدادات Streamlit](#إعدادات-streamlit)
- [هيكل المشروع](#-هيكل-المشروع)
- [المساهمة](#-المساهمة)
- [الترخيص](#-الترخيص)
- [التقدير والشكر](#-التقدير-والشكر)

---

## 🌟 نظرة عامة

مساعد بيانات Gemma هو تطبيق Streamlit جاهز للإنتاج يتيح **تحليل البيانات بشكل خاص ومحلي** باستخدام نموذج Google Gemma 4 E4B. على عكس الحلول السحابية، تتم جميع عمليات المعالجة على جهازك—مما يضمن الخصوصية الكاملة للبيانات مع تقديم أحدث قدرات الذكاء الاصطناعي.

يعتمد التطبيق على:
- **Per-Layer Embeddings (PLE)** للاستدلال الفعال بنموذج 4 مليار معلمة.
- **تفكير متعدد الوسائط أصلي** للمدخلات الصوتية والبصرية والنصية.
- **نافذة سياق 128K** لتحليل مجموعات البيانات الكبيرة.
- **تنفيذ أدوات ذكية** لتوليد الأكواد والرسوم البيانية بشكل تلقائي.

---

## ✨ المميزات

### 🧠 تفكير متقدم
- عرض حي لطريقة تفكير الذكاء الاصطناعي عبر معالجة رمز `<|think|>`.
- عمق تفكير قابل للتعديل: سريع، قياسي، أو تحليل عميق.
- التصحيح الذاتي والتحقق الداخلي من الحسابات قبل الرد.

### 🤖 وكيل بيانات مستقل
- **تصور ديناميكي**: إنشاء رسوم بيانية Matplotlib/Seaborn عند الطلب.
- **تنفيذ الكود**: يقوم الذكاء الاصطناعي بكتابة وتنفيذ كود Python باستخدام `pandas`, `matplotlib`, `seaborn`.
- **تحويل البيانات**: تصفية متعددة الخطوات، تجميع، وتحليل إحصائي.
- **نتائج مستمرة**: الرسوم البيانية والجداول تظل موجودة حتى بعد إعادة تشغيل الجلسة.

### 🎙️ مدخلات متعددة الوسائط
- **تحويل الصوت إلى نص**: التعرف على الكلام بدون إنترنت عبر ASR الأصلي لـ Gemma 4 E4B
- **تحليل الصور**: رفع لقطات الشاشة أو الرسوم البيانية للمقارنة والتحليل.
- **دردشة نصية**: واجهة محادثة تقليدية مع وعي كامل بالسياق.

### 📊 ذكاء البيانات
- **بروفايل تلقائي**: اكتشاف المخطط (Schema)، أنواع الأعمدة، وملخصات إحصائية (المتوسط، المجموع، إلخ).
- **تحسين السياق**: وضع "السياق السريع" (أول 100 صف + إحصائيات كاملة) لتقليل وقت الاستجابة بنسبة 70%.
- **قدرات التصدير**: تحميل البيانات المحولة كملفات Excel.
- **بيانات تجريبية**: 5 مجموعات بيانات محملة مسبقاً للاختبار الفوري.

### 🌐 دعم ثنائي اللغة (إنجليزي / عربي)
- **واجهة عربية كاملة**: ترجمة جميع العناوين والأزرار والرسائل.
- **تخطيط RTL**: دعم كامل للتخطيط من اليمين إلى اليسار في الوضع العربي.
- **رسوم بيانية عربية**: رسوم Matplotlib مع نص عربي معالج بشكل صحيح (reshaping + bidi).
- **تبديل لغة ديناميكي**: التنقل بين الإنجليزية والعربية فوراً دون إعادة تشغيل.
- **دعم الخطوط العربية**: اكتشاف تلقائي لخط Noto Sans Arabic أو العودة لخطوط النظام (Arial, Tahoma).

### 🎨 واجهة مستخدم احترافية
- **الوضع الداكن**: نظام تصميم مستوحى من Google DeepMind.
- **فحص الحالة**: التحقق من الاتصال بالخادم.
- **عداد السياق**: عرض استهلاك الرموز (Tokens) في الوقت الفعلي.

---

## 🚀 البدء السريع

### المتطلبات الأساسية

| المتطلب | التفاصيل |
|-------------|---------|
| **Python** | 3.10 أو أعلى |
| **RAM** | 8 جيجابايت كحد أدنى، 16 جيجابايت مستحسن (لسياق 128K) |
| **llama.cpp** | مثبت مع ملف `llama-server` |
| **النموذج** | Gemma 4 E4B GGUF من [Unsloth HuggingFace](https://huggingface.co/unsloth/gemma-4-e4b-it-gguf) |
| **نظام التشغيل** | Windows, macOS, أو Linux |

### التثبيت

1. **نسخ المستودع**:
```bash
git clone https://github.com/malgaroshy-maker/gemma4-data-assistant.git
cd gemma4-data-assistant
```

2. **تثبيت التبعيات**:
```bash
# باستخدام المشغل التلقائي (ينشئ بيئة افتراضية)
./run_app.bat  # Windows
# أو يدوياً:
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### تشغيل التطبيق

**الخطوة 1: تشغيل llama-server**
```bash
# استخدم المشغل المحسن (موصى به لـ RTX 4060 8GB)
./llama-opencode.bat

# أو استخدم المشغل القديم
./start_llama_server.bat

# أو التشغيل يدوياً (حدث المسارات لمكان النموذج لديك)
llama-server \
  -m "path/to/gemma-4-E4B-it-Q4_K_XL.gguf" \
  --mmproj "path/to/mmproj-BF16.gguf" \
  --ctx-size 131072 \
  --port 8080
```

**الخطوة 2: تشغيل تطبيق Streamlit**
```bash
streamlit run app.py
```

---

## 🌐 تدويل التطبيق (i18n)

### دعم اللغة العربية

يدعم التطبيق **الوضع ثنائي اللغة بالكامل** مع محول للغة في الشبيكة الجانبية.

**ما تم ترجمته:**
- جميع تسميات واجهة المستخدم والأزرار والعناوين.
- مكان نص الدردشة ورسائل الحالة.
- تنبيهات الخطأ والنجاح.
- النصائح الاحترافية ووصف العروض التجريبية.
- تسميات وعناوين الرسوم البيانية.

### تخطيط اليمين إلى اليسار (RTL)

يتضمن تنفيذ RTL:
- مرآة الشبيكة الجانبية إلى الجهة اليمنى.
- محاذاة رسائل الدردشة لليمين.
- محاذاة الجداول والمقاييس لليمين.
- تظل كتل الأكواد من اليسار لليمن (للحفاظ على قابلية قراءة Python).

---

## 📁 هيكل المشروع

```
gemma4-data-assistant/
├── app.py                          # تطبيق Streamlit الرئيسي (~990 سطر)
├── translations.py                 # قاموس الترجمة ثنائي اللغة (EN/AR)
├── start_llama_server.bat          # مشغل الخادم مع اكتشاف تلقائي
├── run_app.bat                     # مشغل التطبيق لويندوز
├── requirements.txt                # التبعيات (تتضمن مكتبات المعالجة العربية)
├── AGENTS.md                       # دليل الوكلاء المساعدين
└── .streamlit/                     # إعدادات Streamlit
    └── config.toml
```

---

## ⚠️ القيود المعروفة

### إدخال الصوت — يعمل بدون إنترنت بالكامل
ميزة تحويل الصوت إلى نص تستخدم الآن ASR الأصلي لـ Gemma 4 E4B عبر واجهة `/v1/audio/transcriptions` في llama-server. كل المعالجة محلية — لا حاجة للإنترنت.

منذ أن دمج llama.cpp مشفر الصوت Conformer لـ Gemma 4 (PR #21421) وواجهة الترجمة الصوتية المتوافقة مع OpenAI (PR #21863)، تم حل القيود السابقة. الإدخال الصوتي يعمل بدون إنترنت مع دعم اللغتين الإنجليزية والعربية.

لمزيد من التفاصيل، انظر [AUDIO_STATUS.md](AUDIO_STATUS.md).

---

## 🤝 المساهمة

المساهمات مرحب بها! إليك كيف يمكنك المساعدة:

1. **عمل Fork للمستودع**
2. **إنشاء فرع للميزة**: `git checkout -b feature/amazing-feature`
3. **اعتماد التغييرات**: `git commit -m 'feat: add amazing feature'`
4. **فتح طلب سحب (Pull Request)**

---

## 📄 الترخيص

هذا المشروع مرخص بموجب رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

---

## 🙏 التقدير والشكر

- **Google DeepMind** لسلسلة نماذج Gemma 4.
- **llama.cpp** لمحرك الاستدلال الرائع.
- **Streamlit** لإطار عمل واجهة المستخدم.
- **Unsloth** لتحويلات نماذج GGUF المحسنة.

---

<div align="center">

**تم التطوير بواسطة [Mahamed Algaroshy](https://github.com/malgaroshy-maker)**  
*مهندس كهربائي ومطور ذكاء اصطناعي*

[⭐ Star this repo](https://github.com/malgaroshy-maker/gemma4-data-assistant/stargazers) • [🐛 Report Bug](https://github.com/malgaroshy-maker/gemma4-data-assistant/issues)

</div>
