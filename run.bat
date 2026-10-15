@echo off
TITLE OmniGen-NIM Launcher

echo [1/2] Checking Local Ollama Server...
netstat -ano | findstr :11434 >nul
if %errorlevel% equ 0 (
    echo Ollama is already active in the background.
) else (
    echo Starting Ollama Server...
    start /b ollama serve >nul 2>&1
    timeout /t 3 /nobreak > nul
)

echo [2/2] Launching Streamlit Dashboard...
cd /d "%~dp0"
"D:\Miniconda\python.exe" -m streamlit run app\dashboard.py
pause