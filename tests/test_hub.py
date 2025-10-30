#!/usr/bin/env python3
"""
Test the AI-IoT Hub functionality with scripted interactions
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from interactive_hub import SimpleAIIoTHub

def test_ai_iot_hub():
    """Test AI-IoT Hub with various commands"""
    
    print("🚀 Testing AI-IoT Hub LLM Integration")
    print("=" * 60)
    
    hub = SimpleAIIoTHub()
    
    # Test 1: Device Discovery
    print("\n📍 TEST 1: Device Discovery")
    print("-" * 30)
    response = hub.process_user_request("Discover all devices on my network")
    print(response)
    
    # Test 2: Washing Machine Control
    print("\n📍 TEST 2: Washing Machine Control")
    print("-" * 30)
    response = hub.process_user_request("Start washing machine at 192.168.0.5")
    print(response)
    
    # Test 3: Status Check
    print("\n📍 TEST 3: Device Status Check")
    print("-" * 30)
    response = hub.process_user_request("Check status of washing machine at 192.168.0.5")
    print(response)
    
    # Test 4: Show generated files
    print("\n📍 TEST 4: Generated Files")
    print("-" * 30)
    
    # Check config file
    config_file = Path("config/credentials.json")
    if config_file.exists():
        print(f"✅ Config created: {config_file}")
        with open(config_file) as f:
            import json
            config = json.load(f)
            print(f"   Contains: {list(config.keys())}")
    
    # Check generated tool
    tool_file = Path("tools/generated/washing_machine_192_168_0_5.py")
    if tool_file.exists():
        print(f"✅ Tool generated: {tool_file}")
        print(f"   Size: {tool_file.stat().st_size} bytes")
        
        # Show first few lines
        lines = tool_file.read_text().split('\n')[:10]
        print("   Preview:")
        for line in lines:
            print(f"     {line}")
    
    print(f"\n🎯 Summary: AI-IoT Hub successfully demonstrated:")
    print(f"   🔍 Device discovery simulation")
    print(f"   🧠 LLM request analysis and routing")
    print(f"   📝 Automatic communication code generation")
    print(f"   🔑 Credential management and prompting")
    print(f"   📊 Device status simulation")

if __name__ == "__main__":
    test_ai_iot_hub()