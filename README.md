# AI-IoT Hub

An intelligent IoT hub using smolagents' `CodeAgent` to dynamically discover, analyze, and communicate with network devices. The system generates Python code on-demand by parsing raw documentation, creating cached communication tools for seamless device interaction.

## Features

- 🧠 **LLM-Powered Device Control** - Natural language interface for IoT devices
- 🔧 **Dynamic Code Generation** - Automatically creates communication modules from documentation
- 📄 **Multi-Format Documentation Support** - PDFs, URLs, Word docs, any format
- 🔑 **Secure Credential Management** - User-friendly prompting with secure storage
- 🌐 **Protocol Agnostic** - REST APIs, TCP, MQTT, Modbus, WebSockets
- ⚡ **Smart Caching** - Generated tools are reused for performance
- 🔍 **Network Discovery** - Automatic device detection and identification
- 🚀 **Easy Installation** - No C++ compiler requirements, clean dependencies

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
# Complete installation (recommended)
pip install -r requirements.txt
```

**Alternative minimal installation**:
```bash
# Basic functionality only
pip install -e .

# Add specific features as needed
pip install -e ".[ui]"      # Rich terminal interface
pip install -e ".[network]" # Network discovery tools
pip install -e ".[ai]"      # Full AI capabilities
```

### User Interfaces

#### 🎨 **Rich Textual Interface (Recommended)**
```bash
# Launch rich terminal interface (included in main requirements.txt)
python examples/textual_hub.py
```

**Features:**
- 🎨 **Rich formatting** with colors, emojis, and visual hierarchy
- 📱 **Interactive terminal UI** with input field and scrolling chat
- ⌨️ **Keyboard shortcuts** (Ctrl+C quit, Ctrl+L clear, Enter send)
- 📊 **Structured responses** with proper visual formatting
- 🎯 **Enhanced readability** for device status and control
- 🔧 **Smart formatting** - CodeAgent reads `config/textual_markup_guide.md` for response styling

#### 💬 **Basic Terminal Interface**
```bash
# No extra dependencies needed
python interactive_hub.py
```

**Features:**
- 💬 **Simple text-based** conversation
- 🚀 **Lightweight** - works anywhere
- 🔧 **Fallback option** when Textual unavailable

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
from src.hub.ai_controller import AIDeviceController

async def main():
    hub = AIDeviceController()
    
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

## How It Works

### Complete Workflow

AI-IoT Hub uses a sophisticated AI-driven workflow that combines intelligent device discovery, automatic documentation processing, and dynamic code generation:

#### 1. **Device Discovery** 🔍
```
You: "Discover devices on my network"
↓
AI Hub: Uses multi-method discovery (mDNS, zeroconf, HTTP fingerprinting)
↓ 
Result: "Found Samsung SmartThings Hub at 192.168.1.100 (confidence: 90%)"
```

#### 2. **Intelligent Documentation Search** 📚
```
AI Hub: "I need SmartThings API docs to generate communication code"
↓
AI searches web intelligently: "Samsung SmartThings API documentation site:developer.samsung.com"
↓
Downloads: SmartThings API docs → saves to devices/raw_docs/samsung_smartthings/
```

#### 3. **Dynamic Code Generation** ⚡
```
AI Hub: "Now I'll generate Python code to communicate with this device"
↓
CodeAgent reads documentation files directly (PDFs, URLs, JSON)
↓
Generates: tools/generated/smartthings_192_168_1_100.py (complete communication class)
```

#### 4. **Device Control** 🎯
```
You: "Turn on washing machine at 192.168.1.100"
↓
AI Hub: Imports and executes generated communication code
↓
Prompts for credentials if needed → Sends command → Returns result
```

### Key Innovations

- **🧠 LLM-Native Processing**: No hardcoded parsers - AI understands any document format
- **🔍 Multi-Method Discovery**: Combines nmap, mDNS, UPnP, HTTP fingerprinting with confidence scoring  
- **📝 Intelligent Search**: AI constructs context-aware queries for manufacturer documentation
- **⚡ Direct File Access**: CodeAgent reads files directly without intermediate parsing tools
- **🔄 Smart Caching**: Generated code is reused, documentation is cached locally

### Architecture

#### Core Components

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
│       ├── device_tools.py            # smolagents Tools for discovery/control
│       └── code_writing_agent.py      # Dynamic code generation (processes docs directly)
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

## Detailed Example Walkthrough

### Real-World Scenario: SmartThings Washing Machine

#### Step 1: Discovery
```bash
$ python interactive_hub.py
You: "Discover devices on my network"

AI-IoT Hub: 🔍 Scanning network with comprehensive discovery...
           📡 Found Samsung SmartThings Hub at 192.168.1.100
           🏠 Detected washing machine device (confidence: 95%)
           ✅ SmartThings API protocol identified
```

#### Step 2: Documentation Processing
```
AI-IoT Hub: 🧠 I need SmartThings documentation to generate communication code
           🌐 Searching: "Samsung SmartThings API documentation site:developer.samsung.com"  
           📥 Downloaded: SmartThings REST API specification
           📄 Processed: OAuth2 authentication requirements identified
```

#### Step 3: Code Generation
```python
# AI generates tools/generated/smartthings_192_168_1_100.py:

class SmartThingsDevice:
    def __init__(self, ip: str, access_token: str):
        self.base_url = f"https://{ip}:8080"
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    def get_devices(self):
        # Auto-generated from API documentation
        return requests.get(f"{self.base_url}/devices", headers=self.headers).json()
    
    def send_command(self, device_id: str, command: str, value: str):
        # Extracted from SmartThings API examples
        payload = {"commands": [{"command": command, "value": value}]}
        return requests.post(f"{self.base_url}/devices/{device_id}/commands", 
                           json=payload, headers=self.headers)
```

#### Step 4: Interactive Control
```bash
You: "Start washing machine at 192.168.1.100"

AI-IoT Hub: 🔑 I need your SmartThings credentials to control this device
           📝 Please provide your Personal Access Token: [secure input]
           💾 Credentials saved securely for future use
           
           ⚡ Executing command...
           ✅ Washing machine started successfully!
           📊 Status: Running delicate cycle, 45 minutes remaining
```

### File System After Processing
```
devices/
├── raw_docs/samsung_smartthings/
│   ├── smartthings_api_docs.json      # Auto-downloaded API spec
│   └── developer_guide_url.txt        # Documentation URL reference
├── discovered_devices.json            # Network scan results
└── generated_specs/                   # AI-processed specifications

tools/generated/
└── smartthings_192_168_1_100.py      # Generated communication module

config/
└── credentials.json                   # Secure credential storage
```

## Device Integration Examples

### Any Device Type - AI Figures It Out!

The beauty of AI-IoT Hub is that you don't need device-specific integration code. The AI handles everything:

#### SmartThings Ecosystem
- **Discovery**: mDNS detection + HTTP fingerprinting
- **Documentation**: Auto-downloads from developer.samsung.com
- **Authentication**: OAuth2 + Personal Access Token prompting
- **Communication**: REST API with WebSocket events

#### Philips Hue
- **Discovery**: Hue Bridge mDNS service detection  
- **Documentation**: Auto-fetches from developers.meethue.com
- **Authentication**: API key generation workflow
- **Communication**: REST API with color/brightness control

#### Modbus Industrial Devices
- **Discovery**: Port 502 detection + manufacturer identification
- **Documentation**: PDF manual processing + register extraction
- **Authentication**: Usually none required
- **Communication**: TCP socket with register read/write

#### MQTT IoT Sensors  
- **Discovery**: Network scanning + protocol detection
- **Documentation**: Broker specification processing
- **Authentication**: Username/password or certificate-based
- **Communication**: Pub/sub with topic autodiscovery

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

## Installation Options

### Basic Installation (Ping-based discovery)
```bash
pip install -e .
```
**Capabilities**: Basic device discovery, document processing, code generation

### Full Network Discovery (Recommended)
```bash
pip install -e ".[network]"
```
**Capabilities**: Advanced device discovery (mDNS, zeroconf, MAC lookup, HTTP fingerprinting)

### Complete Development Setup
```bash
pip install -e ".[network,ai,dev]"
```
**Capabilities**: Full functionality + smolagents CodeAgent + development tools

### Optional: Enhanced Discovery (requires system dependencies)
```bash
# For 100% discovery capability, install nmap system binary:
# Windows: Download from https://nmap.org/download.html
# macOS: brew install nmap
# Linux: apt-get install nmap
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

## FAQ & Troubleshooting

### Q: "No devices found during discovery"
**A**: 
1. Check network range in config: `network.scan_range: "192.168.1.0/24"`
2. Install network dependencies: `pip install -e ".[network]"`  
3. For full capability, install nmap system binary

### Q: "AI can't find documentation for my device"
**A**: 
1. Drop any PDF/manual in `devices/raw_docs/{category}/`
2. Add URL file: `echo "https://device-api-docs.com" > devices/raw_docs/sensors/my_device_api.txt`
3. AI will search intelligently and adapt to any documentation format

### Q: "Generated code doesn't work with my device"
**A**:
1. AI learns from errors - run again and it will adapt the generated code
2. Provide more specific documentation in `raw_docs/`
3. Check credentials are correct for your device type

### Q: "How do I add a completely new device type?"
**A**: 
Just use it! The AI automatically:
1. Discovers the device type and manufacturer  
2. Searches for appropriate documentation online
3. Downloads and processes the documentation
4. Generates communication code tailored to that device
5. Prompts for any required credentials

### Q: "Can I use my own LLM model?"
**A**: Yes! Configure in `config/hub_config.yaml`:
```yaml
model:
  model_id: "your-model-id" 
  # Works with any Hugging Face model or OpenAI API
```

## Project Structure

```
├── src/
│   ├── agents/           # Core LLM agents (CodeAgent-based)
│   ├── hub/             # Main AI controller and interfaces  
│   └── discovery/       # Network discovery engines
├── config/              # Configuration files
│   └── hub_config.yaml  # Main configuration (imports, model settings)
├── devices/
│   ├── raw_docs/        # Device documentation (PDFs, URLs, etc.)
│   └── generated_specs/ # AI-parsed device specifications
├── tools/generated/     # Generated device communication modules
├── demos/               # Demonstration scripts
│   ├── demo_simple.py           # Basic functionality demo
│   ├── demo_smartthings.py      # SmartThings integration
│   └── demo_working_discovery.py # Device discovery showcase
├── tests/               # Test suite
│   ├── test_discovery.py        # Discovery tests
│   ├── test_imports_config.py   # Configuration tests
│   └── test_code_generation.py  # CodeAgent tests
├── examples/            # Reference implementations
│   ├── textual_hub.py           # Rich terminal UI
│   └── real_device_discovery.py # Discovery examples
└── docs/                # Documentation and guides
```

### Key Directories

- **`src/`** - Core application code and agents
- **`config/`** - Configuration files (edit `hub_config.yaml` for imports)
- **`devices/raw_docs/`** - Drop device documentation here
- **`tools/generated/`** - Auto-generated device communication code
- **`demos/`** - Runnable examples (`python demos/demo_simple.py`)
- **`tests/`** - Test suite (`python tests/test_discovery.py`)  
- **`examples/`** - Reference implementations and UI examples

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