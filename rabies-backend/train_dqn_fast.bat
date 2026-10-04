@echo off
REM ============================================================================
REM Fast DQN Training Script
REM Trains DQN model with fast settings (10K timesteps, ~2-5 minutes)
REM Good for testing!
REM ============================================================================

echo.
echo ============================================================================
echo   PAWPATROL - DQN Training (FAST - For Testing)
echo ============================================================================
echo.
echo   This will train a DQN model quickly for testing purposes.
echo   Training time: ~2-5 minutes on CPU
echo   Timesteps: 10,000
echo.
echo   Note: This is for testing only. Use standard training for best results.
echo.
pause

python drl/train_dqn.py --preset fast

echo.
echo ============================================================================
pause
