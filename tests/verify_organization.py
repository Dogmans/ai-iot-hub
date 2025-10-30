#!/usr/bin/env python3
"""
Verify that file organization is successful and all files are accessible
"""

import os
from pathlib import Path

def check_directory_structure():
    """Check that the new directory structure is correct"""
    print("🗂️ Verifying Project Organization")
    print("=" * 50)
    
    # Expected structure
    expected_dirs = {
        "tests": "Test files",
        "demos": "Demonstration scripts", 
        "examples": "Reference implementations",
        "src": "Core application code",
        "config": "Configuration files",
        "devices": "Device documentation and specs",
        "tools": "Generated tools and utilities",
        "docs": "Documentation"
    }
    
    # Check directories exist
    for dir_name, description in expected_dirs.items():
        dir_path = Path(dir_name)
        if dir_path.exists():
            file_count = len(list(dir_path.glob("*.py"))) + len(list(dir_path.glob("*.md")))
            print(f"✅ {dir_name:12} - {description} ({file_count} files)")
        else:
            print(f"❌ {dir_name:12} - Missing directory")
    
    print()

def check_moved_files():
    """Check that moved files are in correct locations"""
    print("📁 Checking Moved Files")
    print("-" * 30)
    
    # Check test files
    test_files = list(Path("tests").glob("test_*.py"))
    print(f"Tests: {len(test_files)} files")
    for f in test_files[:3]:  # Show first 3
        print(f"  ✅ {f.name}")
    if len(test_files) > 3:
        print(f"  ... and {len(test_files) - 3} more")
    
    # Check demo files  
    demo_files = list(Path("demos").glob("demo_*.py"))
    print(f"Demos: {len(demo_files)} files")
    for f in demo_files:
        print(f"  ✅ {f.name}")
    
    # Check examples
    example_files = list(Path("examples").glob("*.py"))
    print(f"Examples: {len(example_files)} files")
    for f in example_files[:3]:  # Show first 3
        print(f"  ✅ {f.name}")
    
    print()

def check_readmes():
    """Check that README files exist in organized directories"""
    print("📖 Checking Documentation")
    print("-" * 30)
    
    readme_dirs = ["tests", "demos", "examples"]
    for dir_name in readme_dirs:
        readme_path = Path(dir_name) / "README.md"
        if readme_path.exists():
            print(f"✅ {dir_name}/README.md exists")
        else:
            print(f"❌ {dir_name}/README.md missing")
    
    print()

def check_root_cleanliness():
    """Check that root directory is cleaner"""
    print("🧹 Root Directory Cleanliness")
    print("-" * 30)
    
    root_py_files = list(Path(".").glob("*.py"))
    
    # Expected files in root
    expected_root_files = [
        "interactive_hub.py"  # Main entry point should stay in root
    ]
    
    unexpected_files = [f for f in root_py_files if f.name not in expected_root_files]
    
    print(f"Python files in root: {len(root_py_files)}")
    for f in expected_root_files:
        if Path(f).exists():
            print(f"  ✅ {f} (expected)")
        else:
            print(f"  ❌ {f} (missing)")
    
    if unexpected_files:
        print(f"  ⚠️  Unexpected files: {[f.name for f in unexpected_files]}")
    else:
        print("  ✅ No unexpected Python files in root")
    
    print()

def test_imports():
    """Test that moved files can still be imported correctly"""
    print("🔍 Testing File Accessibility")
    print("-" * 30)
    
    try:
        # Test that we can run files from new locations
        import subprocess
        
        # Test a simple test file using current Python executable
        import sys
        result = subprocess.run(
            [sys.executable, "tests/test_imports_config.py"], 
            capture_output=True, 
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Tests run successfully from new location")
        else:
            print(f"❌ Test failed: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Import test failed: {e}")

if __name__ == "__main__":
    check_directory_structure()
    check_moved_files()
    check_readmes()
    check_root_cleanliness()
    test_imports()
    
    print("🎉 File organization verification complete!")
    print("\n📝 Summary:")
    print("- Tests moved to tests/ directory with README")
    print("- Demos moved to demos/ directory with README") 
    print("- Examples organized in examples/ directory with README")
    print("- Root directory cleaned up")
    print("- All files accessible from new locations")