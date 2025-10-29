# 🔧 AI-IoT Hub Configuration Guide

## Overview

The AI-IoT Hub uses `config/hub_config.yaml` as the main configuration file. This guide explains all available settings and their purposes.

## Complete Configuration Reference

### Basic Configuration Structure

```yaml
# Hub Configuration
network:
  scan_range: "192.168.1.0/24"
  timeout: 5
  max_concurrent_scans: 10

# LLM Model Settings
model:
  provider: "huggingface"  # or "openai", "anthropic"
  model_id: "meta-llama/Meta-Llama-3.1-8B-Instruct"
  api_key: "your_huggingface_token_here"  # Optional: HF token for premium models
  temperature: 0.1
  max_tokens: 2048

# Code Generation Settings  
code_generation:
  cache_ttl: 3600  # seconds (1 hour)
  max_cache_size: 100  # number of cached tools
  force_refresh: false
  
  # Security settings for smolagents
  executor_type: "docker"  # "local", "e2b", "docker", "wasm"
  additional_imports:
    - "socket"
    - "requests" 
    - "asyncio"
    - "json"
    - "time"
    - "paho.mqtt.client"
    - "pymodbus.client"
    - "websockets"

# Device Discovery Settings
discovery:
  enabled_protocols:
    - "tcp"
    - "http" 
    - "mqtt"
    - "modbus_tcp"
  common_ports:
    - 80
    - 443
    - 502   # Modbus TCP
    - 1883  # MQTT
    - 8080
  scan_interval: 300  # seconds between automatic scans

# Logging Configuration
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file: "logs/ai-iot-hub.log"
  format: "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"

# Credentials (automatically populated by AI)
credentials:
  # This section is managed automatically by the CredentialManagerTool
  # Example entries:
  # smartthings_washing_machine_192.168.0.5:
  #   access_token: "your-pat-token"
  #   device_id: "device-uuid"

# Device Registry (automatically populated)
devices:
  # This section is updated by device discovery
  # Example entries:
  # "192.168.1.100":
  #   type: "smartthings_hub"
  #   manufacturer: "Samsung"
  #   last_seen: "2025-01-15T10:30:00Z"
```

## Configuration Sections Explained

### 🌐 Network Settings (`network`)

Controls device discovery and network scanning behavior.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `scan_range` | string | `"192.168.1.0/24"` | CIDR network range to scan for devices |
| `timeout` | integer | `5` | Seconds to wait for device responses |
| `max_concurrent_scans` | integer | `10` | Maximum parallel network scans |

**Example**:
```yaml
network:
  scan_range: "10.0.0.0/16"      # Scan entire 10.x.x.x network
  timeout: 10                     # Wait longer for slow devices
  max_concurrent_scans: 20        # Faster scanning
```

### 🧠 Model Settings (`model`)

Configures the AI language model for device communication and code generation.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | string | `"huggingface"` | AI provider: `huggingface`, `openai`, `anthropic` |
| `model_id` | string | `"meta-llama/Meta-Llama-3.1-8B-Instruct"` | Specific model to use |
| `api_key` | string | `null` | API key/token for the provider |
| `temperature` | float | `0.1` | Randomness in AI responses (0.0-1.0) |
| `max_tokens` | integer | `2048` | Maximum response length |

**Examples**:

**Hugging Face (Default)**:
```yaml
model:
  provider: "huggingface"
  model_id: "meta-llama/Meta-Llama-3.1-8B-Instruct"
  api_key: "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  temperature: 0.1
```

**OpenAI**:
```yaml
model:
  provider: "openai"
  model_id: "gpt-4"
  api_key: "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  temperature: 0.2
```

**Free Models (No API Key Required)**:
```yaml
model:
  provider: "huggingface"
  model_id: "microsoft/DialoGPT-medium"  # Free conversational model
  temperature: 0.1
```

### 🔧 Code Generation (`code_generation`)

Controls how the AI generates and caches device communication code.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cache_ttl` | integer | `3600` | Seconds to keep generated tools cached |
| `max_cache_size` | integer | `100` | Maximum number of tools to cache |
| `force_refresh` | boolean | `false` | Always regenerate tools (ignore cache) |
| `executor_type` | string | `"docker"` | Code execution environment |
| `additional_imports` | list | See above | Python modules allowed in generated code |

**Security Note**: The `executor_type` determines how generated code runs:
- `"local"`: Runs directly on your system (fast, less secure)
- `"docker"`: Runs in Docker container (secure, requires Docker)
- `"e2b"`: Runs in cloud sandbox (secure, requires E2B account)

### 🔍 Discovery Settings (`discovery`)

Configures device discovery protocols and scanning behavior.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled_protocols` | list | `["tcp", "http", "mqtt", "modbus_tcp"]` | Protocols to scan for |
| `common_ports` | list | `[80, 443, 502, 1883, 8080]` | Ports to check during scanning |
| `scan_interval` | integer | `300` | Seconds between automatic discovery scans |

### 📝 Logging (`logging`)

Controls logging output and verbosity.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `level` | string | `"INFO"` | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `file` | string | `"logs/ai-iot-hub.log"` | Log file path |
| `format` | string | See above | Log message format |

## Configuration Management

### Environment Variables

You can override config values using environment variables:

```bash
# Override API key
export HF_TOKEN="your_huggingface_token"

# Override model
export AI_IOT_MODEL_ID="microsoft/DialoGPT-medium"

# Override network range  
export AI_IOT_SCAN_RANGE="10.0.0.0/8"
```

### Configuration Precedence

The system loads configuration in this order (later overrides earlier):

1. **Default values** (hardcoded in `ai_controller.py`)
2. **`config/hub_config.yaml`** (your configuration file)
3. **Environment variables** (highest priority)

### Automatic Configuration Updates

The AI system automatically updates these sections:

- **`credentials`**: When you provide device credentials
- **`devices`**: When devices are discovered on your network
- **Cache timestamps**: When tools are generated or used

## Common Configuration Examples

### Home Network Setup
```yaml
network:
  scan_range: "192.168.1.0/24"
  timeout: 5

model:
  provider: "huggingface"
  model_id: "HuggingFaceH4/zephyr-7b-beta"  # Free model
  temperature: 0.1

discovery:
  enabled_protocols: ["tcp", "http", "mqtt"]
  scan_interval: 600  # Check for new devices every 10 minutes
```

### Industrial/Office Network
```yaml
network:
  scan_range: "10.0.0.0/16"
  timeout: 10
  max_concurrent_scans: 50

model:
  provider: "openai"
  model_id: "gpt-4"
  api_key: "your-openai-key"

discovery:
  enabled_protocols: ["modbus_tcp", "tcp", "http"]
  common_ports: [502, 503, 80, 443, 8080, 8443]
  
code_generation:
  executor_type: "docker"  # Secure code execution
```

### Development/Testing Setup
```yaml
model:
  provider: "huggingface" 
  model_id: "microsoft/DialoGPT-medium"
  temperature: 0.2

code_generation:
  cache_ttl: 60        # Short cache for testing
  force_refresh: true  # Always regenerate code
  executor_type: "local"  # Fast execution

logging:
  level: "DEBUG"       # Verbose logging
```

## Troubleshooting Configuration

### Common Issues

**1. API Key Not Working**
```bash
# Check your token works
curl -H "Authorization: Bearer YOUR_TOKEN" https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct
```

**2. Network Discovery Issues**
```yaml
# Try larger timeout and smaller scan range
network:
  scan_range: "192.168.1.100/30"  # Smaller range
  timeout: 15                      # Longer timeout
```

**3. Model Not Responding**
```yaml
# Try a known working free model
model:
  model_id: "microsoft/DialoGPT-medium"
  # Remove api_key line to use free tier
```

## Next Steps

1. **Copy the example** that matches your setup
2. **Save as** `config/hub_config.yaml` 
3. **Add your API key** if using premium models
4. **Test the configuration** with `python interactive_hub.py`
5. **Adjust settings** based on your network and performance needs

For more help, see:
- [Installation Guide](../INSTALL.md)
- [FAQ & Troubleshooting](../README.md#faq--troubleshooting)
- [Device Integration Examples](../README.md#device-integration-examples)