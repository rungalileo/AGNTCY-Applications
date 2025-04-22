#!/usr/bin/env python
"""
Wrapper script to run the Weather Vibes Agent from the project root.
This script handles all the import path configuration automatically.

Usage:
    python run_weather_vibes.py [location]
    python run_weather_vibes.py --location "New York" --units imperial
"""
import os
import sys
from pathlib import Path

# Set up the Python path to include the project directory
current_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(current_dir))

# Import and run the main function from the actual agent runner
if __name__ == "__main__":
    try:
        # Import here to avoid issues before sys.path is configured
        import asyncio
        from weather_vibes.run_agent import main
        
        # Run the main function
        asyncio.run(main())
    except ImportError as e:
        print(f"Error importing required modules: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're in the project's virtual environment:")
        print("   source venv/bin/activate")
        print("2. Try installing the package in development mode:")
        print("   pip install -e .")
        print("3. Ensure all requirements are installed:")
        print("   pip install -r weather_vibes/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error running the Weather Vibes Agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 