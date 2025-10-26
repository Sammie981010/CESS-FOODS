"""
Simplified build script with better error handling
"""
import subprocess
import sys
import os

def simple_build():
    print("🔧 Simple Build Script")
    print("=" * 25)
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found!")
        return False
    
    # Test if app.py can be imported
    try:
        print("Testing app.py...")
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
        print("✅ app.py readable")
    except Exception as e:
        print(f"❌ Cannot read app.py: {e}")
        return False
    
    # Simple PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=CESS_FOODS",
        "app.py"
    ]
    
    try:
        print("Running PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            print("📁 Check dist folder for CESS_FOODS.exe")
            return True
        else:
            print("❌ Build failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ PyInstaller not found!")
        print("Install with: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    simple_build()
    input("\nPress Enter to exit...")