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

logger = logging.getLogger(__name__)

class DeviceDiscoveryTool(Tool):
    name = "device_discovery"
    description = """
    Discover IoT devices on the network by scanning IP ranges and detecting services.
    Use this to find devices before trying to communicate with them.
    """
    
    def forward(self, ip_range: str = "192.168.1.0/24", ports: List[int] = None) -> Dict[str, Any]:
        """Discover devices on network"""
        
        if ports is None:
            ports = [80, 443, 502, 1883, 8080]  # Common IoT ports
        
        logger.info(f"Scanning network range: {ip_range}")
        
        # Simple ping-based discovery (replace with nmap in full implementation)
        discovered_devices = []
        
        # Extract IP range for simple scanning
        if "/" in ip_range:
            base_ip = ip_range.split("/")[0].rsplit(".", 1)[0]
            
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
                            "status": "online",
                            "open_ports": [],
                            "device_type": "unknown"
                        }
                        
                        # Check if common IoT ports are open
                        for port in [80, 443, 502]:
                            if self._check_port(ip, port):
                                device_info["open_ports"].append(port)
                        
                        # Infer device type from open ports
                        if 502 in device_info["open_ports"]:
                            device_info["device_type"] = "modbus_device"
                        elif 80 in device_info["open_ports"] or 443 in device_info["open_ports"]:
                            device_info["device_type"] = "web_device"
                        
                        discovered_devices.append(device_info)
                        logger.info(f"Found device at {ip}")
                        
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                    continue
        
        # Update device registry
        self._update_device_registry(discovered_devices)
        
        return {
            "discovered_devices": discovered_devices,
            "scan_range": ip_range,
            "total_found": len(discovered_devices)
        }
    
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
    
    def _update_device_registry(self, devices: List[Dict]):
        """Update the device registry file"""
        registry_path = Path("devices/discovered_devices.json")
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(registry_path, 'w') as f:
            json.dump({
                "last_scan": "2025-01-12T00:00:00Z",
                "devices": devices
            }, f, indent=2)


class DeviceControlTool(Tool):
    name = "device_control"
    description = """
    Control IoT devices by loading or generating communication tools and executing commands.
    This tool handles the complete workflow: spec generation, code generation, and execution.
    """
    
    def forward(self, device_ip: str, device_type: str, command: str, **kwargs) -> Dict[str, Any]:
        """Control a device by generating/using communication tools"""
        
        logger.info(f"Attempting to control {device_type} at {device_ip} with command: {command}")
        
        try:
            # Check if communication tool already exists
            tool_path = self._get_tool_path(device_type, device_ip)
            
            if not tool_path.exists():
                logger.info(f"No cached tool found, generating new one for {device_type}")
                success = self._generate_communication_tool(device_type, device_ip)
                if not success:
                    return {"error": f"Failed to generate communication tool for {device_type}"}
            
            # Load and use the communication tool
            result = self._execute_device_command(tool_path, command, **kwargs)
            
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
    
    def _generate_communication_tool(self, device_type: str, device_ip: str) -> bool:
        """Generate communication tool for device type"""
        
        # Look for appropriate documentation
        docs_path = Path("devices/raw_docs")
        device_docs = []
        
        for category_dir in docs_path.glob("*"):
            if category_dir.is_dir():
                for doc_file in category_dir.glob("*"):
                    # Simple matching - in production would use LLM analysis
                    if any(keyword in doc_file.name.lower() for keyword in [device_type, "smartthings", "api"]):
                        device_docs.append(doc_file)
        
        if not device_docs:
            logger.warning(f"No documentation found for {device_type}")
            return False
        
        # Use the first matching doc (in production, would analyze all)
        doc_file = device_docs[0]
        logger.info(f"Using documentation: {doc_file}")
        
        # Generate spec (simplified - would use LLM in production)
        spec = self._create_device_spec(device_type, device_ip, doc_file)
        
        # Generate communication code
        code = self._generate_device_code(device_type, device_ip, spec)
        
        # Save the generated code
        tool_path = self._get_tool_path(device_type, device_ip)
        tool_path.parent.mkdir(parents=True, exist_ok=True)
        tool_path.write_text(code)
        
        logger.info(f"Generated communication tool: {tool_path}")
        return True
    
    def _create_device_spec(self, device_type: str, device_ip: str, doc_file: Path) -> Dict:
        """Create device specification (simplified version)"""
        
        # In production, this would use the SpecAnalyzer with LLM
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
        else:
            # Generate TCP socket code
            return f'''
import socket
import time
import logging

logger = logging.getLogger(__name__)

class DeviceCommunicator:
    def __init__(self, device_ip="{device_ip}", port={spec.get("default_port", 502)}):
        self.device_ip = device_ip
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """Connect to device via TCP"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.device_ip, self.port))
            self.connected = True
            logger.info(f"Connected to {{self.device_ip}}:{{self.port}}")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {{e}}")
            return False
    
    def disconnect(self):
        """Disconnect from device"""
        if self.socket:
            self.socket.close()
        self.connected = False
    
    def read_status(self):
        """Read device status"""
        if not self.connected:
            self.connect()
        
        # Simple status read (would be protocol-specific in production)
        try:
            self.socket.send(b"\\x01\\x03\\x00\\x00\\x00\\x01")  # Sample Modbus read
            response = self.socket.recv(1024)
            return {{"raw_response": response.hex(), "status": "received"}}
        except Exception as e:
            logger.error(f"Status read failed: {{e}}")
            return {{"error": str(e)}}
    
    def send_command(self, command_data):
        """Send command to device"""
        if not self.connected:
            self.connect()
        
        try:
            if isinstance(command_data, str):
                command_data = command_data.encode()
            
            self.socket.send(command_data)
            response = self.socket.recv(1024)
            return {{"response": response.hex(), "status": "sent"}}
        except Exception as e:
            logger.error(f"Command failed: {{e}}")
            return {{"error": str(e)}}
'''
    
    def _execute_device_command(self, tool_path: Path, command: str, **kwargs) -> Dict:
        """Execute command using generated communication tool"""
        
        try:
            # Dynamically import the generated module
            spec = importlib.util.spec_from_file_location("device_comm", tool_path)
            device_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(device_module)
            
            # Create device communicator instance
            device_comm = device_module.DeviceCommunicator(**kwargs)
            
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
    
    def forward(self, device_type: str, credential_type: str, device_ip: str = None) -> Dict[str, Any]:
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