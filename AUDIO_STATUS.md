# 🎙️ Audio Input Status

## Current State: **Native Gemma 4 ASR (Fully Offline)**

Voice input now uses Gemma 4 E4B's **built-in ASR** via llama-server's `/v1/audio/transcriptions` API endpoint. No internet connection is required — all processing is done locally.

### How It Works
1. `st.audio_input()` captures microphone audio as WAV bytes
2. Audio is sent directly to `llama-server` via OpenAI-compatible `client.audio.transcriptions.create()`
3. Gemma 4's native audio encoder (Conformer) transcribes the speech
4. Transcribed text is displayed for user confirmation before sending to chat

### Requirements
- **llama-server** must be running with `--mmproj` flag (BF16 mmproj required for audio)
- The `mmproj-BF16.gguf` file must contain the audio encoder (confirmed in our setup)
- Maximum audio length: **30 seconds**

### llama.cpp Timeline
| PR/Issue | Title | Status |
|---|---|---|
| [#21421](https://github.com/ggml-org/llama.cpp/pull/21421) | mtmd: add Gemma 4 audio conformer encoder | **Merged** (Apr 2026) |
| [#21863](https://github.com/ggml-org/llama.cpp/pull/21863) | server: support OAI /v1/audio/transcriptions | **Merged** (Apr 2026) |
| [#21905](https://github.com/ggml-org/llama.cpp/pull/21905) | Fix reasoning leakage in transcription | **Merged** (Apr 2026) |

## What This Means

| Feature | Status |
|---|---|
| Voice Input | ✅ Works offline via Gemma 4 native ASR |
| Internet Required | ❌ No — 100% local processing |
| Arabic Voice | ✅ Supported (native multilingual ASR) |
| Privacy | ✅ Audio never leaves your machine |

## Fallback
If `llama-server` is not running or the transcription endpoint fails, the app shows a clear error message directing the user to start the server with `llama-opencode.bat`.
