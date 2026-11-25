@echo off
cd /d "c:\Users\pgowt\OneDrive\Desktop\all folders\main folders\cheran_pumps"
call .venv\Scripts\activate
echo.
echo Starting Cheran Pumps server...
echo Open your browser at http://127.0.0.1:8000
echo Press CTRL+C to stop the server.
echo.
python manage.py runserver
pause
