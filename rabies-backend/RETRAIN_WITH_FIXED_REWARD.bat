@echo off
echo ========================================
echo RETRAIN DRL with FIXED Reward Function
echo ========================================
echo.
echo CHANGES MADE TO REWARD:
echo 1. Added PREVENTION PENALTY - penalizes low coverage with infections
echo 2. Added COVERAGE BONUS - rewards achieving 70%% WHO threshold
echo 3. Reduced vaccination cost during outbreaks
echo.
echo Training will take 30-60 minutes...
echo.
pause

cd drl
python train_dqn.py

echo.
echo ========================================
echo Training Complete!
echo ========================================
echo.
echo The model should now recommend:
echo - 70-80%% vaccination when there are infections
echo - NOT 0%% vaccination during outbreaks
echo.
pause
