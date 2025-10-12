"""AI-IoT Hub - Intelligent IoT device communication with LLM-powered code generation"""

__version__ = "0.1.0"
__author__ = "AI-IoT Hub Team"
__email__ = "contact@ai-iot-hub.dev"
__description__ = "An intelligent IoT hub using smolagents for dynamic device discovery and communication"

# Core imports for easy access
from .hub.ai_controller import AIIoTHubController
from .agents.device_tools import DeviceDiscoveryTool, DeviceControlTool, CredentialManagerTool

__all__ = [
    "AIIoTHubController",
    "DeviceDiscoveryTool", 
    "DeviceControlTool",
    "CredentialManagerTool"
]