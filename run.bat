@echo off

:: Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Installing Python...
    :: Add code here to download and install Python
    exit /b
)

:: Check for pip
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Installing pip...
    python -m ensurepip
)

:: Check for Pillow
pip show Pillow >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Pillow...
    pip install Pillow
)

:: Run the Python script
python gui_maker.py
