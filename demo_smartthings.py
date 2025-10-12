#!/usr/bin/env python3
"""
Demo script to process Samsung SmartThings documentation and generate 
communication tools for a washing machine at 192.168.0.5
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from agents.spec_analyzer import SpecAnalyzer
from agents.code_writing_agent import DeviceCodeAgent

async def process_smartthings_washing_machine():
    """Process SmartThings API docs and generate washing machine communicator"""
    
    print("🚀 AI-IoT Hub Demo: Samsung SmartThings Washing Machine")
    print("=" * 60)
    
    # Initialize our agents
    spec_analyzer = SpecAnalyzer()
    code_agent = DeviceCodeAgent()
    
    # Step 1: Process the SmartThings API documentation
    doc_path = Path("devices/raw_docs/thermostats/samsung_smartthings_api.txt")
    print(f"\n📄 Step 1: Processing documentation from {doc_path}")
    
    try:
        spec = await spec_analyzer.parse_document(doc_path)
        print(f"✅ Generated spec with {len(spec.get('endpoints', []))} endpoints")
        print(f"   Protocol: {spec.get('protocol')}")
        print(f"   Device Type: {spec.get('device_type')}")
    except Exception as e:
        print(f"❌ Error processing documentation: {e}")
        return
    
    # Step 2: Generate communication code for washing machine
    device_ip = "192.168.0.5"
    device_type = "washing_machine"  # Override for our specific use case
    
    print(f"\n🔧 Step 2: Generating communication code for washing machine at {device_ip}")
    
    try:
        # Update spec for washing machine specifics
        washing_machine_spec = spec.copy()
        washing_machine_spec['device_type'] = device_type
        washing_machine_spec['endpoints'] = [
            {
                "name": "get_status",
                "method": "GET",
                "path": "/api/v1/devices/{device_id}/status",
                "description": "Get washing machine status (running, idle, complete)"
            },
            {
                "name": "start_cycle",
                "method": "POST", 
                "path": "/api/v1/devices/{device_id}/commands",
                "description": "Start a wash cycle",
                "parameters": {
                    "command": {"type": "string", "required": True, "value": "start"},
                    "cycle_type": {"type": "string", "required": False, "options": ["normal", "delicate", "heavy"]}
                }
            },
            {
                "name": "stop_cycle",
                "method": "POST",
                "path": "/api/v1/devices/{device_id}/commands", 
                "description": "Stop current wash cycle",
                "parameters": {
                    "command": {"type": "string", "required": True, "value": "stop"}
                }
            },
            {
                "name": "get_cycle_progress",
                "method": "GET",
                "path": "/api/v1/devices/{device_id}/progress",
                "description": "Get current cycle progress and time remaining"
            }
        ]
        
        # Save washing machine specific spec
        import json
        spec_path = Path("devices/generated_specs/samsung_washing_machine_spec.json")
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        with open(spec_path, 'w') as f:
            json.dump(washing_machine_spec, f, indent=2)
        
        print(f"✅ Saved washing machine spec to: {spec_path}")
        
        # Generate the communication code
        generated_code = await code_agent.generate_device_communicator(device_ip, device_type)
        
        # Save the generated code
        cache_key = f"{device_type}_{device_ip.replace('.', '_')}"
        code_path = Path(f"tools/generated/{cache_key}.py")
        code_path.parent.mkdir(parents=True, exist_ok=True)
        code_path.write_text(generated_code)
        
        print(f"✅ Generated communication tool: {code_path}")
        
    except Exception as e:
        print(f"❌ Error generating code: {e}")
        return
    
    # Step 3: Demonstrate usage
    print(f"\n🎯 Step 3: Usage example")
    print(f"To communicate with the washing machine at {device_ip}:")
    print()
    print("```python")
    print(f"from tools.generated.{cache_key} import DeviceCommunicator")
    print()
    print("# Initialize connection")
    print(f"washer = DeviceCommunicator('{device_ip}')")
    print("washer.connect()")
    print()
    print("# Check status")
    print("status = washer.get_status()")
    print("print(f'Washing machine status: {status}')")
    print()
    print("# Start a normal cycle")
    print("washer.start_cycle(cycle_type='normal')")
    print()
    print("# Check progress")
    print("progress = washer.get_cycle_progress()")
    print("print(f'Cycle progress: {progress}')")
    print()
    print("# Disconnect")
    print("washer.disconnect()")
    print("```")
    
    print(f"\n✨ Demo complete! Files generated:")
    print(f"   📋 Spec: {spec_path}")
    print(f"   🐍 Code: {code_path}")

if __name__ == "__main__":
    asyncio.run(process_smartthings_washing_machine())