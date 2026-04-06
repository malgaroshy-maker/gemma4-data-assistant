# 🎙️ Audio Input Status

## Current State

**Voice input currently requires an internet connection.** The app uses Google's free Speech-to-Text API via the `SpeechRecognition` library (`recognize_google()`). Your audio is sent to Google's servers for transcription and the text result is returned to the app.

**No audio data is stored or shared** — it's only used for real-time transcription and immediately discarded.

## Limitation

Gemma 4 E4B has **native audio (ASR) support** built into the model, but **llama.cpp does not yet properly route audio input to Gemma 4** through its server API. This is a known issue being actively tracked:

- **GitHub Issue**: [llama.cpp #21325](https://github.com/ggml-org/llama.cpp/issues/21325) — "Eval bug: Gemma 4 audio support is missing"
- **GitHub Discussion**: [llama.cpp #21334](https://github.com/ggml-org/llama.cpp/discussions/21334) — "How to input audio to Gemma 4 E4B?"
- **Related PR**: [llama.cpp #21421](https://github.com/ggml-org/llama.cpp/pull/21421) — Audio processing for Gemma 4 conformer encoder (currently "Changes requested")

The mmproj file (`mmproj-gemma-4-e4b-it-f16.gguf`) **does contain an audio encoder** (confirmed by llama.cpp logs: `clip_model_loader: has audio encoder`), but the server-side routing is not yet implemented.

## Planned Solutions

We are working on two paths to achieve **fully offline voice recognition**:

### Path 1: Faster-Whisper (Recommended — Coming Soon)
- **What**: Integrate [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) using CTranslate2 backend
- **Benefits**: Fully offline, supports Arabic, fast inference on CPU/GPU, production-ready
- **Integration**: Replaces `SpeechRecognition.recognize_google()` with local transcription
- **Model size**: ~400MB for medium model (good accuracy/speed balance)
- **Arabic support**: Excellent — Whisper was trained on 99 languages including Arabic

### Path 2: Native Gemma 4 ASR via llama.cpp (Future)
- **What**: Once llama.cpp merges PR #21421 and resolves issue #21325, we'll switch to native audio
- **Benefits**: No additional dependencies, single model handles everything
- **Timeline**: Depends on llama.cpp development — actively being worked on
- **Status**: Blocked on PR review and CI approval

## What This Means for You

| Feature | Current | Planned |
|---------|---------|---------|
| Voice Input | ✅ Works (requires internet) | ✅ Fully offline |
| Arabic Voice | ⚠️ Limited (Google API) | ✅ Excellent (Whisper) |
| Privacy | ⚠️ Audio sent to Google | ✅ 100% local |
| Offline Use | ❌ Not supported | ✅ Fully supported |

## Workaround for Offline Use

If you need to use the app completely offline right now:
1. Type your queries manually instead of using voice input
2. All other features (data analysis, charts, image upload, text chat) work fully offline

## Tracking Progress

Watch these links for updates:
- [llama.cpp #21325](https://github.com/ggml-org/llama.cpp/issues/21325) — Audio support issue
- [llama.cpp #21421](https://github.com/ggml-org/llama.cpp/pull/21421) — Audio processing PR
- Our [GitHub Issues](https://github.com/malgaroshy-maker/gemma4-data-assistant/issues) — Faster-Whisper integration tracking
