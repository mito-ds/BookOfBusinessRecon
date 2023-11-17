@echo off
REM Check for Python version and set up a virtual environment

REM Check for Python existence
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python.
    exit /b 1
)

REM Get Python version
for /f "delims=" %%i in ('python -c "import platform; print(platform.python_version())"') do set PYTHON_VERSION=%%i

REM Check Python version
echo Found Python version %PYTHON_VERSION%
if "%PYTHON_VERSION%" lss "3.8" (
    echo Error: Python version is too old. Please install Python between 3.8 and 3.11.
    exit /b 1
) else if "%PYTHON_VERSION%" gtr "3.11" (
    echo Error: Python version is too new. Please install Python between 3.8 and 3.11.
    exit /b 1
)

REM Create a virtual environment
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create a virtual environment.
    exit /b 1
)

REM Activate the virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate the virtual environment.
    exit /b 1
)

REM Install requirements from requirements.txt
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements.
    exit /b 1
)

echo Setup completed successfully.
pause