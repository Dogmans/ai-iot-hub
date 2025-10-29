#!/usr/bin/env python3
"""
Test script to validate the enhanced error handling system
"""

import sys
import logging
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from agents.device_tools import DeviceDiscoveryTool, DeviceControlTool

# Setup simple logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_discovery_without_dependencies():
    """Test device discovery when dependencies are missing"""
    print("=" * 60)
    print("Testing Device Discovery without required dependencies")
    print("=" * 60)
    
    # Create discovery tool
    discovery_tool = DeviceDiscoveryTool()
    
    # Test dependency checking
    print("\n1. Testing dependency check...")
    missing_deps = discovery_tool._check_discovery_dependencies()
    
    if missing_deps:
        print(f"✓ Correctly detected missing dependencies: {missing_deps}")
    else:
        print("! All dependencies are available")
    
    # Test discovery with error handling
    print("\n2. Testing discovery with error handling...")
    try:
        result = discovery_tool.forward("192.168.1.0/24")
        print(f"Discovery result: {result}")
    except Exception as e:
        print(f"Discovery error: {e}")

def test_device_control_without_specs():
    """Test device control when proper specs are missing"""
    print("\n" + "=" * 60)
    print("Testing Device Control without proper documentation")
    print("=" * 60)
    
    # Create control tool
    control_tool = DeviceControlTool()
    
    print("\n1. Testing control of unknown device type...")
    try:
        result = control_tool.forward("192.168.1.1", "router", "get status")
        print(f"Control result: {result}")
    except Exception as e:
        print(f"Control error: {e}")

def test_generate_communication_tool():
    """Test the enhanced communication tool generation"""
    print("\n" + "=" * 60)
    print("Testing Communication Tool Generation Error Handling")
    print("=" * 60)
    
    control_tool = DeviceControlTool()
    
    # Test with minimal device spec (should trigger documentation error)
    minimal_spec = {
        "type": "router",
        "manufacturer": "unknown", 
        "protocol": "unknown"
    }
    
    print("\n1. Testing with minimal device spec...")
    result = control_tool._generate_communication_tool("router", "192.168.1.1")
    
    if isinstance(result, dict) and "error" in result:
        print(f"✓ Correctly returned error: {result['error']}")
        print(f"✓ Guidance provided: {result.get('guidance', 'No guidance')}")
    else:
        print(f"! Unexpected result: {result}")

if __name__ == "__main__":
    print("AI-IoT Hub Error Handling Validation Test")
    print("This test validates that the system provides helpful error messages")
    print("instead of falling back to generic demo code.\n")
    
    test_discovery_without_dependencies()
    test_device_control_without_specs() 
    test_generate_communication_tool()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("The system should now provide clear error messages and guidance")
    print("instead of generating generic demo code.")
    print("=" * 60)