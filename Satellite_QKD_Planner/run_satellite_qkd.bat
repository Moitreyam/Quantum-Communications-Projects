@echo off
echo ============================================
echo  Satellite QKD Mission Planning Tool
echo  Installing dependencies...
echo ============================================
pip install numpy matplotlib streamlit
echo.
echo  Launching dashboard in your browser...
echo ============================================
streamlit run "%~dp0satellite_qkd_planner.py"
pause
