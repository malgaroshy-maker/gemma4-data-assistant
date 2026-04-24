@echo off
:: ============================================================
:: Optimized Gemma 4 E4B Server — RTX 4060 8GB / 16GB RAM
:: ============================================================
:: Hardware: Ryzen 7 7435HS (8C) + RTX 4060 Laptop (8GB VRAM)
:: Model: Gemma 4 E4B Q4_K_XL (~3-4GB weights)
:: Context: 128K tokens (131072) with KV cache quantization
::
:: Optimizations applied:
::   --gpu-layers 99        Full GPU offload (all 42 layers)
::   --flash-attn on        Flash Attention (speed + VRAM savings)
::   --cache-type-k q4_0    KV key quantization (75%% less VRAM)
::   --cache-type-v q4_0    KV value quantization (75%% less VRAM)
::   --threads 8            Match Ryzen 7 physical cores
::   --threads-batch 8      Batch processing threads
::   --batch-size 512       Prompt processing throughput
::   --ubatch-size 512      Micro-batch for smooth generation
::   --swa-full             Full-size sliding window cache (Gemma 4 specific)
::   --prio 2               High process priority for smoother inference
::   --mlock                Lock model in RAM (prevent Windows compression)
::   --fit-target 512       Tighter VRAM margin (512 vs 1024 MiB default)
:: ============================================================

set HF_CACHE=%USERPROFILE%\.cache\huggingface\hub\models--unsloth--gemma-4-e4b-it-gguf\snapshots

:: Use environment variable if set, otherwise auto-detect
if defined MODEL_PATH goto check_mmproj
if defined MMPROJ_PATH goto start_server

:: Auto-detect latest snapshot
if not exist "%HF_CACHE%" (
    echo ERROR: HuggingFace cache not found at:
    echo   %HF_CACHE%
    echo.
    echo Please download the model first:
    echo   https://huggingface.co/unsloth/gemma-4-e4b-it-gguf
    pause
    exit /b 1
)

:: Find the latest snapshot directory
for /f "delims=" %%D in ('dir /b /ad /o-n "%HF_CACHE%" 2^>nul') do (
    set SNAPSHOT=%%D
    goto found_snapshot
)

echo ERROR: No snapshot found in %HF_CACHE%
echo Please download the model first.
pause
exit /b 1

:found_snapshot
:: Try multiple model filename patterns (UD and non-UD variants)
set MODEL_PATH=%HF_CACHE%\%SNAPSHOT%\gemma-4-E4B-it-UD-Q4_K_XL.gguf
if not exist %MODEL_PATH% set MODEL_PATH=%HF_CACHE%\%SNAPSHOT%\gemma-4-E4B-it-Q4_K_XL.gguf
if not exist %MODEL_PATH% (
    :: Try to find any matching GGUF file
    for %%F in ("%HF_CACHE%\%SNAPSHOT%\gemma-4-E4B-it-*.gguf") do (
        set MODEL_PATH=%%F
        goto found_model
    )
    echo ERROR: No Gemma 4 model GGUF found in snapshot directory.
    pause
    exit /b 1
)
:found_model
set MMPROJ_PATH=%HF_CACHE%\%SNAPSHOT%\mmproj-BF16.gguf

:check_mmproj
if not exist %MODEL_PATH% (
    echo ERROR: Model file not found: %MODEL_PATH%
    echo.
    echo Please edit this batch file and set MODEL_PATH to your model location.
    pause
    exit /b 1
)

if not exist %MMPROJ_PATH% (
    echo WARNING: Multimodal projector not found: %MMPROJ_PATH%
    echo Voice/Vision features will be disabled.
    echo To enable, ensure mmproj-BF16.gguf is in the model directory.
    set MMPROJ_FLAG=
    goto start_server
)

set MMPROJ_FLAG=--mmproj %MMPROJ_PATH%

:start_server
echo ================================================
echo   Gemma 4 E4B — Optimized for RTX 4060 8GB
echo ================================================
echo.
echo Model:      %MODEL_PATH%
echo Projector:  %MMPROJ_PATH%
echo Context:    131072 tokens (128K)
echo GPU Layers: 99 (full offload, auto-capped at 42)
echo Flash Attn: enabled
echo KV Cache:   q4_0 quantized (keys + values)
echo SWA Cache:  full-size (Gemma 4 sliding window)
echo Threads:    8 / 8 (generation / batch)
echo Priority:   high
echo Memlock:    enabled
echo Batch:      512 / 512 (batch / ubatch)
echo Port:       8080
echo.
echo Estimated VRAM usage:
echo   Model weights:    ~3.5 GB
echo   Vision encoder:   ~0.3 GB
echo   Audio encoder:    ~0.6 GB
echo   KV cache (128K):  ~2.5 GB (q4_0 compressed)
echo   Total:            ~7.0 GB / 8.0 GB
echo.
rem Speculative decoding — 1.3-1.5x generation speedup (ngram-based, no draft model needed)
echo Speculative: enabled (ngram-cache)
echo.
echo Starting llama-server...

llama-server -m %MODEL_PATH% %MMPROJ_FLAG% ^
  --ctx-size 131072 ^
  --gpu-layers 99 ^
  --flash-attn on ^
  --cache-type-k q4_0 ^
  --cache-type-v q4_0 ^
  --threads 8 ^
  --threads-batch 8 ^
  --batch-size 512 ^
  --ubatch-size 512 ^
  --swa-full ^
  --prio 2 ^
  --mlock ^
  --fit-target 512 ^
  --spec-type ngram-cache ^
  --spec-ngram-size-n 12 ^
  --spec-ngram-size-m 48 ^
  --spec-ngram-min-hits 2 ^
  --draft-n 16 ^
  --port 8080

pause
