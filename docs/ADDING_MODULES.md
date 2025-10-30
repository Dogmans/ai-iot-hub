# Adding New Python Modules to AI-IoT Hub CodeAgent

## Overview
The AI-IoT Hub uses smolagents' CodeAgent to generate Python code dynamically. For security, only explicitly authorized modules can be imported in the generated code.

## Configuration Location
**Primary config file**: `config/hub_config.yaml`

Look for the `code_generation.additional_imports` section:

```yaml
code_generation:
  additional_imports:
    - "socket"
    - "requests" 
    - "pathlib"
    # Add new modules here
```

## Adding New Modules

### 1. Install the Module First
```bash
# Example: Adding MQTT support
pip install paho-mqtt

# Example: Adding serial communication  
pip install pyserial
```

### 2. Add to Config File
Edit `config/hub_config.yaml` and add the module to the `additional_imports` list:

```yaml
additional_imports:
  - "paho.mqtt.client"  # For MQTT communication
  - "serial"            # For serial devices
```

### 3. Restart the Application
The CodeAgent reads the configuration on initialization, so restart your application:

```bash
python src/hub/interactive_controller.py
```

## Common Module Categories

### IoT Protocols
```yaml
- "paho.mqtt.client"    # MQTT messaging
- "pymodbus.client"     # Modbus TCP/RTU  
- "websockets"          # WebSocket communication
- "serial"              # Serial/RS485 devices
- "bleak"               # Bluetooth Low Energy
```

### Network Discovery
```yaml
- "nmap"                # Network scanning (requires nmap binary)
- "scapy"               # Packet crafting
- "netifaces"           # Network interface info
- "psutil"              # System/network monitoring
```

### Data Processing
```yaml
- "numpy"               # Numerical computing
- "pandas"              # Data analysis
- "lxml"                # XML processing
```

## Testing Your Changes

Run the test script to verify your configuration:

```bash
python test_imports_config.py
```

## Troubleshooting

### "Non-installed authorized modules" Error
This means you listed a module that isn't installed. Either:
1. Install the module: `pip install module_name`
2. Remove it from the config file
3. Comment it out for later use

### Generated Code Import Errors
If generated code fails with import errors:
1. Check the module is in `additional_imports`
2. Verify the module name is correct (e.g., `serial` not `pyserial`)
3. Ensure the module is installed in the current environment

## Example: Adding MQTT Support

1. **Install**: `pip install paho-mqtt`
2. **Configure**: Add `"paho.mqtt.client"` to `additional_imports`
3. **Test**: Run `python test_imports_config.py`
4. **Use**: The CodeAgent can now generate code with `import paho.mqtt.client`

## Security Note
Only add modules you trust. The CodeAgent can execute any code using these modules, so avoid adding modules with system access unless necessary.