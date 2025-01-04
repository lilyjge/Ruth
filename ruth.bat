@echo off
REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install required dependencies
pip install -r requirements.txt

REM Run initialization script
python initialize.py

REM Start the application
python app.py