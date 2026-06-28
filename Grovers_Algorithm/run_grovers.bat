@echo off
echo ==================================================
echo   Grover's Search Algorithm
echo   Installing dependencies...
echo ==================================================
echo.
pip install qiskit qiskit-aer --quiet
echo.
echo Dependencies installed. Starting simulation...
echo.
python grovers_algorithm.py
pause
