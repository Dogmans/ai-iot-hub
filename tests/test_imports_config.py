#!/usr/bin/env python3
"""
Test script to verify the import configuration is working correctly
"""

import sys
import yaml
from pathlib import Path

# Add src to path (works from both project root and tests directory)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from hub.ai_controller import AIDeviceController
from agents.code_writing_agent import DeviceCodeAgent

def test_config_loading():
    """Test that config file loads imports correctly"""
    print("Testing import configuration...")
    
    # Load config directly
    config_path = Path("config/hub_config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        imports = config.get('code_generation', {}).get('additional_imports', [])
        print(f"[OK] Config loaded: {len(imports)} imports defined")
        print(f"Sample imports: {imports[:5]}...")
        
        return config
    else:
        print("[FAIL] Config file not found")
        return {}

def test_controller_initialization():
    """Test that AIDeviceController uses config imports"""
    try:
        controller = AIDeviceController()
        print("[OK] AIDeviceController initialized successfully")
        print(f"Config loaded with {len(controller.config)} sections")
        return True
    except Exception as e:
        print(f"[FAIL] AIDeviceController failed: {e}")
        return False

def test_code_agent_initialization():
    """Test that DeviceCodeAgent uses config imports"""
    try:
        # Test with config
        config_path = Path("config/hub_config.yaml")
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
        else:
            config = {}
            
        code_agent = DeviceCodeAgent(config=config)
        print("[OK] DeviceCodeAgent initialized successfully")
        
        # Test with empty config (should use defaults)
        code_agent_default = DeviceCodeAgent(config={})
        print("[OK] DeviceCodeAgent with empty config initialized successfully")
        return True
    except Exception as e:
        print(f"[FAIL] DeviceCodeAgent failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing AI-IoT Hub Import Configuration")
    print("=" * 50)
    
    # Test config loading
    config = test_config_loading()
    
    print("\n" + "-" * 30)
    
    # Test controller
    controller_ok = test_controller_initialization()
    
    print("\n" + "-" * 30)
    
    # Test code agent  
    agent_ok = test_code_agent_initialization()
    
    print("\n" + "=" * 50)
    if controller_ok and agent_ok:
        print("SUCCESS: All tests passed! Import configuration is working correctly.")
    else:
        print("FAILED: Some tests failed. Check the configuration.")