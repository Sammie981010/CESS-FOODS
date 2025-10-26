"""
Fix encoding issues in app.py
"""
import os
import shutil

def fix_app_encoding():
    print("🔧 Fixing app.py encoding issues...")
    
    # Backup original
    if os.path.exists('app.py'):
        shutil.copy('app.py', 'app_backup.py')
        print("✓ Created backup: app_backup.py")
    
    # Try different encodings to read the file
    content = None
    used_encoding = None
    
    for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
        try:
            with open('app.py', 'r', encoding=encoding) as f:
                content = f.read()
            used_encoding = encoding
            print(f"✓ Successfully read with {encoding}")
            break
        except UnicodeDecodeError:
            print(f"✗ Failed with {encoding}")
            continue
    
    if content is None:
        print("❌ Could not read app.py with any encoding")
        return False
    
    # Clean content - remove problematic characters
    content = content.replace('\x90', '')  # Remove the problematic byte
    content = content.replace('\x91', "'")  # Replace with proper apostrophe
    content = content.replace('\x92', "'")  # Replace with proper apostrophe
    content = content.replace('\x93', '"')  # Replace with proper quote
    content = content.replace('\x94', '"')  # Replace with proper quote
    
    # Write back as UTF-8
    try:
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed and saved as UTF-8")
        return True
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False

if __name__ == "__main__":
    print("🔧 CESS FOODS App Encoding Fix")
    print("=" * 35)
    
    if fix_app_encoding():
        print("\n✅ Encoding fixed successfully!")
        print("Now run: python build_dist.py")
    else:
        print("\n❌ Could not fix encoding")
        print("Manual fix needed")
    
    input("\nPress Enter to exit...")