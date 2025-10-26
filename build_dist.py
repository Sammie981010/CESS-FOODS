"""
Build script to create distributable executable for CESS FOODS Management System
"""
import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    except subprocess.CalledProcessError:
        print("Warning: Some packages may already be installed")

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
        "--add-data=sales.json;.",
        "--add-data=purchases.json;.",
        "--add-data=payments.json;.",
        "--hidden-import=matplotlib.backends.backend_tkagg",
        "--hidden-import=PIL._tkinter_finder",
        "app.py"                       # Main Python file
    ]
    
    # Remove icon option if file doesn't exist
    if not os.path.exists("app.ico"):
        cmd = [c for c in cmd if not c.startswith("--icon")]
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Build completed successfully!")
        print("📁 Executable created in 'dist' folder")
        print("🚀 Run CESS_FOODS.exe to start the application")
        print("\n📋 Included features:")
        print("  ✓ Invoice numbers for sales & purchases")
        print("  ✓ Editable invoices in view windows")
        print("  ✓ Weekly sales/purchases bars + profit line graph")
        print("  ✓ All latest UI improvements")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("\nDetailed error information:")
        print(f"Command that failed: {' '.join(cmd)}")
        print("\nCommon fixes:")
        print("1. pip install pyinstaller matplotlib reportlab Pillow")
        print("2. Run: python check_errors.py")
        print("3. Check if all JSON files exist")
    except FileNotFoundError as e:
        print(f"❌ Command not found: {e}")
        print("\nTrying to install PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller installed. Please run the script again.")
        except Exception as install_error:
            print(f"Failed to install PyInstaller: {install_error}")

if __name__ == "__main__":
    try:
        print("🔧 CESS FOODS Build Script")
        print("=" * 30)
        install_requirements()
        build_executable()
    except KeyboardInterrupt:
        print("\n❌ Build cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\nDiagnostic steps:")
        print("1. Run: python check_errors.py")
        print("2. pip install pyinstaller matplotlib reportlab Pillow")
        print("3. Check if app.py has syntax errors")
        print("4. Ensure all JSON files exist")
        print("5. Run as administrator if needed")
    finally:
        input("\nPress Enter to exit...")