# Start Data Analyzer AI

# Check if virtual environment exists
if (!(Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Please wait while it is created..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
    pip install streamlit==1.40.0 pandas==2.2.3 openpyxl==3.1.5 openai==1.54.0 tiktoken==0.8.0 tabulate==0.9.0 httpx==0.27.2
} else {
    & .venv\Scripts\Activate.ps1
}

Write-Host "Starting Streamlit App..." -ForegroundColor Green
streamlit run app.py