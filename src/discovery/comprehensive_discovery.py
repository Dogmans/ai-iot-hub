"""
Comprehensive device discovery engine using multiple methods for high accuracy.

This module integrates several proven Python libraries to provide robust IoT device
discovery and identification with confidence scoring.
"""

import logging
import socket
import time
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import requests

# Network discovery libraries (optional imports with graceful fallbacks)
try:
    import nmap
    HAS_NMAP = True
except ImportError:
    HAS_NMAP = False
    logging.warning("python-nmap not available - network scanning disabled")

try:
    from zeroconf import ServiceBrowser, Zeroconf
    HAS_ZEROCONF = True
except ImportError:
    HAS_ZEROCONF = False
    logging.warning("zeroconf not available - mDNS discovery disabled")

try:
    from netdisco.discovery import NetworkDiscovery
    HAS_NETDISCO = True
except ImportError:
    HAS_NETDISCO = False
    logging.warning("netdisco not available - IoT-specific discovery disabled")

try:
    import upnpclient
    HAS_UPNP = True
except ImportError:
    HAS_UPNP = False
    logging.warning("upnpclient not available - UPnP discovery disabled")

try:
    from mac_vendor_lookup import MacLookup
    HAS_MAC_LOOKUP = True
except ImportError:
    HAS_MAC_LOOKUP = False
    logging.warning("mac-vendor-lookup not available - MAC vendor lookup disabled")


class DeviceListener:
    """mDNS service discovery listener for zeroconf."""
    
    def __init__(self):
        self.devices = {}
        self.logger = logging.getLogger(__name__)
    
    def add_service(self, zeroconf, type, name):
        """Handle discovered mDNS service."""
        try:
            info = zeroconf.get_service_info(type, name)
            if info and info.addresses:
                ip = socket.inet_ntoa(info.addresses[0])
                device_info = {
                    'name': name,
                    'service_type': type,
                    'ip': ip,
                    'port': info.port,
                    'properties': {k.decode('utf-8', errors='ignore'): v.decode('utf-8', errors='ignore') 
                                 for k, v in info.properties.items()},
                    'discovery_method': 'mdns'
                }
                
                # SmartThings detection
                if '_smartthings._tcp' in type:
                    device_info['manufacturer'] = 'Samsung SmartThings'
                    device_info['device_type'] = device_info['properties'].get('deviceType', 'SmartThings Hub')
                    device_info['confidence'] = 0.9
                
                # Philips Hue detection  
                elif '_hue._tcp' in type:
                    device_info['manufacturer'] = 'Philips'
                    device_info['device_type'] = 'Hue Bridge'
                    device_info['confidence'] = 0.9
                
                # HomeKit detection
                elif '_hap._tcp' in type:
                    device_info['manufacturer'] = 'Apple HomeKit Compatible'
                    device_info['device_type'] = device_info['properties'].get('md', 'HomeKit Device')
                    device_info['confidence'] = 0.8
                
                self.devices[ip] = device_info
                self.logger.info(f"Discovered {type} device at {ip}: {name}")
                
        except Exception as e:
            self.logger.debug(f"Error processing mDNS service {name}: {e}")
    
    def remove_service(self, zeroconf, type, name):
        """Handle removed mDNS service."""
        pass


class ComprehensiveDeviceDiscovery:
    """Multi-method device discovery with confidence scoring."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.discovered_devices = {}
        
        # Initialize MAC lookup if available
        self.mac_lookup = MacLookup() if HAS_MAC_LOOKUP else None
        
        # Common IoT device signatures
        self.device_signatures = {
            'smartthings': {
                'http_headers': ['smartthings', 'samsung'],
                'http_content': ['smartthings', 'hub'],
                'ports': [8080, 39500],
                'manufacturer': 'Samsung SmartThings'
            },
            'philips_hue': {
                'http_headers': ['philips', 'hue'],
                'http_content': ['philips', 'hue', 'bridge'],
                'ports': [80, 443],
                'manufacturer': 'Philips'
            },
            'sonos': {
                'http_headers': ['sonos'],
                'ports': [1400],
                'manufacturer': 'Sonos'
            },
            'nest': {
                'http_headers': ['nest', 'google'],
                'manufacturer': 'Google Nest'
            }
        }
    
    def discover_all_methods(self, network_range: str = "192.168.1.0/24", timeout: int = 30) -> Dict[str, Dict[str, Any]]:
        """
        Run all available discovery methods and merge results.
        
        Args:
            network_range: CIDR network range to scan
            timeout: Maximum time to spend on discovery
            
        Returns:
            Dictionary of discovered devices with comprehensive information
        """
        self.logger.info(f"Starting comprehensive device discovery on {network_range}")
        start_time = time.time()
        
        devices = {}
        
        # Method 1: nmap network scan (base discovery)
        if HAS_NMAP:
            self.logger.info("Running nmap network scan...")
            nmap_devices = self._nmap_discovery(network_range)
            devices.update(nmap_devices)
            self.logger.info(f"nmap discovered {len(nmap_devices)} devices")
        
        # Method 2: mDNS service discovery (IoT-specific)
        if HAS_ZEROCONF:
            self.logger.info("Running mDNS service discovery...")
            mdns_devices = self._mdns_discovery(timeout=min(10, timeout//3))
            self._merge_device_info(devices, mdns_devices, 'mdns')
            self.logger.info(f"mDNS discovered {len(mdns_devices)} services")
        
        # Method 3: UPnP discovery (smart home devices)
        if HAS_UPNP:
            self.logger.info("Running UPnP discovery...")
            upnp_devices = self._upnp_discovery(timeout=min(10, timeout//3))
            self._merge_device_info(devices, upnp_devices, 'upnp')
            self.logger.info(f"UPnP discovered {len(upnp_devices)} devices")
        
        # Method 4: Netdisco IoT discovery
        if HAS_NETDISCO:
            self.logger.info("Running netdisco IoT discovery...")
            iot_devices = self._netdisco_discovery()
            self._merge_device_info(devices, iot_devices, 'netdisco')
            self.logger.info(f"netdisco discovered {len(iot_devices)} IoT devices")
        
        # Method 5: HTTP fingerprinting for all discovered IPs
        self.logger.info("Running HTTP fingerprinting...")
        self._add_http_fingerprints(devices)
        
        # Calculate confidence scores
        for ip, device_data in devices.items():
            device_data['confidence_score'] = self._calculate_confidence_score(device_data)
            device_data['discovery_time'] = time.time() - start_time
        
        # Filter for high-confidence IoT devices
        iot_devices = {
            ip: data for ip, data in devices.items() 
            if self._is_likely_iot_device(data)
        }
        
        elapsed_time = time.time() - start_time
        self.logger.info(f"Discovery completed in {elapsed_time:.1f}s. Found {len(devices)} total devices, {len(iot_devices)} likely IoT devices")
        
        return iot_devices
    
    def _nmap_discovery(self, network_range: str) -> Dict[str, Dict[str, Any]]:
        """Discover devices using nmap network scanning."""
        devices = {}
        
        try:
            nm = nmap.PortScanner()
            # Fast scan with OS detection and service version detection
            scan_args = '-sn -O --osscan-guess'  # Ping scan with OS detection
            self.logger.debug(f"Running nmap scan: {scan_args}")
            
            scan_result = nm.scan(network_range, arguments=scan_args)
            
            for host in nm.all_hosts():
                if nm[host].state() == 'up':
                    device_info = {
                        'ip': host,
                        'hostname': nm[host].hostname(),
                        'state': nm[host].state(),
                        'discovery_method': 'nmap',
                        'services': {},
                        'os_info': []
                    }
                    
                    # MAC address and vendor
                    if 'mac' in nm[host]['addresses']:
                        device_info['mac'] = nm[host]['addresses']['mac']
                        device_info['mac_vendor'] = self._get_mac_vendor(device_info['mac'])
                    
                    # OS detection
                    if 'osmatch' in nm[host] and nm[host]['osmatch']:
                        for os_match in nm[host]['osmatch']:
                            device_info['os_info'].append({
                                'name': os_match.get('name', ''),
                                'accuracy': int(os_match.get('accuracy', 0)),
                                'line': os_match.get('line', '')
                            })
                    
                    devices[host] = device_info
                    
        except Exception as e:
            self.logger.error(f"nmap discovery failed: {e}")
        
        return devices
    
    def _mdns_discovery(self, timeout: int = 10) -> Dict[str, Dict[str, Any]]:
        """Discover devices using mDNS/Bonjour service discovery."""
        devices = {}
        
        try:
            zeroconf = Zeroconf()
            listener = DeviceListener()
            
            # Common IoT service types
            services = [
                "_smartthings._tcp.local.",
                "_hue._tcp.local.",
                "_hap._tcp.local.",  # HomeKit
                "_matter._tcp.local.",  # Matter/Thread
                "_http._tcp.local.",
                "_ipp._tcp.local.",  # Printers
                "_airplay._tcp.local.",  # Apple devices
                "_googlecast._tcp.local.",  # Chromecast
                "_sonos._tcp.local.",  # Sonos speakers
                "_spotify-connect._tcp.local."  # Spotify Connect devices
            ]
            
            browsers = []
            for service in services:
                browsers.append(ServiceBrowser(zeroconf, service, listener))
            
            time.sleep(timeout)
            zeroconf.close()
            
            devices = listener.devices
            
        except Exception as e:
            self.logger.error(f"mDNS discovery failed: {e}")
        
        return devices
    
    def _upnp_discovery(self, timeout: int = 10) -> Dict[str, Dict[str, Any]]:
        """Discover devices using UPnP."""
        devices = {}
        
        try:
            upnp_devices = upnpclient.discover(timeout=timeout)
            
            for device in upnp_devices:
                # Extract IP from location URL
                ip = self._extract_ip_from_url(device.location)
                if not ip:
                    continue
                    
                device_info = {
                    'ip': ip,
                    'location': device.location,
                    'server': getattr(device, 'server', ''),
                    'device_type': getattr(device, 'device_type', ''),
                    'friendly_name': getattr(device, 'friendly_name', ''),
                    'manufacturer': getattr(device, 'manufacturer', ''),
                    'model_name': getattr(device, 'model_name', ''),
                    'model_description': getattr(device, 'model_description', ''),
                    'services': [s.service_type for s in getattr(device, 'services', [])],
                    'discovery_method': 'upnp'
                }
                
                # Samsung SmartThings detection
                if ('samsung' in device_info['manufacturer'].lower() and 
                    'smartthings' in device_info['model_name'].lower()):
                    device_info['identified_as'] = 'Samsung SmartThings Hub'
                    device_info['confidence'] = 0.8
                
                devices[ip] = device_info
                
        except Exception as e:
            self.logger.error(f"UPnP discovery failed: {e}")
        
        return devices
    
    def _netdisco_discovery(self) -> Dict[str, Dict[str, Any]]:
        """Discover devices using netdisco IoT-specific discovery."""
        devices = {}
        
        try:
            netdis = NetworkDiscovery()
            netdis.scan()
            
            # Check for specific device types
            device_types = ['smartthings', 'philips_hue', 'sonos', 'google_cast', 'apple_tv']
            
            for device_type in device_types:
                try:
                    discovered = netdis.get_info(device_type)
                    for device in discovered:
                        ip = device.get('host', device.get('ip'))
                        if ip:
                            device_info = dict(device)
                            device_info['discovery_method'] = 'netdisco'
                            device_info['netdisco_type'] = device_type
                            device_info['confidence'] = 0.7
                            devices[ip] = device_info
                except Exception as e:
                    self.logger.debug(f"netdisco {device_type} discovery failed: {e}")
                    
        except Exception as e:
            self.logger.error(f"netdisco discovery failed: {e}")
        
        return devices
    
    def _add_http_fingerprints(self, devices: Dict[str, Dict[str, Any]]):
        """Add HTTP fingerprinting to all discovered devices."""
        
        def fingerprint_device(ip):
            return ip, self._http_fingerprint(ip)
        
        # Use ThreadPoolExecutor for parallel HTTP requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_ip = {executor.submit(fingerprint_device, ip): ip for ip in devices.keys()}
            
            for future in as_completed(future_to_ip, timeout=30):
                try:
                    ip, http_info = future.result(timeout=5)
                    devices[ip]['http_fingerprint'] = http_info
                except Exception as e:
                    self.logger.debug(f"HTTP fingerprinting failed for {future_to_ip.get(future)}: {e}")
    
    def _http_fingerprint(self, ip: str) -> Dict[str, Any]:
        """Perform HTTP fingerprinting on a device."""
        fingerprint = {'identified': False, 'info': {}}
        
        try:
            # Try common HTTP ports
            ports = [80, 8080, 443, 8443]
            
            for port in ports:
                try:
                    url = f"http://{ip}:{port}"
                    response = requests.get(url, timeout=3, allow_redirects=False)
                    
                    fingerprint['info'][f'port_{port}'] = {
                        'status_code': response.status_code,
                        'headers': dict(response.headers),
                        'content_preview': response.text[:500] if response.text else ''
                    }
                    
                    # Check for device signatures
                    for device_type, signature in self.device_signatures.items():
                        if self._matches_signature(response, signature):
                            fingerprint['identified'] = True
                            fingerprint['device_type'] = device_type
                            fingerprint['manufacturer'] = signature['manufacturer']
                            fingerprint['confidence'] = 0.8
                            break
                    
                    if fingerprint['identified']:
                        break
                        
                except requests.RequestException:
                    continue
                    
        except Exception as e:
            self.logger.debug(f"HTTP fingerprinting error for {ip}: {e}")
        
        return fingerprint
    
    def _matches_signature(self, response: requests.Response, signature: Dict[str, Any]) -> bool:
        """Check if HTTP response matches device signature."""
        
        # Check headers
        if 'http_headers' in signature:
            headers_text = ' '.join([f"{k}:{v}" for k, v in response.headers.items()]).lower()
            if any(header in headers_text for header in signature['http_headers']):
                return True
        
        # Check content
        if 'http_content' in signature and response.text:
            content_text = response.text.lower()
            if any(content in content_text for content in signature['http_content']):
                return True
        
        return False
    
    def _get_mac_vendor(self, mac_address: str) -> str:
        """Get vendor information from MAC address."""
        if not self.mac_lookup:
            return "Unknown"
        
        try:
            return self.mac_lookup.lookup(mac_address)
        except Exception:
            return "Unknown"
    
    def _extract_ip_from_url(self, url: str) -> Optional[str]:
        """Extract IP address from URL."""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.hostname
        except Exception:
            return None
    
    def _merge_device_info(self, devices: Dict[str, Dict[str, Any]], new_devices: Dict[str, Dict[str, Any]], source: str):
        """Merge new device information into existing devices dictionary."""
        for ip, device_info in new_devices.items():
            if ip in devices:
                # Merge information
                devices[ip][f'{source}_info'] = device_info
                devices[ip][f'{source}_detected'] = True
                
                # Update manufacturer if not already set
                if 'manufacturer' in device_info and 'manufacturer' not in devices[ip]:
                    devices[ip]['manufacturer'] = device_info['manufacturer']
                
                # Update device type if not already set
                if 'device_type' in device_info and 'device_type' not in devices[ip]:
                    devices[ip]['device_type'] = device_info['device_type']
            else:
                # New device
                devices[ip] = device_info
                devices[ip][f'{source}_detected'] = True
    
    def _calculate_confidence_score(self, device_data: Dict[str, Any]) -> float:
        """Calculate identification confidence based on multiple sources."""
        score = 0.0
        
        # Base score for being discovered
        score += 0.1
        
        # MAC vendor match with detected manufacturer
        if (device_data.get('mac_vendor') and device_data.get('manufacturer') and
            device_data['mac_vendor'].lower() in device_data['manufacturer'].lower()):
            score += 0.2
        
        # mDNS service detection (high confidence)
        if device_data.get('mdns_detected'):
            score += 0.4
        
        # UPnP device info (medium confidence)
        if device_data.get('upnp_detected') and device_data.get('upnp_info', {}).get('manufacturer'):
            score += 0.3
        
        # HTTP fingerprint match (high confidence)
        if device_data.get('http_fingerprint', {}).get('identified'):
            score += 0.5
        
        # netdisco detection (medium confidence)
        if device_data.get('netdisco_detected'):
            score += 0.3
        
        # Multiple method agreement bonus
        detection_sources = [s for s in ['nmap', 'mdns', 'upnp', 'netdisco'] 
                           if device_data.get(f'{s}_detected')]
        if len(detection_sources) >= 2:
            score += 0.2
        
        # Known IoT device type bonus
        if device_data.get('device_type') in ['washing_machine', 'thermostat', 'smart_speaker', 'SmartThings Hub']:
            score += 0.1
        
        return min(score, 1.0)
    
    def _is_likely_iot_device(self, device_data: Dict[str, Any]) -> bool:
        """Determine if device is likely an IoT device worth including."""
        
        # High confidence devices
        if device_data.get('confidence_score', 0) >= 0.6:
            return True
        
        # Devices with IoT-specific discovery methods
        if any(device_data.get(f'{method}_detected') for method in ['mdns', 'upnp', 'netdisco']):
            return True
        
        # Devices with known IoT manufacturers
        manufacturer = device_data.get('manufacturer', '').lower()
        iot_manufacturers = ['samsung', 'philips', 'sonos', 'nest', 'google', 'amazon', 'apple']
        if any(mfg in manufacturer for mfg in iot_manufacturers):
            return True
        
        # Devices with IoT-related services
        services = device_data.get('services', [])
        iot_services = ['smartthings', 'hue', 'homekit', 'matter', 'airplay', 'googlecast']
        if any(service for service in services if any(iot in service.lower() for iot in iot_services)):
            return True
        
        return False


def get_discovery_engine() -> ComprehensiveDeviceDiscovery:
    """
    Factory function to get a configured device discovery engine.
    
    Returns:
        ComprehensiveDeviceDiscovery instance ready for use
    """
    return ComprehensiveDeviceDiscovery()