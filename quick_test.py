"""
Quick test to identify the exact error
"""
import sys
import traceback

def test_app_import():
    try:
        print("Testing app.py import...")
        import app
        print("✅ app.py imports successfully")
        return True
    except Exception as e:
        print(f"❌ Error importing app.py: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def test_basic_run():
    try:
        print("\nTesting basic app creation...")
        from app import FoodApp
        print("✅ FoodApp class accessible")
        return True
    except Exception as e:
        print(f"❌ Error creating FoodApp: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Quick Error Test")
    print("=" * 20)
    
    if test_app_import():
        test_basic_run()
    
    input("\nPress Enter to exit...")