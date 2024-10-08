@echo off
:: Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Downloading and installing Python...
    
    :: Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    
    :: Install Python silently for the current user
    start /wait python-installer.exe InstallAllUsers=0 PrependPath=1
    
    :: Cleanup
    del python-installer.exe
)
:: Check for pip
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --user
)
:: Check for Pillow (required for image processing)
python -m pip show Pillow >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Pillow...
    python -m pip install --user Pillow
)

:: Check for ttkbootstrap (required for styling)
python -m pip show ttkbootstrap >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing ttkbootstrap...
    python -m pip install --user ttkbootstrap
)

:: Run the Python script
python gui_maker.py
