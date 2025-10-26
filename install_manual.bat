@echo off
echo Installing packages manually...
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing PyInstaller...
python -m pip install pyinstaller
echo.

echo Installing matplotlib...
python -m pip install matplotlib
echo.

echo Installing reportlab...
python -m pip install reportlab
echo.

echo Installing Pillow...
python -m pip install Pillow
echo.

echo Done! Now you can run build_dist.py
pause