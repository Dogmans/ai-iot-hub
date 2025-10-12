# AI-IoT Hub Installation Guide

## Prerequisites

- Python 3.9 or higher
- Windows/Linux/macOS
- Internet connection for package installation

## Installation Methods

### 1. Development Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/ai-iot/ai-iot-hub.git
cd ai-iot-hub

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

# Install base package
pip install -e .
```

### 2. Install Optional Dependencies

Install additional features as needed:

```bash
# AI/LLM capabilities (smolagents)
pip install -e ".[ai]"

# Document processing (PDF, Word, etc.)
pip install -e ".[docs-processing]"

# Web and HTTP support
pip install -e ".[web]"

# IoT protocols (MQTT, Modbus, Serial)
pip install -e ".[iot]"

# Network discovery
pip install -e ".[network]"

# Bluetooth support
pip install -e ".[bluetooth]"

# All features
pip install -e ".[all]"

# Development tools
pip install -e ".[dev]"
```

### 3. Production Installation

```bash
pip install ai-iot-hub
```

## Quick Test

After installation, test the basic functionality:

```bash
# Test the interactive hub (works without external dependencies)
python interactive_hub.py

# Test with basic project structure
ai-iot-interactive
```

## Troubleshooting

### Network Issues During Installation

If you encounter network connectivity issues:

1. **Install minimal version first**:
```bash
pip install -e .  # Only installs basic dependencies
```

2. **Install dependencies individually**:
```bash
pip install requests pyyaml click colorama
pip install smolagents  # When network is stable
```

### Missing System Dependencies

Some features require system-level dependencies:

**Network Discovery (nmap)**:
- Windows: Install nmap from https://nmap.org/download.html
- Ubuntu/Debian: `sudo apt-get install nmap`
- macOS: `brew install nmap`

**Bluetooth**:
- Windows: Usually works out of the box
- Ubuntu/Debian: `sudo apt-get install bluez libbluetooth-dev`
- macOS: Should work natively

### Permission Issues

Some network operations may require elevated privileges:

```bash
# Windows (Run as Administrator)
# Linux/macOS (use sudo for network scanning)
sudo python your_script.py
```

## Configuration

### Initial Setup

1. **Create config directory**:
```bash
mkdir -p config
```

2. **Add device documentation**:
```bash
mkdir -p devices/raw_docs/thermostats
mkdir -p devices/raw_docs/sensors
```

3. **Test basic functionality**:
```python
from src.hub.ai_controller import AIIoTHubController

hub = AIIoTHubController()
print("AI-IoT Hub initialized successfully!")
```

## Next Steps

1. **Add device documentation** to `devices/raw_docs/{category}/`
2. **Configure your LLM** in `config/hub_config.yaml` 
3. **Start interactive mode**: `python interactive_hub.py`
4. **Begin device discovery**: Ask the AI to "discover devices on network"

For detailed usage examples, see the main [README.md](README.md).