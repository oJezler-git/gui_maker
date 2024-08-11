@echo off

:: Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Downloading and installing Python...
    
    :: Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe
    
    :: Install Python silently
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    :: Cleanup
    del python-installer.exe
)

:: Check for pip
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pip is not installed. Installing pip...
    python -m ensurepip
)

:: Check for Pillow (required for image processing)
pip show Pillow >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Pillow...
    pip install Pillow
)

:: Run the Python script
python gui_maker.py
