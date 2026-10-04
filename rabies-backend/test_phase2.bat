@echo off
REM ============================================================================
REM Test Phase 2 Components
REM ============================================================================

echo.
echo ============================================================================
echo   Testing Phase 2: Environment and DQN Agent
echo ============================================================================
echo.

echo [1/3] Testing Configuration...
python drl/config.py
if errorlevel 1 (
    echo    ❌ Configuration test failed
    pause
    exit /b 1
)
echo.

echo [2/3] Testing Environment...
python drl/environment.py
if errorlevel 1 (
    echo    ❌ Environment test failed
    pause
    exit /b 1
)
echo.

echo [3/3] Testing DQN Agent Utilities...
python drl/dqn_agent.py
if errorlevel 1 (
    echo    ❌ DQN Agent test failed
    pause
    exit /b 1
)
echo.

echo ============================================================================
echo   ✅ All Phase 2 Tests Passed!
echo ============================================================================
echo.
echo   Phase 2 is complete and working correctly.
echo   Ready for Phase 3 (Training)!
echo.
pause
