# 🐍 **Existing Python Tools for Device Discovery & Identification**

## 🏆 **Top Recommended Libraries**

### **1. python-nmap** - Network Discovery Powerhouse
```python
import nmap

# Comprehensive network scanning with OS/service detection
nm = nmap.PortScanner()
scan_result = nm.scan('192.168.1.0/24', arguments='-sS -O -sV --script=default')

for host in nm.all_hosts():
    device_info = {
        'ip': host,
        'hostname': nm[host].hostname(),
        'state': nm[host].state(),
        'os': nm[host]['osmatch'][0]['name'] if nm[host]['osmatch'] else 'Unknown',
        'services': {},
        'mac': nm[host]['addresses'].get('mac', 'Unknown'),
        'vendor': nm[host]['vendor'].get(nm[host]['addresses'].get('mac', ''), 'Unknown')
    }
    
    # Service detection
    for protocol in nm[host].all_protocols():
        ports = nm[host][protocol].keys()
        for port in ports:
            service = nm[host][protocol][port]
            device_info['services'][port] = {
                'name': service['name'],
                'product': service['product'],
                'version': service['version'],
                'state': service['state']
            }
```

**Pros**: Industry standard, OS fingerprinting, service detection, MAC vendor lookup
**Cons**: Requires nmap binary installed, can be slow on large networks

### **2. scapy** - Advanced Network Analysis
```python
from scapy.all import ARP, Ether, srp, sniff
import requests

def advanced_device_discovery(network="192.168.1.0/24"):
    # ARP scan for live devices
    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    devices = []
    for element in answered_list:
        device = {
            'ip': element[1].psrc,
            'mac': element[1].hwsrc,
            'vendor': get_mac_vendor(element[1].hwsrc),
            'device_type': identify_device_type(element[1].psrc, element[1].hwsrc)
        }
        devices.append(device)
    
    return devices

def identify_device_type(ip, mac):
    """Multi-method device identification"""
    # HTTP fingerprinting
    try:
        response = requests.get(f"http://{ip}", timeout=3)
        if 'smartthings' in response.headers.get('server', '').lower():
            return 'Samsung SmartThings'
        if 'philips' in response.text.lower():
            return 'Philips Hue'
    except:
        pass
    
    # Port scanning for common IoT services
    common_iot_ports = [80, 443, 8080, 1883, 502, 8883]
    # ... port scanning logic
    
    return 'Unknown IoT Device'
```

**Pros**: Extremely powerful, packet-level control, custom protocols
**Cons**: Complex, requires networking knowledge, may need root/admin

### **3. zeroconf** - mDNS/Bonjour Service Discovery
```python
from zeroconf import ServiceBrowser, Zeroconf
import time

class DeviceListener:
    def __init__(self):
        self.devices = {}
    
    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            device_info = {
                'name': name,
                'type': type,
                'ip': str(info.addresses[0]) if info.addresses else None,
                'port': info.port,
                'properties': {k.decode(): v.decode() for k, v in info.properties.items()}
            }
            self.devices[name] = device_info
            
            # SmartThings detection
            if '_smartthings._tcp' in type:
                device_info['manufacturer'] = 'Samsung SmartThings'
                device_info['device_type'] = device_info['properties'].get('deviceType', 'Unknown')

def discover_mdns_devices():
    zeroconf = Zeroconf()
    listener = DeviceListener()
    
    # Common IoT service types
    services = [
        "_smartthings._tcp.local.",
        "_hue._tcp.local.", 
        "_homekit._tcp.local.",
        "_matter._tcp.local.",
        "_http._tcp.local.",
        "_ipp._tcp.local."
    ]
    
    browsers = []
    for service in services:
        browsers.append(ServiceBrowser(zeroconf, service, listener))
    
    time.sleep(5)  # Discovery time
    zeroconf.close()
    return listener.devices
```

**Pros**: Perfect for modern IoT devices, automatic service discovery
**Cons**: Only finds devices advertising mDNS services

### **4. netdisco** - Dedicated IoT Device Discovery
```python
from netdisco.discovery import NetworkDiscovery

# Specialized IoT device discovery
netdis = NetworkDiscovery()
netdis.scan()

# Built-in support for major IoT brands
smartthings_devices = netdis.get_info('smartthings')
philips_hue = netdis.get_info('philips_hue') 
sonos_speakers = netdis.get_info('sonos')
chromecast_devices = netdis.get_info('google_cast')

for device in smartthings_devices:
    print(f"SmartThings Hub: {device['host']}:{device['port']}")
    print(f"Device ID: {device.get('device_id', 'Unknown')}")
```

**Pros**: Purpose-built for IoT, knows major device types, easy to use
**Cons**: Limited to supported device types, less flexible

### **5. upnpclient** - UPnP Device Discovery
```python
import upnpclient

# Discover UPnP devices (many IoT devices support this)
devices = upnpclient.discover()

for device in devices:
    device_info = {
        'location': device.location,
        'server': device.server,
        'device_type': device.device_type,
        'friendly_name': device.friendly_name,
        'manufacturer': device.manufacturer,
        'model_name': device.model_name,
        'services': [s.service_type for s in device.services]
    }
    
    # Samsung SmartThings detection
    if 'samsung' in device.manufacturer.lower() and 'smartthings' in device.model_name.lower():
        device_info['identified_as'] = 'Samsung SmartThings Hub'
```

**Pros**: Great for media devices and smart home hubs, detailed device info
**Cons**: Not all IoT devices support UPnP

## 🛠️ **Integrated Solution - Best of All Worlds**

```python
# requirements.txt additions:
python-nmap>=0.7.1
scapy>=2.4.5
zeroconf>=0.39.0
netdisco>=2.8.2
upnpclient>=0.0.8
mac-vendor-lookup>=0.1.11

# Comprehensive device discovery class
class ComprehensiveDeviceDiscovery:
    def __init__(self):
        self.discovered_devices = {}
        
    def discover_all_methods(self, network="192.168.1.0/24"):
        """Run all discovery methods and merge results"""
        devices = {}
        
        # Method 1: nmap network scan (base discovery)
        nmap_devices = self.nmap_discovery(network)
        devices.update(nmap_devices)
        
        # Method 2: mDNS service discovery (IoT-specific)
        mdns_devices = self.mdns_discovery()
        self.merge_device_info(devices, mdns_devices, 'mdns')
        
        # Method 3: UPnP discovery (smart home devices)
        upnp_devices = self.upnp_discovery()
        self.merge_device_info(devices, upnp_devices, 'upnp')
        
        # Method 4: Netdisco IoT discovery
        iot_devices = self.netdisco_discovery()
        self.merge_device_info(devices, iot_devices, 'netdisco')
        
        # Method 5: HTTP fingerprinting
        for ip in devices:
            http_info = self.http_fingerprint(ip)
            devices[ip]['http_fingerprint'] = http_info
            
        return devices
    
    def calculate_confidence_score(self, device_data):
        """Calculate identification confidence based on multiple sources"""
        score = 0.0
        
        # MAC vendor match
        if device_data.get('mac_vendor') == device_data.get('detected_manufacturer'):
            score += 0.2
            
        # mDNS service detection
        if device_data.get('mdns_services'):
            score += 0.4
            
        # UPnP device info
        if device_data.get('upnp_info', {}).get('manufacturer'):
            score += 0.3
            
        # HTTP fingerprint match
        if device_data.get('http_fingerprint', {}).get('identified'):
            score += 0.5
            
        # Multiple method agreement
        sources = [s for s in ['nmap', 'mdns', 'upnp', 'netdisco'] if device_data.get(f'{s}_detected')]
        if len(sources) >= 2:
            score += 0.3
            
        return min(score, 1.0)
```

## 📦 **Quick Integration into AI-IoT Hub**

Update your `pyproject.toml`:

```toml
[project.optional-dependencies]
network = [
    "python-nmap>=0.7.1",
    "scapy>=2.4.5", 
    "zeroconf>=0.39.0",
    "netdisco>=2.8.2",
    "upnpclient>=0.0.8",
    "mac-vendor-lookup>=0.1.11"
]
```

Then integrate into your existing structure:

```python
# src/agents/device_tools.py - Enhanced NetworkScanTool
from .discovery_engines import ComprehensiveDeviceDiscovery

class EnhancedNetworkScanTool(Tool):
    def __init__(self):
        self.discovery = ComprehensiveDeviceDiscovery()
        
    def forward(self, network_range: str = "192.168.1.0/24"):
        """Discover devices using multiple methods for high accuracy"""
        devices = self.discovery.discover_all_methods(network_range)
        
        # Filter for high-confidence IoT devices
        iot_devices = {
            ip: data for ip, data in devices.items() 
            if data.get('confidence_score', 0) > 0.6
        }
        
        return iot_devices
```

## 🎯 **Recommendation**

**Start with `python-nmap` + `zeroconf`** - this combo gives you:
- Reliable network discovery (nmap)
- Modern IoT service detection (mDNS)
- Industry-standard tools
- Good balance of power vs. complexity

Add other libraries as needed for specific device types! 🚀