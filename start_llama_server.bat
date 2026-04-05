@echo off
set MODEL_PATH="C:\Users\masal\.cache\huggingface\hub\models--unsloth--gemma-4-e4b-it-gguf\snapshots\315e03409eb1cdde302488d66e586dea1e82aad1\gemma-4-E4B-it-UD-Q4_K_XL.gguf"
set MMPROJ_PATH="C:\Users\masal\.cache\huggingface\hub\models--unsloth--gemma-4-e4b-it-gguf\snapshots\315e03409eb1cdde302488d66e586dea1e82aad1\mmproj-BF16.gguf"

echo Starting Gemma 4 E4B Server with Multimodal Support...
echo Model: %MODEL_PATH%
echo Projector: %MMPROJ_PATH%

llama-server -m %MODEL_PATH% --mmproj %MMPROJ_PATH% --ctx-size 131072 --port 8080
pause
