@echo off
:: ============================================================
:: Gemma 4 E4B Server Launcher
:: ============================================================
:: This script finds the latest cached Gemma 4 model and starts
:: llama-server with multimodal support on port 8080.
::
:: To customize model paths, edit the MODEL_DIR and MMPROJ_DIR
:: variables below, or set them as environment variables.
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
set MODEL_PATH=%HF_CACHE%\%SNAPSHOT%\gemma-4-E4B-it-UD-Q4_K_XL.gguf
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
    echo ERROR: Multimodal projector not found: %MMPROJ_PATH%
    echo Voice/Vision features will be disabled.
    echo To enable, ensure mmproj-BF16.gguf is in the model directory.
    set MMPROJ_FLAG=
    goto start_server
)

set MMPROJ_FLAG=--mmproj %MMPROJ_PATH%

:start_server
echo ========================================
echo   Gemma 4 E4B Server Launcher
echo ========================================
echo.
echo Model: %MODEL_PATH%
echo Projector: %MMPROJ_PATH%
echo Context: 131072 tokens (128K)
echo Port: 8080
echo.
echo Starting llama-server...
echo.

llama-server -m %MODEL_PATH% %MMPROJ_FLAG% --ctx-size 131072 --port 8080
pause
