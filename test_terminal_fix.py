#!/usr/bin/env python3
"""
Test script to demonstrate the fixed interactive terminal behavior
"""

import subprocess
import sys
from pathlib import Path

def test_piped_input():
    """Test piped input functionality"""
    print("🧪 Testing piped input mode...")
    
    python_exe = Path("C:/repos/ai-iot/.venv/Scripts/python.exe")
    script_path = Path("interactive_hub.py")
    
    # Test single command
    result = subprocess.run(
        [str(python_exe), str(script_path)],
        input="discover devices\n",
        text=True,
        capture_output=True
    )
    
    print("📤 Input: 'discover devices'")
    print("📥 Output preview:")
    lines = result.stdout.split('\n')
    # Show first few and last few lines
    preview_lines = lines[:8] + ['...'] + lines[-5:]
    for line in preview_lines:
        if line.strip():
            print(f"   {line}")
    
    if "Device Discovery Complete" in result.stdout:
        print("✅ Piped input works correctly!")
        return True
    else:
        print("❌ Piped input failed")
        return False

def test_device_control():
    """Test device control via piped input"""
    print("\n🧪 Testing device control...")
    
    python_exe = Path("C:/repos/ai-iot/.venv/Scripts/python.exe") 
    script_path = Path("interactive_hub.py")
    
    result = subprocess.run(
        [str(python_exe), str(script_path)],
        input="start washing machine at 192.168.0.5\n",
        text=True,
        capture_output=True
    )
    
    print("📤 Input: 'start washing machine at 192.168.0.5'")
    
    if "Washing machine started successfully" in result.stdout:
        print("✅ Device control works correctly!")
        return True
    else:
        print("❌ Device control failed")
        print("Debug output:", result.stdout[-200:])  # Last 200 chars
        return False

def test_help_command():
    """Test help command"""
    print("\n🧪 Testing help command...")
    
    python_exe = Path("C:/repos/ai-iot/.venv/Scripts/python.exe")
    script_path = Path("interactive_hub.py")
    
    result = subprocess.run(
        [str(python_exe), str(script_path)],
        input="help\n",
        text=True,
        capture_output=True
    )
    
    print("📤 Input: 'help'")
    
    if "AI-IoT Hub Help" in result.stdout:
        print("✅ Help command works correctly!")
        return True
    else:
        print("❌ Help command failed")
        return False

def main():
    """Run all terminal tests"""
    print("🔧 AI-IoT Hub Terminal Fix Verification")
    print("=" * 50)
    
    tests = [
        test_piped_input,
        test_device_control,
        test_help_command
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All terminal functionality works correctly!")
        print("\n✅ Fixed Issues:")
        print("  • Piped input no longer causes infinite loops")
        print("  • EOF handling works properly")
        print("  • Interactive vs non-interactive mode detection")
        print("  • Clean exit on completion")
    else:
        print("❌ Some tests failed - please check the output above")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())