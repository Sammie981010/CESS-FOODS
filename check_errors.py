"""
Diagnostic script to check for common errors
"""
import sys
import os
import subprocess

def check_python():
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")

def check_packages():
    packages = ['tkinter', 'matplotlib', 'reportlab', 'PIL', 'pyinstaller']
    for pkg in packages:
        try:
            if pkg == 'tkinter':
                import tkinter
                print(f"✓ {pkg} - OK")
            elif pkg == 'matplotlib':
                import matplotlib
                print(f"✓ {pkg} - OK")
            elif pkg == 'reportlab':
                import reportlab
                print(f"✓ {pkg} - OK")
            elif pkg == 'PIL':
                import PIL
                print(f"✓ {pkg} - OK")
            elif pkg == 'pyinstaller':
                import PyInstaller
                print(f"✓ {pkg} - OK")
        except ImportError as e:
            print(f"✗ {pkg} - MISSING: {e}")

def check_files():
    required_files = ['app.py', 'sales.json', 'purchases.json', 'payments.json']
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} - EXISTS")
        else:
            print(f"✗ {file} - MISSING")

def check_app_syntax():
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, 'app.py', 'exec')
        print("✓ app.py syntax - OK")
    except UnicodeDecodeError:
        print("✗ app.py encoding error - fixing...")
        fix_encoding()
    except SyntaxError as e:
        print(f"✗ app.py syntax error: {e}")
    except Exception as e:
        print(f"✗ app.py error: {e}")

def fix_encoding():
    try:
        # Read with different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open('app.py', 'r', encoding=encoding) as f:
                    content = f.read()
                # Write back as UTF-8
                with open('app.py', 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Fixed encoding using {encoding}")
                return
            except UnicodeDecodeError:
                continue
        print("✗ Could not fix encoding")
    except Exception as e:
        print(f"✗ Error fixing encoding: {e}")

if __name__ == "__main__":
    print("🔍 CESS FOODS Error Diagnostic")
    print("=" * 40)
    
    print("\n1. Python Environment:")
    check_python()
    
    print("\n2. Required Packages:")
    check_packages()
    
    print("\n3. Required Files:")
    check_files()
    
    print("\n4. App Syntax Check:")
    check_app_syntax()
    
    print("\n5. Quick Fix Available:")
    print("Run: python fix_app.py (if created)")
    
    input("\nPress Enter to exit...")