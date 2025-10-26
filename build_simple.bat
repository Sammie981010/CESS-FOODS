@echo off
echo Building CESS FOODS Management System...
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Build executable
echo.
echo Creating executable...
pyinstaller --onefile --windowed --name=CESS_FOODS app.py

echo.
echo Build complete! Check the 'dist' folder for CESS_FOODS.exe
pause