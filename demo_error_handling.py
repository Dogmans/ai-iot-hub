"""
Quick demonstration of the improved error handling system
"""
import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Configure logging to file to prevent console interference
def setup_demo_logging():
    """Setup file-based logging for demo"""
    log_path = Path("logs/demo_error_handling.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Clear any existing handlers
    logging.getLogger().handlers.clear()
    
    # Configure file logging only
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_path),
        ]
    )

# Setup logging before importing device tools
setup_demo_logging()

from agents.device_tools import DeviceDiscoveryTool, DeviceControlTool

def demonstrate_error_handling():
    """Demonstrate the improved error handling vs generic code generation"""
    
    print("🔍 AI-IoT Hub Error Handling Demonstration")
    print("=" * 50)
    
    # Test device discovery
    print("\n1. Device Discovery Error Handling:")
    discovery_tool = DeviceDiscoveryTool()
    
    # Check dependencies
    missing_deps = discovery_tool._check_discovery_dependencies()
    if missing_deps:
        print(f"   ❌ Missing dependencies: {missing_deps}")
        print("   📋 Install commands:")
        for dep in missing_deps:
            if 'nmap' in dep:
                print("      - Download Nmap from https://nmap.org/download.html")
            else:
                print(f"      - pip install {dep}")
    else:
        print("   ✅ All discovery dependencies available")
    
    # Test device control  
    print("\n2. Device Control Error Handling:")
    control_tool = DeviceControlTool()
    
    # Try to generate communication code for unknown device
    result = control_tool._generate_communication_tool("smart_thermostat", "192.168.1.50")
    
    if isinstance(result, dict) and result.get('status') == 'failed':
        print(f"   ❌ Generation failed: {result['error']}")
        print(f"   💡 Guidance: {result.get('message', 'No specific guidance')}")
        print(f"   🔧 Action needed: {result.get('required_action', 'See documentation')}")
    else:
        print(f"   ⚠️  Unexpected result: {result}")
    
    print("\n3. Benefits of New System:")
    print("   ✅ No more generic/demo code that doesn't work")  
    print("   ✅ Clear error messages explain what's missing")
    print("   ✅ Specific installation instructions provided")
    print("   ✅ Users understand exactly what needs to be fixed")
    
    print(f"\n{'=' * 50}")
    print("🎯 System now provides actionable guidance instead of false confidence!")

if __name__ == "__main__":
    demonstrate_error_handling()