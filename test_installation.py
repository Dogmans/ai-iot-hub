#!/usr/bin/env python3
"""
Test script to verify AI-IoT Hub installation and basic functionality
"""

import sys
import os
from pathlib import Path

def test_basic_imports():
    """Test that basic modules can be imported"""
    print("🧪 Testing basic imports...")
    
    try:
        import requests
        import yaml
        import click
        import colorama
        print("✅ Core dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Core import failed: {e}")
        return False

def test_interactive_hub():
    """Test the interactive hub functionality"""
    print("🧪 Testing interactive hub...")
    
    try:
        import interactive_hub
        
        # Create a simple hub instance
        hub = interactive_hub.SimpleAIIoTHub()
        
        # Test basic functionality
        response = hub._analyze_request("test command")
        print("✅ Interactive hub works correctly")
        return True
    except Exception as e:
        print(f"❌ Interactive hub test failed: {e}")
        return False

def test_project_structure():
    """Verify project structure exists"""
    print("🧪 Testing project structure...")
    
    required_dirs = [
        "src",
        "devices/raw_docs",
        "tools/generated", 
        "config"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    else:
        print("✅ Project structure is correct")
        return True

def test_configuration():
    """Test configuration loading"""
    print("🧪 Testing configuration...")
    
    try:
        # Test YAML loading
        import yaml
        
        # Create a simple config test
        test_config = {
            "model": {"model_id": "test"},
            "network": {"scan_range": "192.168.1.0/24"}
        }
        
        # Test serialization
        yaml_str = yaml.dump(test_config)
        loaded_config = yaml.safe_load(yaml_str)
        
        assert loaded_config == test_config
        print("✅ Configuration handling works")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_ai_dependencies():
    """Check if AI dependencies are available (optional)"""
    print("🧪 Testing AI dependencies (optional)...")
    
    try:
        import smolagents
        print("✅ smolagents available - full AI functionality enabled")
        return True
    except ImportError:
        print("⚠️  smolagents not installed - AI features disabled")
        print("   Run: pip install -e '.[ai]' to enable AI functionality")
        return False

def main():
    """Run all tests"""
    print("🚀 AI-IoT Hub Installation Test")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_project_structure, 
        test_configuration,
        test_interactive_hub,
        test_ai_dependencies
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("📊 Test Summary")
    print("-" * 30)
    print(f"Passed: {passed}/{total}")
    
    if passed >= 4:  # AI dependencies are optional
        print("🎉 Installation successful! Ready to use AI-IoT Hub")
        print("\nNext steps:")
        print("1. Add device docs to devices/raw_docs/{category}/")
        print("2. Run: python interactive_hub.py")
        print("3. For full AI: pip install -e '.[ai]'")
        return 0
    else:
        print("❌ Installation issues detected")
        print("Please check the errors above and reinstall")
        return 1

if __name__ == "__main__":
    sys.exit(main())