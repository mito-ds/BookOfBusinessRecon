@echo off
REM Script to run a Streamlit application after setup

REM Check if the virtual environment directory exists
if not exist "venv" (
    echo Error: The virtual environment does not exist. Please run setup.bat first.
    exit /b 1
)

REM Activate the virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate the virtual environment.
    exit /b 1
)

REM Run the Streamlit app
streamlit run app.py