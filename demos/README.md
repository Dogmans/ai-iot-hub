# Demos Directory

This directory contains demonstration scripts that showcase different features and capabilities of the AI-IoT Hub.

## Demo Scripts

### Basic Functionality Demos
- `demo_simple.py` - Simple device discovery and control demo
- `demo_working_discovery.py` - Working comprehensive device discovery

### Advanced Feature Demos  
- `demo_smartthings.py` - Samsung SmartThings integration demo
- `demo_credentials.py` - Credential management demonstration
- `demo_error_handling.py` - Error handling and recovery demo

## Running Demos

From the project root:

```bash
# Basic device discovery demo
python demos/demo_simple.py

# SmartThings integration  
python demos/demo_smartthings.py

# Comprehensive discovery
python demos/demo_working_discovery.py

# Error handling showcase
python demos/demo_error_handling.py
```

## Demo Requirements

- Virtual environment activated
- All dependencies installed (`pip install -e .`)
- Network access for device discovery demos
- API credentials for specific service demos (SmartThings, etc.)

## Adding New Demos

1. Create demo file with `demo_` prefix
2. Include clear comments explaining each step
3. Add error handling for missing dependencies
4. Update this README with description
5. Test demo works from clean environment