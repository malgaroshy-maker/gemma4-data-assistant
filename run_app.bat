@echo off
echo Starting Data Analyzer AI Environment...

REM Check if virtual environment exists
if not exist ".venv\Scripts\Activate.ps1" (
    echo Virtual environment not found. Please wait while it is created...
    python -m venv .venv
    echo Installing dependencies...
    call .venv\Scripts\activate.bat
    pip install streamlit==1.40.0 pandas==2.2.3 openpyxl==3.1.5 openai==1.54.0 tiktoken==0.8.0 tabulate==0.9.0 httpx==0.27.2
) else (
    call .venv\Scripts\activate.bat
)

echo Starting Streamlit App...
streamlit run app.py
