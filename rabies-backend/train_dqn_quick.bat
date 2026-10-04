@echo off
REM ============================================================================
REM Quick DQN Training Script
REM Trains DQN model with standard settings (100K timesteps, ~10-15 minutes)
REM ============================================================================

echo.
echo ============================================================================
echo   PAWPATROL - DQN Training (Standard)
echo ============================================================================
echo.
echo   This will train a DQN model for rabies vaccination optimization.
echo   Training time: ~10-15 minutes on CPU
echo   Timesteps: 100,000
echo.
echo   Press Ctrl+C to stop training at any time (model will be saved).
echo.
pause

python drl/train_dqn.py --preset standard

echo.
echo ============================================================================
pause
