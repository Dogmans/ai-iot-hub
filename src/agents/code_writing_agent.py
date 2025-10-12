"""
Device Code Writing Agent

Uses smolagents CodeAgent to dynamically generate Python communication code
for IoT devices based on parsed specifications.
"""

from smolagents import CodeAgent, InferenceClientModel
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

class DeviceCodeAgent:
    def __init__(self, model=None):
        self.model = model or InferenceClientModel()
        self.agent = CodeAgent(
            tools=[],
            model=self.model,
            additional_authorized_imports=[
                'socket', 'requests', 'asyncio', 'json', 'time',
                'paho.mqtt.client', 'pymodbus.client', 'websockets'
            ]
        )
    
    async def generate_device_communicator(self, device_ip, device_type):
        """Generate Python communication code for specific device"""
        spec_path = Path(f"devices/generated_specs/{device_type}_spec.json")
        
        if not spec_path.exists():
            raise FileNotFoundError(f"No spec found for device type: {device_type}")
        
        with open(spec_path) as f:
            spec = json.load(f)
        
        # Create prompt for code generation
        prompt = self._create_generation_prompt(device_ip, device_type, spec)
        
        logger.info(f"[CODE_GEN] Generating communicator for {device_type} at {device_ip}")
        
        # Use CodeAgent to generate the communication code
        result = self.agent.run(prompt)
        
        # Extract generated Python code from result
        generated_code = self._extract_python_code(result)
        
        return generated_code
    
    def _create_generation_prompt(self, device_ip, device_type, spec):
        """Create prompt for smolagents CodeAgent"""
        protocol = spec.get('protocol', 'unknown')
        endpoints = spec.get('endpoints', [])
        
        prompt = f"""
Generate a Python class called 'DeviceCommunicator' for a {device_type} device at IP {device_ip}.

Device Specification:
- Protocol: {protocol}
- IP Address: {device_ip}
- Available Endpoints: {json.dumps(endpoints, indent=2)}

Requirements:
1. Create a class that can communicate using the specified protocol
2. Implement methods for each endpoint/command
3. Handle authentication if required
4. Include proper error handling and timeouts
5. Use appropriate libraries ({self._get_protocol_libraries(protocol)})

Example method structure:
```python
class DeviceCommunicator:
    def __init__(self, ip_address="{device_ip}"):
        self.ip = ip_address
        # Protocol-specific initialization
        
    def connect(self):
        # Establish connection
        
    def disconnect(self):
        # Clean up connection
        
    # Generate methods based on endpoints...
```

Generate the complete, working Python code.
"""
        return prompt
    
    def _get_protocol_libraries(self, protocol):
        """Map protocols to required libraries"""
        protocol_map = {
            'tcp': 'socket',
            'http': 'requests', 
            'rest': 'requests',
            'modbus_tcp': 'pymodbus.client',
            'mqtt': 'paho.mqtt.client',
            'websocket': 'websockets'
        }
        return protocol_map.get(protocol.lower(), 'socket')
    
    def _extract_python_code(self, agent_result):
        """Extract Python code from CodeAgent result"""
        # TODO: Implement proper code extraction from agent output
        # This would parse the agent's generated response to extract the Python code
        
        # For now, return a template
        template_code = '''
import socket
import json
import time
import logging

logger = logging.getLogger(__name__)

class DeviceCommunicator:
    def __init__(self, ip_address, port=502, timeout=5):
        self.ip = ip_address
        self.port = port
        self.timeout = timeout
        self.connected = False
        
    def connect(self):
        """Establish connection to device"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.ip, self.port))
            self.connected = True
            logger.info(f"Connected to device at {self.ip}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close connection to device"""
        if hasattr(self, 'socket'):
            self.socket.close()
            self.connected = False
            logger.info(f"Disconnected from {self.ip}")
    
    def send_command(self, command_data):
        """Send command to device"""
        if not self.connected:
            if not self.connect():
                raise ConnectionError("Unable to connect to device")
        
        try:
            if isinstance(command_data, dict):
                command_data = json.dumps(command_data)
            
            self.socket.send(command_data.encode())
            response = self.socket.recv(1024).decode()
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise
'''
        return template_code