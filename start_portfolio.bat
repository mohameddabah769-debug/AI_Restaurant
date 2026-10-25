@echo off
title Eng. Mohamed Dabah - 3D AI Portfolio
color 0b
echo ===================================================
echo     ENG / MOHAMED DABAH - 3D AI PORTFOLIO
echo ===================================================
echo Starting Python FastAPI Server...
echo Opening your 3D Portfolio in your browser...
echo.

cd /d "%~dp0"
.\venv\Scripts\python.exe portfolio\run.py
pause
