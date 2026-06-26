@echo off
echo ==================================================
echo   Quantum Teleportation Protocol
echo   Installing dependencies...
echo ==================================================
echo.
pip install qiskit qiskit-aer --quiet
echo.
echo Dependencies installed. Starting simulation...
echo.
python quantum_teleportation.py
pause
