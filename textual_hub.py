#!/usr/bin/env python3
"""
AI-IoT Hub with Rich Textual Interface

Launch the interactive AI-IoT Hub with rich terminal formatting.
"""
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def main():
    """Main entry point for Textual interface"""
    try:
        from src.ui.textual_frontend import run_textual_app
        
        print("🚀 Starting AI-IoT Hub with Textual interface...")
        run_textual_app()
        
    except ImportError as e:
        print(f"❌ Error: Missing dependencies for Textual interface")
        print(f"   {e}")
        print("\n💡 Install with: pip install -e \".[ui]\"")
        print("   Or run basic version: python interactive_hub.py")
        
        # Show what's missing
        missing = []
        try:
            import textual
        except ImportError:
            missing.append("textual")
        
        try:
            import rich
        except ImportError:
            missing.append("rich")
            
        if missing:
            print(f"\n📦 Missing packages: {', '.join(missing)}")
            print(f"   Install with: pip install {' '.join(missing)}")
        
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()