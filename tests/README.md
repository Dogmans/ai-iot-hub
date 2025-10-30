# Tests Directory

This directory contains all test files for the AI-IoT Hub project.

## Test Files

### Configuration & Setup Tests
- `test_imports_config.py` - Test CodeAgent import configuration
- `test_controller.py` - Test main AI controller initialization  
- `test_installation.py` - Test project installation and dependencies
- `test_hub.py` - Test hub functionality

### Discovery & Communication Tests  
- `test_discovery.py` - Test basic device discovery
- `test_enhanced_discovery.py` - Test enhanced discovery with all protocols
- `test_working_discovery.py` - Working discovery pipeline test

### Agent & Code Generation Tests
- `test_code_generation.py` - Test CodeAgent code generation
- `test_pathlib.py` - Test pathlib usage in generated code

### UI & Interface Tests
- `test_textual.py` - Test Textual UI components
- `test_terminal_fix.py` - Test terminal output fixes

### Error Handling Tests
- `test_error_handling.py` - Test comprehensive error handling

### Utility Tests
- `quick_test.py` - Quick functionality test
- `verify_terminal_fix.py` - Verify terminal fixes work

## Running Tests

From the project root:

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_discovery.py

# Run with verbose output
python tests/test_imports_config.py
```

## Adding New Tests

1. Create test file with `test_` prefix
2. Follow existing patterns for imports and setup
3. Add description to this README
4. Ensure tests are runnable from project root