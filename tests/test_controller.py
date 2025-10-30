#!/usr/bin/env python3
"""Test AI controller initialization"""

from src.hub.ai_controller import AIDeviceController

def test_controller():
    """Test AI controller initialization"""
    try:
        controller = AIDeviceController()
        print("✅ AI Controller initialized successfully")
        print(f"📋 Agent authorized imports: {controller.agent.authorized_imports}")
        print(f"🔧 Total authorized modules: {len(controller.agent.authorized_imports)}")
        
        # Test a simple pathlib operation
        code = '''
from pathlib import Path
current_dir = Path.cwd()
result = str(current_dir)
'''
        try:
            exec_result = controller.agent.python_executor(code)
            print("✅ Pathlib test successful")
            print("Execution result:", exec_result)
        except Exception as e:
            print(f"❌ Pathlib execution failed: {e}")
            
    except Exception as e:
        print(f"❌ Controller initialization failed: {e}")

if __name__ == "__main__":
    test_controller()