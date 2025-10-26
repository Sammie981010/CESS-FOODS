"""
Install packages one by one with error handling
"""
import subprocess
import sys

def install_package(package):
    """Install a single package"""
    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error installing {package}: {e}")
        return False

def upgrade_pip():
    """Upgrade pip first"""
    print("Upgrading pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip upgraded")
        return True
    except Exception as e:
        print(f"❌ Failed to upgrade pip: {e}")
        return False

def main():
    print("📦 Package Installer")
    print("=" * 20)
    
    # Upgrade pip first
    upgrade_pip()
    
    # List of packages to install
    packages = ["pyinstaller", "matplotlib", "reportlab", "Pillow"]
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
        print("-" * 30)
    
    print(f"\n📊 Results: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("✅ All packages installed! You can now run build_dist.py")
    else:
        print("❌ Some packages failed. Try manual installation:")
        for package in packages:
            print(f"  pip install {package}")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")