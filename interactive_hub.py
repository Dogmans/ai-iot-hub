#!/usr/bin/env python3
"""
Simplified AI-IoT Hub Interface (No Dependencies)

Demonstrates the LLM-powered IoT device communication workflow
without requiring external dependencies. Shows the complete interaction pattern.
"""

import json
import os
import sys
from pathlib import Path

class SimpleAIIoTHub:
    """Simplified AI-IoT Hub for demonstration"""
    
    def __init__(self):
        self.config_path = Path("config/hub_config.yaml")
        self.config = self._load_config()
        
    def _load_config(self):
        """Load or create default configuration"""
        config_file = Path("config/credentials.json")
        
        if config_file.exists():
            with open(config_file) as f:
                return json.load(f)
        else:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            default_config = {
                "credentials": {},
                "devices": {},
                "model_config": {
                    "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
                    "temperature": 0.1
                }
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def _save_config(self):
        """Save current configuration"""
        with open("config/credentials.json", 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def process_user_request(self, user_input: str) -> str:
        """Process user request and return AI response"""
        
        print(f"\n🧠 AI-IoT Hub analyzing request: '{user_input}'")
        
        # Simulate LLM reasoning about the request
        analysis = self._analyze_request(user_input)
        
        if analysis["action"] == "discover_devices":
            return self._discover_devices()
            
        elif analysis["action"] == "control_device":
            return self._control_device(
                analysis["device_ip"], 
                analysis["device_type"], 
                analysis["command"]
            )
            
        elif analysis["action"] == "check_status":
            return self._check_device_status(
                analysis["device_ip"],
                analysis["device_type"]
            )
            
        else:
            return self._general_help()
    
    def _analyze_request(self, user_input: str) -> dict:
        """Simulate LLM analysis of user request"""
        
        user_lower = user_input.lower()
        
        # Extract IP addresses
        import re
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, user_input)
        
        # Analyze intent
        if any(word in user_lower for word in ["discover", "find", "scan", "search"]):
            return {"action": "discover_devices"}
            
        elif any(word in user_lower for word in ["start", "turn on", "activate", "run"]) and "wash" in user_lower:
            return {
                "action": "control_device",
                "device_ip": ips[0] if ips else "192.168.0.5",
                "device_type": "washing_machine", 
                "command": "start_wash_cycle"
            }
            
        elif any(word in user_lower for word in ["stop", "turn off", "halt"]) and "wash" in user_lower:
            return {
                "action": "control_device",
                "device_ip": ips[0] if ips else "192.168.0.5",
                "device_type": "washing_machine",
                "command": "stop_wash_cycle"
            }
            
        elif any(word in user_lower for word in ["status", "check", "state"]):
            device_type = "washing_machine" if "wash" in user_lower else "sensor" if "sensor" in user_lower else "device"
            return {
                "action": "check_status",
                "device_ip": ips[0] if ips else "192.168.0.5", 
                "device_type": device_type
            }
            
        else:
            return {"action": "help"}
    
    def _discover_devices(self) -> str:
        """Simulate device discovery"""
        
        print("🔍 Scanning network for IoT devices...")
        
        # Simulate discovered devices
        discovered = [
            {"ip": "192.168.0.5", "type": "washing_machine", "manufacturer": "Samsung SmartThings"},
            {"ip": "192.168.1.20", "type": "thermostat", "manufacturer": "Nest"},
            {"ip": "192.168.1.50", "type": "sensor", "manufacturer": "Modbus TCP"}
        ]
        
        # Update device registry
        self.config["devices"] = {device["ip"]: device for device in discovered}
        self._save_config()
        
        response = "✅ **Device Discovery Complete**\n\n"
        response += f"Found {len(discovered)} IoT devices on your network:\n\n"
        
        for device in discovered:
            response += f"🔸 **{device['type'].replace('_', ' ').title()}** at `{device['ip']}`\n"
            response += f"   Manufacturer: {device['manufacturer']}\n"
            
            # Check if we have communication tools
            tool_path = self._get_tool_path(device['type'], device['ip'])
            if tool_path.exists():
                response += f"   Status: ✅ Communication tool ready\n\n"
            else:
                response += f"   Status: 🔧 Will generate communication tool when needed\n\n"
        
        response += "💡 **You can now control these devices!** Try commands like:\n"
        response += "• 'Start washing machine at 192.168.0.5'\n"
        response += "• 'Check status of thermostat at 192.168.1.20'\n"
        response += "• 'Read sensor at 192.168.1.50'\n"
        
        return response
    
    def _control_device(self, device_ip: str, device_type: str, command: str) -> str:
        """Control a specific device"""
        
        print(f"🎮 Controlling {device_type} at {device_ip}...")
        
        # Check if communication tool exists
        tool_path = self._get_tool_path(device_type, device_ip)
        
        if not tool_path.exists():
            print("📝 No communication tool found, generating one...")
            result = self._generate_communication_tool(device_type, device_ip)
            if not result["success"]:
                return f"❌ **Error**: {result['error']}"
        
        # Check for credentials
        cred_result = self._check_credentials(device_type, device_ip)
        if cred_result["missing_credentials"]:
            return self._prompt_for_credentials(cred_result["missing_credentials"], device_type, device_ip)
        
        # Simulate command execution
        print(f"⚡ Executing {command} on {device_type}...")
        
        if device_type == "washing_machine":
            if command == "start_wash_cycle":
                return f"✅ **Washing machine started successfully!**\n\n" \
                       f"🔹 Device: {device_ip}\n" \
                       f"🔹 Cycle: Normal wash (30 minutes)\n" \
                       f"🔹 Status: Running\n" \
                       f"🔹 API: SmartThings REST API\n\n" \
                       f"💡 You can check progress with: 'Check status of washing machine at {device_ip}'"
                       
            elif command == "stop_wash_cycle":
                return f"⏹️ **Washing machine stopped successfully!**\n\n" \
                       f"🔹 Device: {device_ip}\n" \
                       f"🔹 Previous status: Running → Stopped\n" \
                       f"🔹 API: SmartThings REST API"
        
        return f"✅ **Command executed**: {command} on {device_type} at {device_ip}"
    
    def _check_device_status(self, device_ip: str, device_type: str) -> str:
        """Check device status"""
        
        print(f"📊 Checking status of {device_type} at {device_ip}...")
        
        # Simulate status check
        if device_type == "washing_machine":
            status = {
                "operating_state": "run",
                "mode": "normal", 
                "completion_time": "15 minutes remaining",
                "temperature": "40°C",
                "spin_speed": "1200 RPM"
            }
            
            response = f"📱 **Washing Machine Status** (`{device_ip}`)\n\n"
            response += f"🔸 **State**: {status['operating_state'].title()}\n"
            response += f"🔸 **Mode**: {status['mode'].title()}\n"
            response += f"🔸 **Time Remaining**: {status['completion_time']}\n" 
            response += f"🔸 **Temperature**: {status['temperature']}\n"
            response += f"🔸 **Spin Speed**: {status['spin_speed']}\n\n"
            response += f"🔗 **Protocol**: SmartThings REST API\n"
            response += f"📡 **Connection**: HTTPS via Samsung SmartThings Cloud"
            
        elif device_type == "thermostat":
            status = {
                "current_temp": "22°C",
                "target_temp": "23°C", 
                "mode": "heat",
                "humidity": "45%"
            }
            
            response = f"🌡️ **Thermostat Status** (`{device_ip}`)\n\n"
            response += f"🔸 **Current**: {status['current_temp']}\n"
            response += f"🔸 **Target**: {status['target_temp']}\n"
            response += f"🔸 **Mode**: {status['mode'].title()}\n"
            response += f"🔸 **Humidity**: {status['humidity']}\n\n"
            response += f"🔗 **Protocol**: Nest REST API"
            
        else:
            response = f"📊 **Device Status** (`{device_ip}`)\n\n"
            response += f"🔸 **Type**: {device_type.replace('_', ' ').title()}\n"
            response += f"🔸 **Connection**: Online\n"
            response += f"🔸 **Last Update**: Just now\n"
            
        return response
    
    def _get_tool_path(self, device_type: str, device_ip: str) -> Path:
        """Get path to communication tool"""
        cache_key = f"{device_type}_{device_ip.replace('.', '_')}"
        return Path(f"tools/generated/{cache_key}.py")
    
    def _generate_communication_tool(self, device_type: str, device_ip: str) -> dict:
        """Generate communication tool for device"""
        
        # Look for documentation
        docs_found = []
        docs_path = Path("devices/raw_docs")
        
        for category_dir in docs_path.glob("*"):
            if category_dir.is_dir():
                for doc_file in category_dir.glob("*"):
                    if "smartthings" in doc_file.name.lower() or device_type in doc_file.name.lower():
                        docs_found.append(doc_file)
        
        if not docs_found:
            return {"success": False, "error": f"No documentation found for {device_type}. Please add API docs to devices/raw_docs/"}
        
        doc_file = docs_found[0]
        print(f"📄 Using documentation: {doc_file}")
        
        # Simulate LLM generating communication code
        print("🧠 LLM analyzing device documentation...")
        print("🔧 Generating Python communication code...")
        
        # Create the tool
        tool_path = self._get_tool_path(device_type, device_ip)
        tool_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate SmartThings communication code
        code = self._generate_smartthings_code(device_type, device_ip)
        tool_path.write_text(code)
        
        print(f"✅ Generated communication tool: {tool_path}")
        
        return {"success": True, "tool_path": tool_path}
    
    def _generate_smartthings_code(self, device_type: str, device_ip: str) -> str:
        """Generate SmartThings communication code"""
        
        return f'''"""
Generated {device_type.title()} Communication Tool
Device IP: {device_ip}
Protocol: SmartThings REST API
Generated by AI-IoT Hub LLM Agent
"""

import requests
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DeviceCommunicator:
    def __init__(self, device_ip="{device_ip}", device_id=None, access_token=None):
        self.device_ip = device_ip
        self.device_id = device_id or "your-smartthings-device-id"
        self.access_token = access_token or "your-smartthings-access-token"
        self.base_url = "https://api.smartthings.com/v1"
        self.headers = {{
            "Authorization": f"Bearer {{self.access_token}}",
            "Content-Type": "application/json"
        }}
        self.connected = False
    
    def connect(self) -> bool:
        """Establish connection to SmartThings API"""
        try:
            # Test API connection
            response = requests.get(
                f"{{self.base_url}}/devices/{{self.device_id}}/health",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.connected = True
                logger.info(f"Connected to SmartThings device {{self.device_id}}")
                return True
            else:
                logger.error(f"SmartThings API error: {{response.status_code}}")
                return False
                
        except Exception as e:
            logger.error(f"Connection failed: {{e}}")
            return False
    
    def disconnect(self):
        """Disconnect (SmartThings API is stateless)"""
        self.connected = False
        logger.info("Disconnected from SmartThings API")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current device status"""
        if not self.connected:
            self.connect()
        
        try:
            response = requests.get(
                f"{{self.base_url}}/devices/{{self.device_id}}/status",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Status check failed: {{e}}")
            return {{"error": str(e)}}
    
    def start_wash_cycle(self, mode: str = "normal") -> Dict[str, Any]:
        """Start washing machine cycle"""
        if not self.connected:
            self.connect()
        
        commands = [{{
            "component": "main",
            "capability": "washerOperatingState",
            "command": "setMachineState", 
            "arguments": ["run"]
        }}]
        
        try:
            response = requests.post(
                f"{{self.base_url}}/devices/{{self.device_id}}/commands",
                headers=self.headers,
                json={{"commands": commands}},
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f"Started {{mode}} wash cycle")
            return {{"status": "started", "mode": mode, "response": response.json()}}
            
        except Exception as e:
            logger.error(f"Start cycle failed: {{e}}")
            return {{"error": str(e)}}
    
    def stop_wash_cycle(self) -> Dict[str, Any]:
        """Stop washing machine cycle"""
        if not self.connected:
            self.connect()
        
        commands = [{{
            "component": "main", 
            "capability": "washerOperatingState",
            "command": "setMachineState",
            "arguments": ["stop"]
        }}]
        
        try:
            response = requests.post(
                f"{{self.base_url}}/devices/{{self.device_id}}/commands",
                headers=self.headers,
                json={{"commands": commands}},
                timeout=10
            )
            response.raise_for_status()
            
            logger.info("Stopped wash cycle")
            return {{"status": "stopped", "response": response.json()}}
            
        except Exception as e:
            logger.error(f"Stop cycle failed: {{e}}")
            return {{"error": str(e)}}

# Example usage:
if __name__ == "__main__":
    washer = DeviceCommunicator(
        device_ip="{device_ip}",
        device_id="your-device-id", 
        access_token="your-pat-token"
    )
    
    if washer.connect():
        status = washer.get_status()
        print(f"Status: {{status}}")
        
        washer.start_wash_cycle("delicate")
        
    washer.disconnect()
'''
    
    def _check_credentials(self, device_type: str, device_ip: str) -> dict:
        """Check if required credentials are available"""
        
        cred_key = f"{device_type}_{device_ip}"
        device_creds = self.config["credentials"].get(cred_key, {})
        
        required_creds = {
            "washing_machine": ["access_token", "device_id"],
            "thermostat": ["access_token", "device_id"], 
            "sensor": []  # Modbus typically doesn't need auth
        }
        
        missing = []
        for cred in required_creds.get(device_type, []):
            if cred not in device_creds:
                missing.append(cred)
        
        return {"missing_credentials": missing, "required": required_creds.get(device_type, [])}
    
    def _prompt_for_credentials(self, missing_creds: list, device_type: str, device_ip: str) -> str:
        """Prompt user for missing credentials"""
        
        response = f"🔑 **Credentials Required** for {device_type} at `{device_ip}`\n\n"
        
        if device_type == "washing_machine":
            response += "To control your Samsung SmartThings washing machine, I need:\n\n"
            
            if "access_token" in missing_creds:
                response += "🔸 **SmartThings Personal Access Token (PAT)**\n"
                response += "   • Go to: https://account.smartthings.com/tokens\n"
                response += "   • Create token with device control permissions\n\n"
            
            if "device_id" in missing_creds:
                response += "🔸 **Device ID**\n"
                response += "   • Find in SmartThings app → Device → Settings\n"
                response += "   • Or use SmartThings CLI: `smartthings devices`\n\n"
            
            response += "💡 **To provide credentials**, update the config file:\n"
            response += "```json\n"
            response += "{\n"
            response += '  "credentials": {\n'
            response += f'    "{device_type}_{device_ip}": {{\n'
            response += '      "access_token": "your-pat-token-here",\n'
            response += '      "device_id": "your-device-id-here"\n'
            response += "    }\n"
            response += "  }\n"
            response += "}\n"
            response += "```\n\n"
            response += f"📁 Save to: `config/credentials.json`"
        
        return response
    
    def _general_help(self) -> str:
        """General help message"""
        
        return """
🤖 **AI-IoT Hub Help**

I can help you discover and control IoT devices on your network!

**🔍 Device Discovery:**
• "Discover devices" or "Scan network"
• "Find washing machines" 

**🎮 Device Control:**
• "Start washing machine at 192.168.0.5"
• "Stop washing machine at 192.168.0.5" 
• "Turn on thermostat at 192.168.1.20"

**📊 Status Checking:**
• "Check status of washing machine at 192.168.0.5"
• "Status of sensor at 192.168.1.50"

**🏗️ How I Work:**
1. **Document Analysis**: I read device API docs from `devices/raw_docs/`
2. **Code Generation**: Create Python communication tools automatically  
3. **Credential Management**: Prompt for and store API tokens securely
4. **Protocol Support**: REST APIs, TCP sockets, MQTT, Modbus, WebSockets

**📁 File Structure:**
• `devices/raw_docs/` - Drop API documentation here
• `devices/generated_specs/` - My parsed device specifications  
• `tools/generated/` - Auto-generated communication code
• `config/credentials.json` - Secure credential storage

**💡 Tips:**
• Add device documentation to get started
• I support Samsung SmartThings, Nest, Modbus, and more
• Each device gets its own cached communication tool
"""

def safe_print(text):
    """Print text with fallback for Unicode issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace problematic Unicode characters with ASCII equivalents
        import re
        # Replace common emojis with ASCII equivalents
        replacements = {
            '🚀': '[ROCKET]',
            '🧠': '[BRAIN]',
            '🔍': '[SEARCH]',
            '🤖': '[AI]', 
            '✅': '[OK]',
            '🔸': '*',
            '🔧': '[TOOL]',
            '💡': '[IDEA]',
            '📝': '[NOTE]',
            '📄': '[DOC]',
            '👋': '[WAVE]',
            '❌': '[ERROR]',
            '⚡': '[POWER]',
            '🎮': '[CONTROL]',
            '🔹': '-',
            '🔗': '[LINK]',
            '📡': '[SIGNAL]',
            '📊': '[CHART]',
            '🏠': '[HOME]',
            '📱': '[PHONE]'
        }
        
        safe_text = text
        for emoji, replacement in replacements.items():
            safe_text = safe_text.replace(emoji, replacement)
        
        # Remove any remaining problematic Unicode
        safe_text = safe_text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)

def main():
    """Interactive AI-IoT Hub interface"""
    import sys
    import os
    
    hub = SimpleAIIoTHub()
    
    safe_print("🚀 AI-IoT Hub Controller (Basic Interface)")
    safe_print("=" * 50)
    safe_print("I'm an AI agent that can discover and control IoT devices on your network.")
    safe_print("I use LLMs to understand device documentation and generate communication code.")
    safe_print("")
    safe_print("💡 For a richer experience with colors and formatting:")
    safe_print("   pip install -e \".[ui]\" && python textual_hub.py")
    safe_print("")
    safe_print("💡 Try commands like:")
    safe_print("  • 'Discover devices on my network'")
    safe_print("  • 'Start washing machine at 192.168.0.5'")  
    safe_print("  • 'Check status of thermostat'")
    safe_print("")
    
    # Check if input is from a TTY (interactive terminal)
    is_interactive = sys.stdin.isatty()
    
    if is_interactive:
        safe_print("Type 'help' for more info, or 'quit' to exit.")
        safe_print("")
    else:
        safe_print("📝 Processing piped input...\n")
    
    while True:
        try:
            # Handle both interactive and piped input
            if is_interactive:
                user_input = input("You: ").strip()
            else:
                # For piped input, read line by line until EOF
                user_input = sys.stdin.readline()
                if not user_input:  # EOF reached
                    safe_print("📄 End of input reached.")
                    break
                user_input = user_input.strip()
                safe_print(f"You: {user_input}")  # Echo the input for clarity
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                safe_print("\n👋 Goodbye! Your IoT devices are in good hands.")
                break
            
            if not user_input:
                if not is_interactive:  # Empty line in piped input
                    continue
                continue
            
            # Process the request
            response = hub.process_user_request(user_input)
            safe_print(f"\n🤖 AI-IoT Hub:\n{response}\n")
            
            # For non-interactive mode, process one command and exit
            if not is_interactive:
                break
            
        except KeyboardInterrupt:
            safe_print("\n👋 Goodbye!")
            break
        except EOFError:
            safe_print("\n📄 End of input reached.")
            break
        except Exception as e:
            safe_print(f"\n❌ Error: {e}")
            if not is_interactive:
                break
            safe_print("")  # Add spacing for interactive mode

if __name__ == "__main__":
    main()