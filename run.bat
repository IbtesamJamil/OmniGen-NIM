@echo off
TITLE OmniGen-NIM Master Launcher
:: Switch to the D drive and navigate to project root
D:
cd /d D:\OmniGen-NIM

:: Activate the clean virtual environment
call venv_clean\Scripts\activate

echo ===================================================
echo   Starting OmniGen-NIM Bioinformatics Platform
echo ===================================================

:: Launch the Celery background worker in a separate window using the solo pool
echo [1/2] Launching Celery background worker (Solo Pool)...
start cmd /k "TITLE Celery Worker & D: && cd /d D:\OmniGen-NIM && venv_clean\Scripts\activate && celery -A pipeline.celery_app worker --loglevel=info -P solo"

:: Brief pause to let the worker establish its SQLite connection
timeout /t 2 >nul

:: Launch the Streamlit dashboard in the primary window
echo [2/2] Launching Streamlit Dashboard...
streamlit run app/dashboard.py

pause