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

from agents.code_writing_agent import DeviceCodeAgent

async def process_smartthings_washing_machine():
    """Generate washing machine communicator using CodeAgent (processes docs directly)"""
    
    print("🚀 AI-IoT Hub Demo: Samsung SmartThings Washing Machine")
    print("=" * 60)
    
    # Initialize code agent (processes documentation directly)
    code_agent = DeviceCodeAgent()
    
    # Step 1: Documentation ready for CodeAgent processing
    doc_path = Path("devices/raw_docs/thermostats/samsung_smartthings_api.txt")
    print(f"\n📄 Step 1: Documentation available at {doc_path}")
    print("✅ CodeAgent will process documentation directly during code generation")
    
    # Step 2: Generate communication code for washing machine
    device_ip = "192.168.0.5"
    device_type = "washing_machine"
    
    print(f"\n🔧 Step 2: Generating communication code for washing machine at {device_ip}")
    
    try:
        # Generate the communication code (CodeAgent will process docs directly)
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
    
    print(f"\n✨ Demo complete! File generated:")
    print(f"   � Code: {code_path}")
    print(f"   � CodeAgent processed docs directly from: {doc_path}")

if __name__ == "__main__":
    asyncio.run(process_smartthings_washing_machine())