@echo off
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing required packages...
pip install -q Flask pandas joblib xgboost scikit-learn

echo.
echo Starting Flask app...
echo Open your browser and go to: http://127.0.0.1:5000
echo.

cd app
python app.py
pause
