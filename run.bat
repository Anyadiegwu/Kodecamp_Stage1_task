@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Checking packages...
pip install -r requirements.txt --quiet --no-warn-script-location

echo.
echo Starting Gemini App...
python main.py

pause