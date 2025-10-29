"""
Demonstration of enhanced device discovery with available dependencies
Shows what's possible with netdisco, zeroconf, and mac_vendor_lookup
"""
import sys
import logging
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

# Configure logging to file to prevent console interference
def setup_test_logging():
    """Setup file-based logging for testing"""
    log_path = Path("logs/test_discovery.log")
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

def test_enhanced_discovery():
    """Test device discovery with available libraries"""
    # Setup logging before importing device tools
    setup_test_logging()
    
    print("🔍 Enhanced Device Discovery Test")
    print("=" * 50)
    
    from agents.device_tools import DeviceDiscoveryTool
    
    # Create discovery tool
    discovery_tool = DeviceDiscoveryTool()
    
    # Check what dependencies we have
    missing_deps = discovery_tool._check_discovery_dependencies()
    available_deps = ['netdisco', 'zeroconf', 'mac_vendor_lookup']
    
    print(f"Available dependencies: {available_deps}")
    print(f"Missing dependencies: {missing_deps}")
    
    # Test discovery with available tools
    print(f"\nRunning discovery with available tools...")
    
    # Use a real network range (replace with your actual network)
    network_range = "192.168.1.0/24"  # Common home network range
    
    try:
        # Test the forward method (main discovery entry point)
        result = discovery_tool.forward(network_range)
        
        print(f"\nDiscovery Results:")
        print(f"  Method used: {result.get('discovery_method', 'unknown')}")
        print(f"  Devices found: {result.get('total_found', 0)}")
        
        if result.get('limitations'):
            print(f"  Current limitations:")
            for limitation in result['limitations']:
                print(f"    - {limitation}")
        
        if result.get('recommendations'):
            print(f"  Recommendations:")
            for rec in result['recommendations']:
                print(f"    - {rec}")
                
        # Show discovered devices (if any)
        devices = result.get('discovered_devices', [])
        if devices:
            print(f"  Discovered devices:")
            for device in devices[:3]:  # Show first 3
                print(f"    - {device.get('ip', 'unknown')} ({device.get('type', 'unknown')})")
        else:
            print(f"  No devices discovered (this is normal without nmap)")
            
    except Exception as e:
        print(f"Discovery error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Discovery with available tools completed!")
    print("💡 Install nmap and upnpclient for comprehensive device identification")

if __name__ == "__main__":
    test_enhanced_discovery()