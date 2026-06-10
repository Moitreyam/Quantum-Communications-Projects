@echo off
echo ==================================================
echo   BB84 Quantum Key Distribution Protocol
echo   Installing dependencies...
echo ==================================================
echo.
pip install qiskit qiskit-aer --quiet
echo.
echo Dependencies installed. Starting simulation...
echo.
python bb84_protocol.py
pause
