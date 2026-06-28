@echo off
echo ==================================================
echo   Superdense Coding Protocol
echo   Installing dependencies...
echo ==================================================
echo.
pip install qiskit qiskit-aer --quiet
echo.
echo Dependencies installed. Starting simulation...
echo.
python superdense_coding.py
pause
