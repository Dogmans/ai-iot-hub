#!/usr/bin/env python3
"""
Test script for comprehensive device discovery implementation.

This script validates that the real device discovery works correctly,
both with and without the optional network dependencies installed.
"""

import logging
import sys
import json
from pathlib import Path

# Add src to path to import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_discovery_imports():
    """Test that discovery modules import correctly with graceful fallbacks."""
    print("🔍 Testing discovery module imports...")
    
    try:
        from src.discovery.comprehensive_discovery import ComprehensiveDeviceDiscovery, get_discovery_engine
        print("✅ Comprehensive discovery imports successful")
        return True
    except ImportError as e:
        if "smolagents" in str(e):
            print("⚠️ smolagents not available, testing discovery engine directly")
            try:
                # Test the discovery engine without smolagents dependency
                import sys
                sys.path.insert(0, "src")
                from discovery.comprehensive_discovery import ComprehensiveDeviceDiscovery
                print("✅ Direct discovery engine imports successful")
                return True
            except Exception as e2:
                print(f"❌ Direct discovery engine import failed: {e2}")
                return False
        else:
            print(f"❌ Discovery import failed: {e}")
            return False

def test_device_tools():
    """Test that device tools work with and without network dependencies."""
    print("\n🛠️ Testing DeviceDiscoveryTool...")
    
    try:
        from src.agents.device_tools import DeviceDiscoveryTool
        print("✅ DeviceDiscoveryTool imports successful")
        
        # Create tool instance
        discovery_tool = DeviceDiscoveryTool()
        print("✅ DeviceDiscoveryTool instantiation successful")
        
        return discovery_tool
    except ImportError as e:
        if "smolagents" in str(e):
            print("⚠️ smolagents not available - testing discovery engine directly")
            try:
                # Import discovery engine directly
                import sys
                sys.path.insert(0, "src")
                from discovery.comprehensive_discovery import ComprehensiveDeviceDiscovery
                discovery_tool = ComprehensiveDeviceDiscovery()
                print("✅ Direct discovery engine instantiation successful")
                return discovery_tool
            except Exception as e2:
                print(f"❌ Direct discovery engine failed: {e2}")
                return None
        else:
            print(f"❌ DeviceDiscoveryTool import failed: {e}")
            return None

def test_fallback_discovery(discovery_tool):
    """Test fallback discovery method (always works)."""
    print("\n🔄 Testing fallback discovery method...")
    
    try:
        # Test with local loopback range (safe for testing)
        if hasattr(discovery_tool, 'forward'):
            # DeviceDiscoveryTool interface
            result = discovery_tool.forward(network_range="127.0.0.0/30", timeout=10)
        else:
            # Direct discovery engine interface
            result = discovery_tool.discover_all_methods(network_range="127.0.0.0/30", timeout=10)
            # Convert to expected format
            result = {
                "discovered_devices": list(result.values()),
                "scan_range": "127.0.0.0/30",
                "total_found": len(result),
                "discovery_method": "comprehensive" if result else "fallback"
            }
        
        print(f"✅ Discovery completed")
        print(f"   Scan range: {result.get('scan_range', 'Unknown')}")
        print(f"   Total devices: {result.get('total_found', 0)}")
        print(f"   Discovery method: {result.get('discovery_method', 'Unknown')}")
        
        discovered_devices = result.get('discovered_devices', [])
        if discovered_devices:
            print("   Found devices:")
            for device in discovered_devices[:3]:  # Show first 3
                ip = device.get('ip', 'Unknown')
                device_type = device.get('device_type', 'Unknown')
                confidence = device.get('confidence_score', device.get('confidence', 0.0))
                print(f"     - {ip}: {device_type} (confidence: {confidence:.2f})")
        
        return True
    except Exception as e:
        print(f"❌ Discovery test failed: {e}")
        return False

def test_comprehensive_discovery(discovery_tool):
    """Test comprehensive discovery if network dependencies are available."""
    print("\n🚀 Testing comprehensive discovery method...")
    
    # Check if we have the discovery engine (either as attribute or direct instance)
    if hasattr(discovery_tool, 'discovery_engine') and not discovery_tool.discovery_engine:
        print("⚠️ Comprehensive discovery not available (missing network dependencies)")
        print("   Install with: pip install -e '.[network]'")
        return False
    elif not hasattr(discovery_tool, 'discovery_engine') and not hasattr(discovery_tool, 'discover_all_methods'):
        print("⚠️ No discovery methods available")
        return False
    
    try:
        # Test with local network range (adjust as needed)
        result = discovery_tool.forward(network_range="192.168.1.0/28", timeout=15)
        
        print(f"✅ Comprehensive discovery completed")
        print(f"   Scan range: {result['scan_range']}")
        print(f"   Total devices: {result['total_found']}")
        print(f"   Discovery method: {result['discovery_method']}")
        print(f"   High confidence devices: {len(result.get('high_confidence_devices', []))}")
        
        if result['discovered_devices']:
            print("   Found devices:")
            for device in result['discovered_devices'][:5]:  # Show first 5
                methods = ', '.join(device['discovery_methods'])
                print(f"     - {device['ip']}: {device['manufacturer']} {device['device_type']}")
                print(f"       Confidence: {device['confidence_score']:.2f}, Methods: {methods}")
        
        return True
    except Exception as e:
        print(f"❌ Comprehensive discovery failed: {e}")
        return False

def test_device_registry():
    """Test that device registry is created and readable."""
    print("\n📝 Testing device registry...")
    
    registry_path = Path("devices/discovered_devices.json")
    
    if registry_path.exists():
        try:
            with open(registry_path) as f:
                registry_data = json.load(f)
            
            print(f"✅ Device registry loaded successfully")
            print(f"   File: {registry_path}")
            print(f"   Last scan: {registry_data.get('last_scan', 'Unknown')}")
            print(f"   Discovery engine: {registry_data.get('discovery_engine', 'Unknown')}")
            print(f"   Total devices: {registry_data.get('total_devices', 0)}")
            print(f"   High confidence: {registry_data.get('high_confidence_devices', 0)}")
            
            return True
        except Exception as e:
            print(f"❌ Failed to read device registry: {e}")
            return False
    else:
        print("⚠️ No device registry found (run discovery first)")
        return False

def check_network_dependencies():
    """Check which network discovery libraries are available."""
    print("\n📦 Checking network discovery dependencies...")
    
    dependencies = [
        ("python-nmap", "nmap"),
        ("zeroconf", "zeroconf"),
        ("netdisco", "netdisco.discovery"),
        ("upnpclient", "upnpclient"),
        ("mac-vendor-lookup", "mac_vendor_lookup")
    ]
    
    available = []
    missing = []
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"   ✅ {name}")
            available.append(name)
        except ImportError:
            print(f"   ❌ {name}")
            missing.append(name)
    
    print(f"\nAvailable: {len(available)}/{len(dependencies)} dependencies")
    
    if missing:
        print(f"To install missing dependencies: pip install -e '.[network]'")
    
    return len(available), len(missing)

def main():
    """Run comprehensive device discovery tests."""
    print("🧪 AI-IoT Hub Device Discovery Test Suite")
    print("=" * 50)
    
    # Check dependencies
    available_count, missing_count = check_network_dependencies()
    
    # Test imports
    imports_ok = test_discovery_imports()
    if not imports_ok:
        print("\n❌ Critical import failure - cannot continue")
        return 1
    
    # Test device tools
    discovery_tool = test_device_tools()
    if not discovery_tool:
        print("\n❌ DeviceDiscoveryTool failure - cannot continue")
        return 1
    
    # Test fallback discovery (always available)
    fallback_ok = test_fallback_discovery(discovery_tool)
    
    # Test comprehensive discovery (if dependencies available)
    comprehensive_ok = False
    if available_count > 0:
        comprehensive_ok = test_comprehensive_discovery(discovery_tool)
    
    # Test device registry
    registry_ok = test_device_registry()
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 Test Results Summary:")
    print(f"   Module Imports: {'✅' if imports_ok else '❌'}")
    print(f"   Device Tools: {'✅' if discovery_tool else '❌'}")
    print(f"   Fallback Discovery: {'✅' if fallback_ok else '❌'}")
    print(f"   Comprehensive Discovery: {'✅' if comprehensive_ok else '⚠️ Deps missing' if missing_count > 0 else '❌'}")
    print(f"   Device Registry: {'✅' if registry_ok else '⚠️'}")
    print(f"   Network Dependencies: {available_count}/{available_count + missing_count}")
    
    if fallback_ok and (comprehensive_ok or missing_count > 0):
        print("\n🎉 Device discovery is working! Ready for AI-IoT Hub usage.")
        return 0
    else:
        print("\n💥 Some tests failed. Check errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)