@echo off
echo ======================================================================
echo   PAWPATROL DRL Retraining - Comprehensive Coverage
echo ======================================================================
echo.
echo This will train a NEW DRL model that handles ALL infection scenarios
echo from 0%% to 90%% without needing fallback rules.
echo.
echo Training Configuration:
echo   - Timesteps: 500,000 (extended training)
echo   - Duration: ~45-60 minutes
echo   - Infection scenarios: 0%% to 90%% (diverse)
echo   - Reward: Fixed (infection reduction, not absolute)
echo.
echo Press Ctrl+C now to cancel, or
pause

echo.
echo Starting training...
echo.

cd drl
python train_dqn.py

echo.
echo ======================================================================
echo   Training Complete!
echo ======================================================================
echo.
echo Next steps:
echo   1. Restart the backend: python main.py
echo   2. Test in the frontend (run simulation + get AI recommendations)
echo.
pause
