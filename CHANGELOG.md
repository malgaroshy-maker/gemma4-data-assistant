# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.1.0] - 2026-04-05

### Added
- Full Arabic language support with RTL layout
- Bilingual translation system (`translations.py`)
- Arabic chart text rendering (`arabic-reshaper` + `python-bidi`)
- Dynamic language switching without restart
- Auto-detecting Noto Sans Arabic font from Windows font directories
- `plt.show()` stripping from AI-generated code
- `print()` wrapper to capture DataFrame outputs in tool execution
- Max upload size configuration (200MB)
- Python and error checking in launchers

### Fixed
- Image upload infinite loop (MD5 hash deduplication)
- OpenAI client recreation on every rerun
- Fragile JSON parsing (regex-based extraction)
- Hardcoded Windows username in `start_llama_server.bat`
- Tables showing on every tool call (even chart-only requests)
- Missing dependencies in `requirements.txt`
- External CDN dependency (Google Fonts removed)
- Context meter, demo buttons, and status messages not translated

### Changed
- `start_llama_server.bat` auto-detects latest HuggingFace snapshot
- System fonts instead of Google Fonts for 100% offline operation
- Improved launcher scripts with Python detection and error handling

## [Unreleased]

## [1.0.0] - 2026-04-05

### Added
- Initial release
- Streamlit app with Gemma 4 E4B via llama-server
- CSV/Excel file upload and analysis
- Voice-to-text input (SpeechRecognition)
- Image upload for multimodal analysis
- Agentic Python code execution tool
- Matplotlib/Seaborn chart generation with persistence
- Fast Context mode (100 rows + statistics)
- Demo datasets (5 pre-loaded)
- Dark mode UI with DeepMind-inspired design
- Reasoning depth selector (Quick, Standard, Deep Analysis)
- Export to Excel functionality
- Health check for server connectivity
