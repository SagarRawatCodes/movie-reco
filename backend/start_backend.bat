@echo off
echo Activating virtual environment...
call .\.venv\Scripts\activate

echo Starting FastAPI server at http://127.0.0.1:8000
uvicorn app.main:app --reload