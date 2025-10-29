"""
Device Tools for AI-IoT Hub

These tools are used by the smolagents CodeAgent to discover devices,
generate communication code, and manage credentials.
"""

import json
import asyncio
import subprocess
import importlib.util
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml

from smolagents import Tool

# Import our comprehensive discovery engine
try:
    from ..discovery.comprehensive_discovery import get_discovery_engine
    HAS_COMPREHENSIVE_DISCOVERY = True
except ImportError:
    HAS_COMPREHENSIVE_DISCOVERY = False

logger = logging.getLogger(__name__)

class DeviceDiscoveryTool(Tool):
    name = "device_discovery"
    description = """
    Discover IoT devices on the network using comprehensive multi-method discovery.
    Uses nmap, mDNS, UPnP, and HTTP fingerprinting for accurate device identification.
    Use this to find devices before trying to communicate with them.
    """
    inputs = {
        "network_range": {
            "type": "string",
            "description": "CIDR network range to scan (e.g., '192.168.1.0/24')",
            "nullable": True
        },
        "timeout": {
            "type": "integer", 
            "description": "Maximum time to spend on discovery in seconds",
            "nullable": True
        }
    }
    output_type = "object"
    
    def __init__(self):
        super().__init__()
        self.discovery_engine = None
        if HAS_COMPREHENSIVE_DISCOVERY:
            try:
                self.discovery_engine = get_discovery_engine()
                logger.info("Initialized comprehensive device discovery engine")
            except Exception as e:
                logger.warning(f"Failed to initialize comprehensive discovery: {e}")
    
    def forward(self, network_range: str = "192.168.1.0/24", timeout: int = 30) -> Dict[str, Any]:
        """
        Discover devices on network using comprehensive multi-method approach.
        
        Args:
            network_range: CIDR network range to scan (e.g., "192.168.1.0/24")
            timeout: Maximum time to spend on discovery in seconds
            
        Returns:
            Dictionary with discovered devices and metadata
        """
        logger.info(f"Starting comprehensive device discovery on {network_range}")
        
        # Use comprehensive discovery if available
        if self.discovery_engine:
            try:
                discovered_devices = self.discovery_engine.discover_all_methods(
                    network_range=network_range, 
                    timeout=timeout
                )
                
                # Convert to simplified format for AI agent
                simplified_devices = []
                for ip, device_data in discovered_devices.items():
                    device_info = {
                        "ip": ip,
                        "hostname": device_data.get('hostname', ''),
                        "manufacturer": device_data.get('manufacturer', 'Unknown'),
                        "device_type": device_data.get('device_type', 'Unknown'),
                        "mac_address": device_data.get('mac', ''),
                        "confidence_score": device_data.get('confidence_score', 0.0),
                        "discovery_methods": [method for method in ['nmap', 'mdns', 'upnp', 'netdisco'] 
                                            if device_data.get(f'{method}_detected')],
                        "services": device_data.get('services', []),
                        "open_ports": list(device_data.get('services', {}).keys()) if isinstance(device_data.get('services'), dict) else []
                    }
                    
                    # Add SmartThings specific information
                    if 'smartthings' in device_info['manufacturer'].lower():
                        device_info['communication_protocol'] = 'smartthings_api'
                        device_info['requires_credentials'] = True
                        device_info['credential_types'] = ['access_token', 'device_id']
                    
                    # Add other device type specific info
                    elif 'philips' in device_info['manufacturer'].lower() and 'hue' in device_info['device_type'].lower():
                        device_info['communication_protocol'] = 'philips_hue_api'
                        device_info['requires_credentials'] = True
                        device_info['credential_types'] = ['username']
                    
                    elif 'modbus' in device_info.get('device_type', '').lower() or 502 in device_info['open_ports']:
                        device_info['communication_protocol'] = 'modbus_tcp'
                        device_info['requires_credentials'] = False
                    
                    simplified_devices.append(device_info)
                
                # Update device registry
                self._update_device_registry(simplified_devices)
                
                logger.info(f"Comprehensive discovery completed. Found {len(simplified_devices)} IoT devices")
                
                return {
                    "discovered_devices": simplified_devices,
                    "scan_range": network_range,
                    "total_found": len(simplified_devices),
                    "discovery_method": "comprehensive_multi_method",
                    "high_confidence_devices": [d for d in simplified_devices if d['confidence_score'] > 0.7]
                }
                
            except Exception as e:
                logger.error(f"Comprehensive discovery failed: {e}")
                # Check what dependencies are missing and provide helpful fallback
                missing_deps = self._check_discovery_dependencies()
                fallback_result = self._fallback_discovery(network_range)
                
                # Add warning about limited discovery capabilities
                fallback_result["warnings"] = [
                    f"Comprehensive discovery failed: {str(e)}",
                    f"Using basic ping-based discovery instead",
                    f"Missing dependencies: {missing_deps}" if missing_deps else "Check network connectivity"
                ]
                
                if missing_deps:
                    fallback_result["recommendations"] = [
                        "Install missing network discovery tools for better device identification:",
                        f"pip install {' '.join([d for d in missing_deps if 'nmap (binary)' not in d])}",
                        "Download Nmap from https://nmap.org/download.html" if any("nmap" in d for d in missing_deps) else None
                    ]
                    fallback_result["recommendations"] = [r for r in fallback_result["recommendations"] if r]
                
                return fallback_result
        
        else:
            logger.warning("Comprehensive discovery not available, using fallback method")
            return self._fallback_discovery(network_range)
    
    def _fallback_discovery(self, network_range: str) -> Dict[str, Any]:
        """Fallback discovery method when comprehensive discovery is not available."""
        logger.info(f"Using fallback ping-based discovery for {network_range}")
        
        discovered_devices = []
        
        # Extract IP range for simple scanning
        if "/" in network_range:
            base_ip = network_range.split("/")[0].rsplit(".", 1)[0]
            
            # Scan first 10 IPs for demo (would be full range in production)
            for i in range(1, 11):
                ip = f"{base_ip}.{i}"
                
                # Try to ping the IP
                try:
                    result = subprocess.run(
                        ["ping", "-n", "1", "-w", "1000", ip], 
                        capture_output=True, 
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        # Try to detect device type by checking common ports
                        device_info = {
                            "ip": ip,
                            "hostname": "",
                            "manufacturer": "Unknown",
                            "device_type": "Unknown",
                            "mac_address": "",
                            "confidence_score": 0.3,  # Low confidence for fallback method
                            "discovery_methods": ["ping"],
                            "services": [],
                            "open_ports": []
                        }
                        
                        # Check if common IoT ports are open
                        for port in [80, 443, 502, 1883, 8080]:
                            if self._check_port(ip, port):
                                device_info["open_ports"].append(port)
                        
                        # Infer device type from open ports (basic heuristics)
                        if 502 in device_info["open_ports"]:
                            device_info["device_type"] = "modbus_device"
                            device_info["communication_protocol"] = "modbus_tcp"
                            device_info["requires_credentials"] = False
                            device_info["confidence_score"] = 0.5
                        elif 1883 in device_info["open_ports"]:
                            device_info["device_type"] = "mqtt_device"
                            device_info["communication_protocol"] = "mqtt"
                        elif 80 in device_info["open_ports"] or 443 in device_info["open_ports"]:
                            device_info["device_type"] = "web_device"
                            device_info["communication_protocol"] = "http"
                        
                        discovered_devices.append(device_info)
                        logger.info(f"Found device at {ip} (fallback method)")
                        
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                    continue
        
        # Update device registry
        self._update_device_registry(discovered_devices)
        
        # Check what's missing and provide guidance
        missing_deps = self._check_discovery_dependencies()
        
        result = {
            "discovered_devices": discovered_devices,
            "scan_range": network_range,
            "total_found": len(discovered_devices),
            "discovery_method": "ping_fallback",
            "limitations": [
                "Using basic ping-based discovery only",
                "Cannot identify device manufacturers or specific models",
                "Limited protocol detection capabilities"
            ]
        }
        
        if missing_deps:
            result["missing_dependencies"] = missing_deps
            result["recommendations"] = [
                "Install missing tools for comprehensive device identification:",
                f"pip install {' '.join([d for d in missing_deps if 'nmap (binary)' not in d])}",
                "Download Nmap from https://nmap.org/download.html" if any("nmap" in d for d in missing_deps) else None
            ]
            result["recommendations"] = [r for r in result["recommendations"] if r]
        
        return result
    
    def _check_port(self, ip: str, port: int, timeout: float = 1.0) -> bool:
        """Check if a port is open on given IP"""
        import socket
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _check_discovery_dependencies(self) -> List[str]:
        """Check which discovery dependencies are missing"""
        missing = []
        
        # Check for nmap binary
        import subprocess
        try:
            subprocess.run(['nmap', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append("nmap (binary)")
        
        # Check Python packages
        dependencies = [
            ("upnpclient", "upnpclient"),
            ("netdisco", "netdisco"), 
            ("zeroconf", "zeroconf"),
            ("mac_vendor_lookup", "mac-vendor-lookup")
        ]
        
        for import_name, package_name in dependencies:
            try:
                __import__(import_name)
            except ImportError:
                missing.append(package_name)
        
        return missing

    def _update_device_registry(self, devices: List[Dict[str, Any]]):
        """Update the device registry file"""
        registry_path = Path("devices/discovered_devices.json")
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add timestamp and discovery metadata
        registry_data = {
            "last_scan": "2025-10-12T12:00:00Z",  # Would use actual timestamp
            "discovery_engine": "comprehensive" if self.discovery_engine else "fallback",
            "total_devices": len(devices),
            "high_confidence_devices": len([d for d in devices if d.get('confidence_score', 0) > 0.7]),
            "devices": devices
        }
        
        with open(registry_path, 'w') as f:
            json.dump(registry_data, f, indent=2)
        
        logger.info(f"Updated device registry with {len(devices)} devices")


class DeviceControlTool(Tool):
    name = "device_control"
    description = """
    Control IoT devices by loading or generating communication tools and executing commands.
    This tool handles the complete workflow: spec generation, code generation, and execution.
    """
    inputs = {
        "device_ip": {
            "type": "string",
            "description": "IP address of the device to control"
        },
        "device_type": {
            "type": "string", 
            "description": "Type of device (e.g., 'washing_machine', 'thermostat')"
        },
        "command": {
            "type": "string",
            "description": "Command to execute on the device"
        }
    }
    output_type = "object"
    
    def forward(self, device_ip: str, device_type: str, command: str) -> Dict[str, Any]:
        """Control a device by generating/using communication tools"""
        
        logger.info(f"Attempting to control {device_type} at {device_ip} with command: {command}")
        
        try:
            # Check if communication tool already exists
            tool_path = self._get_tool_path(device_type, device_ip)
            
            if not tool_path.exists():
                logger.info(f"No cached tool found, generating new one for {device_type}")
                generation_result = self._generate_communication_tool(device_type, device_ip)
                
                if not generation_result["success"]:
                    # Return detailed error information instead of generic failure
                    error_response = {
                        "device_ip": device_ip,
                        "device_type": device_type,
                        "command": command,
                        "status": "failed", 
                        "error": generation_result["error"],
                        "message": generation_result["message"]
                    }
                    
                    # Add specific guidance based on error type
                    if generation_result["error"] == "missing_dependencies":
                        error_response["required_action"] = "Install missing network discovery tools"
                        error_response["install_command"] = f"pip install {' '.join(generation_result['missing_deps'])}"
                        if "nmap (binary)" in generation_result["missing_deps"]:
                            error_response["additional_setup"] = "Download and install Nmap from https://nmap.org/download.html"
                    
                    elif generation_result["error"] == "no_documentation":
                        error_response["required_action"] = "Add device documentation"
                        error_response["suggestions"] = generation_result["suggestions"]
                    
                    return error_response
            
            # Load and use the communication tool
            result = self._execute_device_command(tool_path, command)
            
            return {
                "device_ip": device_ip,
                "device_type": device_type, 
                "command": command,
                "result": result,
                "status": "success"
            }
            
        except Exception as e:
            error_msg = f"Error controlling device: {e}"
            logger.error(error_msg)
            return {"error": error_msg, "status": "failed"}
    
    def _get_tool_path(self, device_type: str, device_ip: str) -> Path:
        """Get path to communication tool for device"""
        cache_key = f"{device_type}_{device_ip.replace('.', '_')}"
        return Path(f"tools/generated/{cache_key}.py")
    
    def _check_discovery_dependencies(self) -> List[str]:
        """Check which discovery dependencies are missing"""
        missing = []
        
        # Check for nmap binary
        import subprocess
        try:
            subprocess.run(['nmap', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append("nmap (binary)")
        
        # Check Python packages
        dependencies = [
            ("upnpclient", "upnpclient"),
            ("netdisco", "netdisco"), 
            ("zeroconf", "zeroconf"),
            ("mac_vendor_lookup", "mac-vendor-lookup")
        ]
        
        for import_name, package_name in dependencies:
            try:
                __import__(import_name)
            except ImportError:
                missing.append(package_name)
        
        return missing
    
    def _generate_communication_tool(self, device_type: str, device_ip: str) -> Dict[str, Any]:
        """Generate communication tool for device type with detailed error reporting"""
        
        # Check for missing discovery dependencies first
        missing_deps = self._check_discovery_dependencies()
        if missing_deps:
            logger.error(f"Cannot generate proper device code for {device_type} - missing dependencies: {missing_deps}")
            return {
                "success": False, 
                "error": "missing_dependencies",
                "missing_deps": missing_deps,
                "message": f"Cannot identify {device_type} properly due to missing network discovery tools. Install: {', '.join(missing_deps)}"
            }
        
        # Look for appropriate documentation
        docs_path = Path("devices/raw_docs")
        device_docs = []
        
        for category_dir in docs_path.glob("*"):
            if category_dir.is_dir():
                for doc_file in category_dir.glob("*"):
                    # Simple matching - in production would use LLM analysis
                    if any(keyword in doc_file.name.lower() for keyword in [device_type, "router", "gateway", "smartthings", "api"]):
                        device_docs.append(doc_file)
        
        if not device_docs:
            logger.error(f"No documentation found for {device_type} at {device_ip}")
            return {
                "success": False,
                "error": "no_documentation", 
                "message": f"No API documentation found for {device_type}. Please add manufacturer documentation to devices/raw_docs/ folder.",
                "suggestions": [
                    f"Create devices/raw_docs/{device_type}/ folder",
                    f"Add manufacturer API documentation (PDF, URL in .txt file, etc.)",
                    f"Alternatively, provide the device manual or API specification"
                ]
            }
        
        # Use the first matching doc (in production, would analyze all)
        doc_file = device_docs[0]
        logger.info(f"Using documentation: {doc_file}")
        
        # Generate spec (simplified - would use LLM in production)
        spec = self._create_device_spec(device_type, device_ip, doc_file)
        
        # Generate communication code
        try:
            code = self._generate_device_code(device_type, device_ip, spec)
            
            # Save the generated code
            tool_path = self._get_tool_path(device_type, device_ip)
            tool_path.parent.mkdir(parents=True, exist_ok=True)
            tool_path.write_text(code)
            
            logger.info(f"Generated communication tool: {tool_path}")
            return {
                "success": True,
                "tool_path": str(tool_path),
                "message": f"Successfully generated communication tool for {device_type}"
            }
        except Exception as e:
            logger.error(f"Code generation failed for {device_type}: {e}")
            return {
                "success": False,
                "error": "code_generation_failed",
                "message": f"Failed to generate communication code: {str(e)}"
            }
    
    def _create_device_spec(self, device_type: str, device_ip: str, doc_file: Path) -> Dict:
        """Create device specification (simplified version)"""
        
        # CodeAgent processes documents directly during code generation
        if "smartthings" in doc_file.name.lower():
            return {
                "device_type": device_type,
                "protocol": "rest",
                "base_url": "https://api.smartthings.com/v1",
                "authentication": {"type": "bearer_token"},
                "endpoints": [
                    {"name": "get_status", "method": "GET", "path": "/devices/{deviceId}/status"},
                    {"name": "execute_command", "method": "POST", "path": "/devices/{deviceId}/commands"}
                ]
            }
        else:
            # Default to simple TCP
            return {
                "device_type": device_type,
                "protocol": "tcp",
                "default_port": 502,
                "endpoints": [
                    {"name": "connect", "description": "Connect to device"},
                    {"name": "read_status", "description": "Read device status"}
                ]
            }
    
    def _generate_device_code(self, device_type: str, device_ip: str, spec: Dict) -> str:
        """Generate Python communication code"""
        
        if spec["protocol"] == "rest":
            # Generate REST API code
            return f'''
import requests
import json
import logging

logger = logging.getLogger(__name__)

class DeviceCommunicator:
    def __init__(self, device_ip="{device_ip}", device_id=None, access_token=None):
        self.device_ip = device_ip
        self.device_id = device_id
        self.access_token = access_token
        self.base_url = "{spec.get("base_url", "http://" + device_ip)}"
        self.headers = {{"Authorization": f"Bearer {{self.access_token}}"}}
        self.connected = False
    
    def connect(self):
        """Connect to device"""
        try:
            response = requests.get(f"{{self.base_url}}/devices/{{self.device_id}}/health", 
                                  headers=self.headers, timeout=10)
            response.raise_for_status()
            self.connected = True
            return True
        except Exception as e:
            logger.error(f"Connection failed: {{e}}")
            return False
    
    def disconnect(self):
        """Disconnect from device"""
        self.connected = False
    
    def get_status(self):
        """Get device status"""
        if not self.connected:
            self.connect()
        
        response = requests.get(f"{{self.base_url}}/devices/{{self.device_id}}/status",
                              headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def execute_command(self, command, **kwargs):
        """Execute device command"""
        if not self.connected:
            self.connect()
        
        payload = {{"commands": [command]}}
        response = requests.post(f"{{self.base_url}}/devices/{{self.device_id}}/commands",
                               headers=self.headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
'''
        elif spec["protocol"] == "modbus_tcp":
            # Generate proper Modbus TCP code only if we have proper device identification
            return f'''"""
Generated Modbus TCP communication for {device_type} at {device_ip}
This code was generated because port 502 was detected as open.
"""
import socket
import time
import logging

logger = logging.getLogger(__name__)

class DeviceCommunicator:
    def __init__(self, device_ip="{device_ip}", port=502):
        self.device_ip = device_ip
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """Connect to Modbus device via TCP"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.device_ip, self.port))
            self.connected = True
            logger.info(f"Connected to Modbus device at {{self.device_ip}}:{{self.port}}")
            return True
        except Exception as e:
            logger.error(f"Modbus connection failed: {{e}}")
            return False
    
    def disconnect(self):
        """Disconnect from Modbus device"""
        if self.socket:
            self.socket.close()
        self.connected = False
    
    def read_holding_registers(self, start_address=0, count=1):
        """Read Modbus holding registers"""
        if not self.connected:
            self.connect()
        
        # Basic Modbus TCP frame for reading holding registers
        # Note: This is a simplified implementation
        transaction_id = 0
        protocol_id = 0
        length = 6
        unit_id = 1
        function_code = 3  # Read holding registers
        
        # Build Modbus TCP frame
        frame = (
            transaction_id.to_bytes(2, 'big') +
            protocol_id.to_bytes(2, 'big') +
            length.to_bytes(2, 'big') +
            unit_id.to_bytes(1, 'big') +
            function_code.to_bytes(1, 'big') +
            start_address.to_bytes(2, 'big') +
            count.to_bytes(2, 'big')
        )
        
        try:
            self.socket.send(frame)
            response = self.socket.recv(1024)
            # Basic response parsing (simplified)
            if len(response) >= 9:
                return {{"raw_response": response.hex(), "status": "success"}}
            else:
                return {{"error": "Invalid response length"}}
        except Exception as e:
            logger.error(f"Modbus read failed: {{e}}")
            return {{"error": str(e)}}
'''
        else:
            # Refuse to generate generic code - require proper documentation
            raise ValueError(
                f"Cannot generate communication code for {device_type} with protocol '{spec.get('protocol', 'unknown')}'. "
                f"This device requires specific manufacturer documentation to generate proper communication code. "
                f"Please add API documentation to devices/raw_docs/{device_type}/ folder."
            )
    
    def _execute_device_command(self, tool_path: Path, command: str) -> Dict:
        """Execute command using generated communication tool"""
        
        try:
            # Dynamically import the generated module
            spec = importlib.util.spec_from_file_location("device_comm", tool_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load module from {tool_path}")
            device_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(device_module)
            
            # Create device communicator instance - use default constructor
            device_comm = device_module.DeviceCommunicator()
            
            # Execute the command
            if hasattr(device_comm, command):
                result = getattr(device_comm, command)()
            elif command == "status":
                result = device_comm.get_status() if hasattr(device_comm, 'get_status') else device_comm.read_status()
            elif command == "connect":
                result = device_comm.connect()
            else:
                result = {"error": f"Unknown command: {command}"}
            
            # Clean up
            if hasattr(device_comm, 'disconnect'):
                device_comm.disconnect()
            
            return result
            
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return {"error": str(e)}


class CredentialManagerTool(Tool):
    name = "credential_manager"
    description = """
    Manage device credentials (API tokens, passwords, device IDs) securely.
    Prompts user for missing credentials and stores them in config file.
    """
    inputs = {
        "device_type": {
            "type": "string",
            "description": "Type of device needing credentials"
        },
        "credential_type": {
            "type": "string",
            "description": "Type of credential needed (access_token, device_id, api_key, etc.)"
        },
        "device_ip": {
            "type": "string",
            "description": "IP address of the device (optional)",
            "nullable": True
        }
    }
    output_type = "object"
    
    def forward(self, device_type: str, credential_type: str, device_ip: Optional[str] = None) -> Dict[str, Any]:
        """Get or set device credentials"""
        
        config_path = Path("config/hub_config.yaml")
        
        # Load current config
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
        else:
            config = {"credentials": {}}
        
        credentials = config.get("credentials", {})
        
        # Create credential key
        cred_key = f"{device_type}_{device_ip}" if device_ip else device_type
        
        # Check if credential exists
        if cred_key in credentials and credential_type in credentials[cred_key]:
            return {
                "status": "found",
                "message": f"Credential {credential_type} found for {cred_key}"
            }
        
        # Prompt user for missing credential
        credential_prompts = {
            "access_token": f"SmartThings Personal Access Token for {device_type}",
            "device_id": f"Device ID for {device_type} at {device_ip}",
            "api_key": f"API key for {device_type}",
            "username": f"Username for {device_type}",
            "password": f"Password for {device_type}"
        }
        
        prompt = credential_prompts.get(credential_type, f"{credential_type} for {device_type}")
        
        return {
            "status": "missing",
            "message": f"Please provide {prompt}",
            "prompt": f"Enter {prompt}: ",
            "store_as": cred_key,
            "credential_type": credential_type
        }
    
    def store_credential(self, store_key: str, credential_type: str, value: str):
        """Store credential in config file"""
        
        config_path = Path("config/hub_config.yaml") 
        
        # Load current config
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
        else:
            config = {"credentials": {}}
        
        # Store credential
        if "credentials" not in config:
            config["credentials"] = {}
        
        if store_key not in config["credentials"]:
            config["credentials"][store_key] = {}
        
        config["credentials"][store_key][credential_type] = value
        
        # Save config
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            yaml.dump(config, f, indent=2)
        
        logger.info(f"Stored {credential_type} for {store_key}")
        
        return {"status": "stored", "message": f"Credential {credential_type} stored for {store_key}"}