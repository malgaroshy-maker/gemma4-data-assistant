# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.2.1] - 2026-04-25

### Added
- **Context window management**: Token counting before API calls, automatic old-message trimming when nearing 128K limit
- **Context meter in sidebar**: Shows combined data + conversation token usage with overflow warning
- **Sandbox hardening**: `__import__` blocked; 12 safe modules pre-imported (`datetime`, `numpy`, `dataframe_to_rows`, `Image`, etc.)
- **Message cap**: Auto-trims to 50 most recent messages to prevent session state bloat
- **Multi-figure capture**: All matplotlib figures saved individually, not just the last one
- **Speculative decoding** enabled in `llama-opencode.bat` (~1.3x speedup via ngram-cache)
- Context trimming final safety valve (truncates system prompt if still over limit)

### Changed
- **System prompt rewritten**: Cleaner rules, error-handling guidance, number formatting, pre-imported module instructions
- **Excel detection**: Now scans for xlsx ZIP magic bytes (`PK` header) on `BytesIO` objects only (avoids StringIO corruption)
- Tool description updated: mentions all pre-imported modules, no import statements needed

### Fixed
- `</think>` data loss: trailing text after closing think tag in same chunk is now preserved
- `response_format="json"` for llama-server transcription endpoint (was `"text"` causing 400 errors)
- `type(open("dummy","rb"))` crash replaced with proper `BytesIO` type check
- `plt`/`sns` code-splitting regex no longer breaks assignments (`fig, ax = plt.subplots()`)
- JSON parse crash: malformed tool-call arguments now shown as warning, partial content preserved

### Removed
- 4 orphaned translation keys (`analyze_media`, `voice_requires_internet`, `speech_error`, `voice_input_label`)

## [1.2.0] - 2026-04-24

### Added
- **Native Gemma 4 ASR** for fully offline voice recognition via `/v1/audio/transcriptions` endpoint
- **AI-generated Excel reports** with tables and charts (openpyxl in tool execution context)
- **Optimized `llama-opencode.bat`** server launcher for RTX 4060 8GB (flash attn, KV cache quantization, full GPU offload)
- Download button for AI-generated Excel reports in chat history

### Changed
- Voice input: replaced Google Speech-to-Text with native Gemma 4 ASR (100% offline)
- `openpyxl` added to tool execution globals (`execute_python_code`)
- System prompt updated with Excel report generation instructions
- Tool schema now includes Excel creation capability
- Updated translations (voice labels now indicate "Fully offline")

### Removed
- `SpeechRecognition` from requirements.txt (no longer needed)
- Internet requirement for voice input

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

### Planned
- Multi-model support
- Enhanced chart customization options

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
