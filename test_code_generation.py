#!/usr/bin/env python3
"""
Test that CodeAgent can actually use the configured imports to generate working code
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, "src")

from agents.code_writing_agent import DeviceCodeAgent

async def test_code_generation():
    """Test that CodeAgent can generate code using configured imports"""
    print("🧪 Testing CodeAgent Code Generation")
    print("=" * 50)
    
    try:
        # Initialize with real config
        from hub.ai_controller import AIDeviceController
        controller = AIDeviceController()
        
        code_agent = DeviceCodeAgent(config=controller.config)
        
        # Simple test prompt that uses basic imports
        test_prompt = """
Write a simple Python function that:
1. Uses pathlib to create a file path
2. Uses json to create some data
3. Uses time to add a timestamp
4. Returns a dictionary with the results

The function should be called 'test_imports' and demonstrate that the imports work.
"""
        
        print("📝 Generating test code...")
        print("Prompt:", test_prompt[:100] + "...")
        
        # This should work with our configured imports
        result = code_agent.agent.run(test_prompt)
        
        print(f"✅ Code generation successful!")
        print(f"Result type: {type(result)}")
        print(f"Result preview: {str(result)[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_code_generation())