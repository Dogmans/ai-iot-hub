#!/usr/bin/env python3
"""Test pathlib usage with CodeAgent"""

from smolagents import CodeAgent

def test_pathlib():
    """Test that pathlib works with CodeAgent"""
    agent = CodeAgent(
        tools=[], 
        model=None, 
        additional_authorized_imports=['pathlib']
    )
    
    code = '''
from pathlib import Path

# Test basic pathlib operations
current_dir = Path.cwd()
print("Current directory:", current_dir)

# Test path operations
test_path = Path("test") / "file.txt"
print("Test path:", test_path)

# List some files in current dir (first 3)
files = list(current_dir.iterdir())[:3]
file_names = [f.name for f in files]
print("First 3 files:", file_names)
'''
    
    try:
        result = agent.python_executor(code)
        print("✅ Pathlib test successful!")
        print("Result:", result)
        return True
    except Exception as e:
        print(f"❌ Pathlib test failed: {e}")
        return False

if __name__ == "__main__":
    test_pathlib()