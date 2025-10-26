"""
Build script to create distributable executable for CESS FOODS Management System
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # PyInstaller command with options
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single executable file
        "--windowed",                   # No console window (GUI app)
        "--name=CESS_FOODS",           # Name of executable
        "--icon=app.ico",              # Icon file (if exists)
        "--add-data=*.json;.",         # Include JSON data files
        "app.py"                       # Main Python file
    ]
    
    # Remove icon option if file doesn't exist
    if not os.path.exists("app.ico"):
        cmd.remove("--icon=app.ico")
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Build completed successfully!")
        print("📁 Executable created in 'dist' folder")
        print("🚀 Run CESS_FOODS.exe to start the application")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")

if __name__ == "__main__":
    try:
        install_requirements()
        build_executable()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")