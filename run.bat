@echo off

:: Set installation directory
set "INSTALL_DIR=%USERPROFILE%\Python"

:: Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Downloading and installing Python...
    
    :: Download Python installer
    curl -o python-installer.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
    
    :: Install Python silently to user directory
    start /wait python-installer.exe InstallAllUsers=0 TargetDir="%INSTALL_DIR%" PrependPath=1
    
    :: Cleanup
    del python-installer.exe

    :: Add Python to PATH for this session
    setx PATH "%PATH%;%INSTALL_DIR%;%INSTALL_DIR%\Scripts"
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

:: Check for ttkbootstrap (required for styling)
pip show ttkbootstrap >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing ttkbootstrap...
    pip install ttkbootstrap
)

:: Run the Python script
python gui_maker.py
