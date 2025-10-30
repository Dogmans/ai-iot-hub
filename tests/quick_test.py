#!/usr/bin/env python3
"""
Quick test of real device discovery without nmap dependency
"""

import sys
sys.path.insert(0, "src")

from discovery.comprehensive_discovery import ComprehensiveDeviceDiscovery
import logging

logging.basicConfig(level=logging.INFO)

def main():
    print("🔍 Testing Comprehensive Device Discovery")
    
    discovery = ComprehensiveDeviceDiscovery()
    
    # Test on a small local range 
    print("🌐 Discovering devices on 192.168.1.1/30 (local test)...")
    devices = discovery.discover_all_methods("192.168.1.1/30", timeout=15)
    
    print(f"\n📊 Results:")
    print(f"   Total devices found: {len(devices)}")
    
    for ip, device_data in devices.items():
        print(f"\n   🖥️  {ip}")
        print(f"      Manufacturer: {device_data.get('manufacturer', 'Unknown')}")
        print(f"      Device Type: {device_data.get('device_type', 'Unknown')}")
        print(f"      Confidence: {device_data.get('confidence_score', 0.0):.2f}")
        print(f"      Discovery Methods: {[m for m in ['nmap', 'mdns', 'upnp', 'netdisco'] if device_data.get(f'{m}_detected')]}")
        
        # Show mDNS info if available
        if 'mdns_info' in device_data:
            mdns = device_data['mdns_info']
            print(f"      mDNS Service: {mdns.get('service_type', 'N/A')}")
            
        # Show HTTP fingerprint if available
        if 'http_fingerprint' in device_data and device_data['http_fingerprint'].get('identified'):
            print(f"      HTTP Identified: {device_data['http_fingerprint'].get('device_type', 'N/A')}")

if __name__ == "__main__":
    main()