@echo off
REM ============================================================================
REM PAWPATROL DRL Setup Script
REM Installs all dependencies for Deep Reinforcement Learning
REM ============================================================================

echo.
echo ============================================================================
echo   PAWPATROL - DRL Installation Script
echo   Phase 1: Setup Dependencies
echo ============================================================================
echo.

REM Check Python
echo [1/7] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo    ✅ Python found
echo.

REM Upgrade pip
echo [2/7] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo    ⚠️  Warning: Could not upgrade pip, continuing anyway...
) else (
    echo    ✅ pip upgraded
)
echo.

REM Install PyTorch
echo [3/7] Installing PyTorch (this may take a few minutes)...
pip install torch==2.1.1 torchvision==0.16.1
if errorlevel 1 (
    echo    ❌ ERROR: Failed to install PyTorch
    pause
    exit /b 1
)
echo    ✅ PyTorch installed
echo.

REM Install Stable-Baselines3
echo [4/7] Installing Stable-Baselines3...
pip install stable-baselines3==2.2.1
if errorlevel 1 (
    echo    ❌ ERROR: Failed to install Stable-Baselines3
    pause
    exit /b 1
)
echo    ✅ Stable-Baselines3 installed
echo.

REM Install Gymnasium
echo [5/7] Installing Gymnasium...
pip install gymnasium==0.29.1
if errorlevel 1 (
    echo    ❌ ERROR: Failed to install Gymnasium
    pause
    exit /b 1
)
echo    ✅ Gymnasium installed
echo.

REM Install remaining dependencies
echo [6/7] Installing remaining dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo    ❌ ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo    ✅ All dependencies installed
echo.

REM Verify installation
echo [7/7] Verifying installation...
echo.

python -c "import torch; print(f'   ✅ PyTorch {torch.__version__}')"
python -c "import stable_baselines3 as sb3; print(f'   ✅ Stable-Baselines3 {sb3.__version__}')"
python -c "import gymnasium; print(f'   ✅ Gymnasium {gymnasium.__version__}')"
python -c "import numpy; print(f'   ✅ NumPy {numpy.__version__}')"
python -c "import scipy; print(f'   ✅ SciPy {scipy.__version__}')"

echo.
echo ============================================================================
echo   ✅ Installation Complete!
echo ============================================================================
echo.
echo   Next steps:
echo   1. Test configuration:  python drl/config.py
echo   2. Ready for Phase 2 (Environment Definition)
echo.
echo   To view training progress later, run:
echo   tensorboard --logdir=./drl/logs/tensorboard
echo.
echo ============================================================================
pause
