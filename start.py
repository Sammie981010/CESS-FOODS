#!/usr/bin/env python3
"""
Start script for CESS FOODS Management System
"""
import sys
import os

def main():
    """Main entry point"""
    try:
        # Import and run the application
        from app import FoodApp
        
        print("🚀 Starting CESS FOODS Management System...")
        app = FoodApp()
        app.run()
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()