"""
AI-IoT Hub Main Entry Point

Orchestrates device discovery, documentation parsing, and dynamic code generation
using smolagents CodeAgent for on-demand device communication.
"""

import asyncio
import logging
from pathlib import Path
from smolagents import CodeAgent, InferenceClientModel


from agents.code_writing_agent import DeviceCodeAgent
from agents.device_discovery import NetworkDiscovery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIIoTHub:
    def __init__(self, config_path="config/hub_config.yaml"):
        self.config = self._load_config(config_path)
        self.model = InferenceClientModel()
        self.code_agent = DeviceCodeAgent(model=self.model)
        self.discovery = NetworkDiscovery()
        
    def _load_config(self, config_path):
        """Load hub configuration"""
        # TODO: Implement YAML config loading
        return {
            "network_range": "192.168.1.0/24",
            "cache_ttl": 3600,
            "max_concurrent_scans": 10
        }
    
    async def discover_devices(self):
        """Discover devices on network and update registry"""
        logger.info("[DISCOVERY] Starting network device discovery...")
        devices = await self.discovery.scan_network(self.config["network_range"])
        logger.info(f"[DISCOVERY] Found {len(devices)} devices")
        return devices
    
    async def process_documentation(self, doc_path):
        """CodeAgent processes documentation directly during code generation - no separate parsing needed"""
        logger.info(f"[DOC_READY] Documentation available at: {doc_path}")
        return {"message": "CodeAgent will process documentation directly when generating device tools"}
    
    async def generate_device_tool(self, device_ip, device_type, force_refresh=False):
        """Generate communication tool for specific device"""
        cache_key = f"{device_type}_{device_ip.replace('.', '_')}"
        cache_path = Path(f"tools/generated/{cache_key}.py")
        
        if cache_path.exists() and not force_refresh:
            logger.info(f"[CACHE_HIT] Using cached tool: {cache_path}")
            return cache_path
            
        logger.info(f"[CODE_GEN] Generating new tool for {device_type} at {device_ip}")
        tool_code = await self.code_agent.generate_device_communicator(
            device_ip=device_ip,
            device_type=device_type
        )
        
        # Save generated code
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(tool_code)
        logger.info(f"[CODE_GEN] Tool cached at: {cache_path}")
        return cache_path
    
    async def communicate_with_device(self, device_ip, device_type, command, **kwargs):
        """Execute communication with device using generated tool"""
        tool_path = await self.generate_device_tool(device_ip, device_type)
        
        # Dynamic import and execution
        module_name = f"tools.generated.{tool_path.stem}"
        logger.info(f"[DEVICE_COMM] Executing {command} on {device_ip} via {module_name}")
        
        # TODO: Implement dynamic module loading and command execution
        result = await self._execute_device_command(module_name, command, **kwargs)
        return result
    
    async def _execute_device_command(self, module_name, command, **kwargs):
        """Safely execute generated device communication code"""
        # TODO: Implement safe code execution with smolagents
        pass

if __name__ == "__main__":
    hub = AIIoTHub()
    
    # Example usage
    asyncio.run(hub.discover_devices())