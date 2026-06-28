@echo off
echo ==================================================
echo   Quantum Password Cracker
echo   Powered by Grover's Algorithm
echo   Installing dependencies...
echo ==================================================
echo.
pip install qiskit qiskit-aer --quiet
echo.
echo Dependencies installed. Starting simulation...
echo.
python quantum_password_cracker.py
pause
