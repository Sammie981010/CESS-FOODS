# CESS FOODS - Build Instructions

## Creating Distributable Executable

### Prerequisites
1. Python 3.7+ installed
2. Required packages: matplotlib, reportlab, pyinstaller

### Method 1: Using Batch File (Easiest)
1. Double-click `build_simple.bat`
2. Wait for build to complete
3. Find `CESS_FOODS.exe` in the `dist` folder

### Method 2: Manual Commands
```cmd
# Install dependencies
pip install matplotlib reportlab pyinstaller

# Build executable
pyinstaller --onefile --windowed --name=CESS_FOODS app.py
```

### Method 3: Using Spec File
```cmd
# Install dependencies first
pip install matplotlib reportlab pyinstaller

# Build using spec file
pyinstaller CESS_FOODS.spec
```

### Output
- Executable: `dist/CESS_FOODS.exe`
- Size: ~50-80MB (includes Python runtime)
- Standalone: No Python installation required on target machine

### Distribution
1. Copy `CESS_FOODS.exe` to target computer
2. Optionally include sample JSON files for initial data
3. Run the executable - it will create data files automatically

### Troubleshooting
- If build fails, ensure all dependencies are installed
- For missing modules, add them to hiddenimports in the spec file
- Antivirus may flag the executable - add exception if needed

### Login Credentials
- Admin: admin@cess.com / admin123
- Cashier: cashier@cess.com / cashier123