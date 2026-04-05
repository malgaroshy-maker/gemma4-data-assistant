# 💎 Gemma 4 E4B: Frontier Multimodal Data Assistant

> **A local-first, agentic demonstration of Google's April 2026 Gemma 4 series.**

This project is a high-end technical showcase of the **Gemma 4 E4B** model. It demonstrates how a compact, "effective" 4-billion parameter model can outperform traditional LLMs by leveraging Per-Layer Embeddings (PLE) and native multimodal reasoning directly on local consumer hardware.

---

## 🚀 Frontier Capabilities on Display

### 🧠 1. Native Reasoning Engine (`<|think|>`)
Unlike standard chat models, Gemma 4 E4B features a dedicated reasoning budget. In this app, you can watch the AI's "internal monologue" in real-time. It explores hypotheses, performs internal math checks, and self-corrects before providing a final answer.

### 🤖 2. Autonomous Data Agent (Tool Use)
This isn't just a chatbot—it's a data engineer. Gemma autonomously writes and executes Python code to:
- **Generate Visualizations:** Create complex Matplotlib and Seaborn charts on the fly.
- **Transform Data:** Perform multi-step filtering and grouping directly on your uploaded files.
- **Export Results:** Generate downloadable Excel subsets of its analytical findings.

### 🎙️ 3. Native Multimodal Support
Gemma 4 E4B "sees" and "hears" without external models:
- **Audio Inputs:** Ask questions about your data using your voice via the built-in microphone.
- **Vision Inputs:** Upload screenshots of dashboards or external charts to compare them with your raw spreadsheet data.

### 📏 4. 128K Context Breakthrough
The E4B variant handles massive datasets that would crash smaller models. With a native 128,000 token context window, it maintains a holistic "memory" of your entire file throughout the conversation.

---

## 🎨 Polished Gemma Experience
The app features a custom UI designed to match the **Google DeepMind** aesthetic:
- **🩺 Gemma Health Check:** Instant data profiling (duplicates, nulls, types) upon upload.
- **📊 Context Meter:** Real-time visualization of the 128K context window usage.
- **⚡ Performance First:** Optimized for low-end devices without sacrificing reasoning depth.

---

## 🛠️ Quick Start

### 1. Requirements
- **Hardware:** 8GB+ RAM (16GB recommended for 128k context).
- **Server:** `llama-server` (llama.cpp) running the GGUF version of Gemma 4 E4B.

### 2. Start the Engine
To use multimodal features (Voice/Vision), you MUST include the `--mmproj` flag. I have created a `start_llama_server.bat` file for you that uses the correct paths:
```bash
# Just run the batch file:
./start_llama_server.bat

# Or use the manual command:
llama-server -m "C:\Users\masal\.cache\huggingface\hub\models--unsloth--gemma-4-e4b-it-gguf\snapshots\315e03409eb1cdde302488d66e586dea1e82aad1\gemma-4-E4B-it-UD-Q4_K_XL.gguf" --mmproj "C:\Users\masal\.cache\huggingface\hub\models--unsloth--gemma-4-e4b-it-gguf\snapshots\315e03409eb1cdde302488d66e586dea1e82aad1\mmproj-BF16.gguf" --ctx-size 131072 --port 8080
```

### 3. Launch the Demo
Simply double-click `run_app.bat` or run:
```bash
streamlit run app.py
```

---
*Developed by **Mahamed Algaroshy**, an electrical engineer and AI enthusiast dedicated to building software that leverages AI tools to enhance people's lives.*

*Created as a technical demo for the Google Gemma 4 Model Series (April 2026).*
