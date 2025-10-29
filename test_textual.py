#!/usr/bin/env python3
"""
Test script for Textual interface components
Validates UI functionality without requiring full AI setup
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

def test_markup_loading():
    """Test loading of markup configuration"""
    print("🧪 Testing markup configuration loading...")
    
    from src.ui.textual_frontend import AIIoTApp
    
    app = AIIoTApp()
    instructions = app.markup_instructions
    
    print(f"✅ Loaded {len(instructions)} characters of markup instructions")
    print(f"📝 Sample: {instructions[:100]}...")
    
    # Check for key formatting elements
    required_elements = ['[bold]', '[green]', '[red]', '🔍', '━━━']
    missing = [elem for elem in required_elements if elem not in instructions]
    
    if missing:
        print(f"⚠️  Missing elements: {missing}")
    else:
        print("✅ All required markup elements found")

def test_demo_controller():
    """Test demo controller responses"""
    print("\n🧪 Testing demo controller...")
    
    from src.ui.textual_frontend import DemoAIController
    
    demo = DemoAIController()
    
    # Test different request types
    test_cases = [
        ("discover devices", "discovery"),
        ("control washing machine", "washing machine"),
        ("check temperature", "temperature"),
        ("help", "help"),
        ("unknown command", "general")
    ]
    
    for query, expected_type in test_cases:
        print(f"  Testing: '{query}'")
        
        import asyncio
        response = asyncio.run(demo.process_request_with_textual("", query))
        
        # Check for expected formatting
        has_formatting = any(marker in response for marker in ['[bold]', '[green]', '[red]', '━━━'])
        
        if has_formatting:
            print(f"    ✅ Response has proper formatting")
        else:
            print(f"    ⚠️  Response missing formatting")
        
        print(f"    📝 Length: {len(response)} chars")

def test_config_file():
    """Test configuration file structure"""
    print("\n🧪 Testing configuration files...")
    
    config_file = Path("config/textual_markup_guide.md")
    
    if config_file.exists():
        print(f"✅ Configuration file exists: {config_file}")
        
        with open(config_file) as f:
            content = f.read()
        
        print(f"📊 File size: {len(content)} characters")
        
        # Check for key sections
        sections = ["Basic Text Formatting", "Color Formatting", "Visual Structure", "Example"]
        for section in sections:
            if section in content:
                print(f"  ✅ Section found: {section}")
            else:
                print(f"  ⚠️  Section missing: {section}")
    else:
        print(f"❌ Configuration file not found: {config_file}")

def main():
    """Run all tests"""
    print("🚀 Textual Interface Component Tests")
    print("=" * 50)
    
    try:
        test_config_file()
        test_markup_loading()
        test_demo_controller()
        
        print("\n✨ All tests completed!")
        print("🎯 Ready to launch: python textual_hub.py")
        
    except ImportError as e:
        print(f"\n⚠️  Import error: {e}")
        print("💡 Install dependencies: pip install -e \".[ui]\"")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()