# AI-IoT Hub Copilot Instructions

## Project Overview
An intelligent IoT hub using smolagents' `CodeAgent` to dynamically discover, analyze, and communicate with network devices. The system generates Python code on-demand by parsing raw documentation, creating cached communication tools for seamless device interaction.

## Architecture & Core Components

### Agent-Driven Communication Flow
1. **Raw Documentation Ingestion** (`devices/raw_docs/`) - Drop zone for any format device docs
2. **Spec Generation** (`src/agents/spec_analyzer.py`) - LLM parses docs → structured JSON specs  
3. **Dynamic Code Generation** (`src/agents/code_writing_agent.py`) - smolagents CodeAgent creates device communication code
4. **Code Caching** (`tools/generated/`) - Generated Python modules cached by device type + IP
5. **Runtime Execution** - Import and execute generated code for device communication

### Key Directory Structure
```
├── src/agents/           # Core LLM agents (CodeAgent-based)
├── devices/
│   ├── raw_docs/         # Drop zone: PDFs, URLs (.txt), Word docs, etc.
│   │   ├── thermostats/  # Device category folders
│   │   └── sensors/
│   ├── generated_specs/  # AI-parsed structured specs (JSON)
│   └── discovered_devices.json  # Network scan results with IPs
├── tools/generated/      # Cached Python communication modules
└── config/              # Hub and agent configurations
```

## Development Workflows

### Adding New Device Documentation
1. Drop ANY format documentation in `devices/raw_docs/{category}/`
   - PDFs: `honeywell_manual.pdf`
   - URLs: `nest_api_docs.txt` (containing single URL)
   - Word docs: `modbus_sensor_spec.docx`
2. Agent auto-parses → structured spec in `devices/generated_specs/`
3. On user request, CodeAgent generates communication code → `tools/generated/`

### smolagents CodeAgent Integration
The `CodeAgent` generates Python code that can:
```python
# TCP socket communication
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((device_ip, 502))  # Modbus TCP

# HTTP REST API calls  
import requests
response = requests.post(f"http://{device_ip}/api/v1/temperature", 
                        headers={"Authorization": f"Bearer {token}"})

# Async operations
import asyncio
async def read_sensor_data(ip, port):
    reader, writer = await asyncio.open_connection(ip, port)
    # Custom protocol communication
```

## Project Conventions

### File Naming Patterns
- **Raw docs**: Any name in category folder (e.g., `honeywell_t6_manual.pdf`)
- **URL files**: `{service}_api_link.txt` containing single URL
- **Generated specs**: `{manufacturer}_{device_type}_spec.json`
- **Generated tools**: `{device_type}_{ip_underscored}.py` (e.g., `thermostat_192_168_1_100.py`)

### Code Generation & Caching Strategy
- **Cache Key**: Device type + IP address combination
- **Cache Location**: `tools/generated/{device_type}_{ip_underscored}.py`
- **Invalidation**: Regenerate when device specs change or `--refresh` flag used
- **Import Pattern**: `from tools.generated.thermostat_192_168_1_100 import DeviceCommunicator`

### Communication Protocols Supported
- **TCP Sockets**: Raw TCP, Modbus TCP, custom protocols
- **HTTP/REST**: RESTful APIs with authentication
- **UDP**: Broadcast discovery, simple request/response
- **MQTT**: Publish/subscribe messaging (via `paho-mqtt`)
- **WebSocket**: Real-time bidirectional communication

## smolagents Integration Patterns

### CodeAgent Setup
```python
from smolagents import CodeAgent, InferenceClientModel
from src.agents.device_tools import NetworkScanTool, DocParserTool

model = InferenceClientModel()
agent = CodeAgent(
    tools=[NetworkScanTool(), DocParserTool()], 
    model=model,
    additional_authorized_imports=['socket', 'requests', 'asyncio', 'paho.mqtt.client']
)
```

### Dynamic Tool Generation
```python
# Agent generates code like this:
def create_device_communicator(device_ip, spec_data):
    if spec_data['protocol'] == 'modbus_tcp':
        # Generate Modbus TCP client
        code = f"""
import socket
class DeviceCommunicator:
    def __init__(self):
        self.ip = '{device_ip}'
        self.port = 502
        
    def read_temperature(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        # Modbus read holding registers
        """
    elif spec_data['protocol'] == 'rest_api':
        # Generate REST API client
        pass
```

### Error Handling & Fallbacks
- **Network timeouts**: Retry logic with exponential backoff
- **Authentication failures**: Token refresh mechanisms  
- **Code generation errors**: Fallback to spec regeneration
- **Device unavailable**: Graceful degradation with cached responses

## External Dependencies

### Core Libraries
- **smolagents**: `CodeAgent` for dynamic code generation
- **PyPDF2/pdfplumber**: PDF document parsing
- **python-docx**: Word document processing
- **requests**: HTTP API communication
- **python-nmap**: Network device discovery
- **paho-mqtt**: MQTT messaging

### Device Protocol Libraries
- **pymodbus**: Modbus TCP/RTU communication
- **bleak**: Bluetooth Low Energy devices
- **pyserial**: Serial device communication
- **websockets**: WebSocket client/server

## Debugging & Monitoring

### Logging Structure
```python
# Agent operation logs
[SPEC_GEN] Parsing PDF: honeywell_t6_manual.pdf -> 45 API endpoints found
[CODE_GEN] Generating tool for thermostat_192_168_1_100 -> 234 lines Python code
[CACHE_HIT] Using cached tool: sensor_192_168_1_101.py (generated 2h ago)
[DEVICE_COMM] TCP connection to 192.168.1.100:502 -> SUCCESS (87ms)
[ERROR] Authentication failed for device 192.168.1.105 -> retrying with backup credentials
```

### Key Monitoring Metrics  
- **Code Generation**: Success rate, generation time, cache hit ratio
- **Device Communication**: Connection success, response times, error rates
- **Network Discovery**: Devices found, spec parsing accuracy
- **Resource Usage**: Memory for cached tools, disk space for generated code

## Critical Implementation Notes

### Security Considerations
- **Sandboxed Execution**: Use smolagents' E2B/Docker executors for untrusted code
- **Input Validation**: Sanitize device IPs and parsed spec data
- **Authentication**: Secure credential storage for device access
- **Code Review**: Log all generated code for audit trails

### Performance Optimizations
- **Lazy Loading**: Import generated tools only when needed
- **Concurrent Discovery**: Parallel network scanning and spec parsing
- **Smart Caching**: Version-aware cache with dependency tracking
- **Batch Operations**: Group similar device communications

## LLM Integration & Usage

### Interactive AI Controller
```bash
# Start the AI-IoT Hub interactive mode
python interactive_hub.py

# Example conversations:
You: "Discover devices on my network"
AI-IoT Hub: *Scans network, finds washing machine at 192.168.0.5*

You: "Start washing machine at 192.168.0.5"  
AI-IoT Hub: *Generates communication code, prompts for SmartThings credentials*

You: "Check status of washing machine at 192.168.0.5"
AI-IoT Hub: *Uses cached tool to query device status via REST API*
```

### LLM Agent Architecture
```python
# The LLM Agent understands:
- File structure and role of each directory
- Protocol detection from documentation 
- Credential requirements by device type
- When to generate vs reuse cached tools
- How to execute device commands safely

# Agent tools:
- DeviceDiscoveryTool: Network scanning and device detection
- DeviceControlTool: Code generation and command execution  
- CredentialManagerTool: Secure credential storage and prompting
```

### Request Processing Flow
1. **User Input**: Natural language device request
2. **Intent Analysis**: LLM determines action (discover/control/status)
3. **Tool Selection**: Routes to appropriate agent tool
4. **Code Generation**: Creates communication code if needed
5. **Credential Check**: Prompts for missing authentication
6. **Command Execution**: Imports and runs generated tool
7. **Response**: Returns formatted results to user

### Credential Management
```json
// config/credentials.json - Auto-generated secure storage
{
  "credentials": {
    "washing_machine_192.168.0.5": {
      "access_token": "smartthings-pat-token",
      "device_id": "device-uuid"
    }
  },
  "devices": {
    "192.168.0.5": {"type": "washing_machine", "manufacturer": "Samsung"}
  }
}
```

## Getting Started

1. **Basic Setup**: `git clone` and `cd ai-iot`
2. **Add Documentation**: Drop device API docs in `devices/raw_docs/{category}/`
3. **Start AI Hub**: `python interactive_hub.py`
4. **Natural Language Control**: 
   - "Discover devices on my network"
   - "Start washing machine at 192.168.0.5"
   - "Check thermostat status"
5. **Provide Credentials**: Follow AI prompts for API tokens/device IDs

### With Full smolagents Integration
1. **Install Dependencies**: `pip install smolagents PyPDF2 python-docx requests`
2. **Configure Model**: Set LLM credentials in `config/hub_config.yaml`
3. **Run Full Version**: `python src/hub/ai_controller.py`

---
*The AI agent learns your device ecosystem and generates communication tools automatically. It understands file structure, protocols, and security requirements without manual configuration.*