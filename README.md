# AI-IoT Hub

An intelligent IoT hub using smolagents' `CodeAgent` to dynamically discover, analyze, and communicate with network devices. The system generates Python code on-demand by parsing raw documentation, creating cached communication tools for seamless device interaction.

## Features

- 🧠 **LLM-Powered Device Control** - Natural language interface for IoT devices
- 🔧 **Dynamic Code Generation** - Automatically creates communication modules from documentation
- 📄 **Multi-Format Documentation Support** - PDFs, URLs, Word docs, any format
- 🔑 **Secure Credential Management** - User-friendly prompting with secure storage
- 🌐 **Protocol Agnostic** - REST APIs, TCP, MQTT, Modbus, WebSockets, Bluetooth
- ⚡ **Smart Caching** - Generated tools are reused for performance
- 🔍 **Network Discovery** - Automatic device detection and identification

## Quick Start

### Installation

1. **Clone and setup environment**:
```bash
git clone https://github.com/ai-iot/ai-iot-hub.git
cd ai-iot-hub
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
```

2. **Install dependencies**:
```bash
pip install -e .
```

3. **For development**:
```bash
pip install -e ".[dev]"
```

### Basic Usage

1. **Add device documentation** to `devices/raw_docs/{category}/`:
   - Drop PDFs: `honeywell_manual.pdf`
   - URLs: `smartthings_api.txt` (containing API URL)
   - Word docs: `modbus_spec.docx`

2. **Start the interactive hub**:
```bash
ai-iot-interactive
```

3. **Control devices with natural language**:
```
You: "Discover devices on my network"
AI-IoT Hub: *Scans network, finds washing machine at 192.168.0.5*

You: "Start washing machine at 192.168.0.5"
AI-IoT Hub: *Prompts for SmartThings credentials, generates code, executes command*
```

### Programmatic Usage

```python
from src.hub.ai_controller import AIIoTHubController

async def main():
    hub = AIIoTHubController()
    
    # Natural language device control
    response = await hub.process_user_request("Turn on lights in living room")
    print(response)
    
    # Use generated tools directly
    from tools.generated.smart_bulb_192_168_1_100 import DeviceCommunicator
    
    bulb = DeviceCommunicator()
    if bulb.connect():
        bulb.set_brightness(80)
        bulb.set_color("warm_white")
```

## Architecture

### Core Components

- **Agent-Driven Flow**: LLM parses docs → generates code → executes commands
- **Dynamic Code Generation**: smolagents CodeAgent creates device communication modules
- **Smart Caching**: Generated Python modules cached by device type + IP
- **Secure Credentials**: Device-specific authentication with user prompting

### Directory Structure

```
ai-iot-hub/
├── src/
│   ├── hub/ai_controller.py           # Main LLM controller
│   └── agents/
│       ├── spec_analyzer.py           # Document → structured specs
│       ├── device_tools.py            # smolagents Tools
│       └── code_writing_agent.py      # Dynamic code generation
├── devices/
│   ├── raw_docs/                      # Drop zone for device docs
│   │   ├── thermostats/
│   │   └── sensors/
│   ├── generated_specs/               # AI-parsed structured specs
│   └── discovered_devices.json       # Network scan results
├── tools/generated/                   # Cached communication modules
├── config/                           # Hub and credential configuration
└── interactive_hub.py                # Simple CLI interface
```

### Supported Protocols

- **HTTP/REST APIs** - SmartThings, Nest, Philips Hue
- **TCP Sockets** - Raw TCP, Modbus TCP, custom protocols
- **MQTT** - Home Assistant, IoT sensors
- **WebSockets** - Real-time device communication
- **Bluetooth Low Energy** - BLE sensors and devices
- **Serial** - USB/RS485 connected devices

## Device Integration Examples

### SmartThings Devices
```python
# Place API URL in devices/raw_docs/thermostats/smartthings_api.txt
# AI generates complete REST API client with authentication
```

### Modbus TCP Devices
```python
# Drop Modbus manual PDF in devices/raw_docs/sensors/
# AI creates socket-based communication with register mapping
```

### MQTT Sensors
```python
# Provide MQTT broker documentation
# AI generates pub/sub client with topic structure
```

## Development

### Running Tests
```bash
pytest
pytest --cov=src tests/  # With coverage
```

### Code Formatting
```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
```

### Type Checking
```bash
mypy src/
```

## Configuration

### Hub Configuration (`config/hub_config.yaml`)
```yaml
model:
  model_id: "meta-llama/Meta-Llama-3.1-8B-Instruct"
  temperature: 0.1

network:
  scan_range: "192.168.1.0/24"
  timeout: 5

cache_ttl: 3600
```

### Credentials (`config/credentials.json`)
```json
{
  "credentials": {
    "smartthings_washing_machine_192.168.0.5": {
      "access_token": "your-pat-token",
      "device_id": "device-uuid"
    }
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Install development dependencies: `pip install -e ".[dev]"`
4. Make your changes and add tests
5. Run the test suite: `pytest`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **smolagents** - For the powerful CodeAgent framework
- **Hugging Face** - For the transformer models and inference API
- **IoT Community** - For device documentation and protocol specifications