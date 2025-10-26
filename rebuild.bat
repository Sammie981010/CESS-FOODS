@echo off
echo Rebuilding CESS FOODS with all latest changes...
echo.
echo Cleaning old build files...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"
echo.
echo Building new executable...
python build_dist.py
echo.
echo Done! Check dist folder for CESS_FOODS.exe
pause