# AI-IoT Hub Installation Guide

## Quick Start (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/ai-iot-hub
cd ai-iot-hub

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install with specific feature groups
pip install -e ".[network,ui,ai]"
```

## Installation Options

### Core Installation
```bash
pip install -e .
```

### Feature Groups
```bash
# Network discovery (UPnP, mDNS, nmap)
pip install -e ".[network]"

# Rich terminal UI
pip install -e ".[ui]"

# AI/LLM functionality  
pip install -e ".[ai]"

# Document processing
pip install -e ".[docs-processing]"

# Development tools
pip install -e ".[dev]"

# Everything
pip install -e ".[all]"
```

## Troubleshooting

### lxml Compilation Errors on Windows

If you see errors about `libxml/xpath.h` or `xmlversion.h`, this means pip is trying to compile lxml from source instead of using binary wheels.

**Solution**: Our `pyproject.toml` is configured to use lxml>=6.0.0 which has reliable binary wheels for Windows.

**If you still have issues**:
```bash
# Install lxml binary first
pip install "lxml>=6.0.0,<7.0.0" --only-binary=lxml

# Then install the project
pip install -e ".[network]"
```

### Version Conflict Prevention

The `pyproject.toml` uses explicit version constraints to prevent common conflicts:

- **lxml**: Pinned to 6.x binary wheels (avoids 4.x source compilation)
- **upnpclient**: Works with lxml 6.x despite declaring <5.0.0 constraint
- **Dependencies shared across groups** are explicitly versioned for consistency

### Network Discovery Dependencies Status

After installation, verify network discovery tools:
```bash
python -c "
import netdisco, zeroconf, upnpclient
from mac_vendor_lookup import MacLookup
import ifaddr, scapy
print('✅ All network discovery dependencies working!')
"
```

Expected status: **5/5 tools working**

### Missing nmap Binary

`python-nmap` requires the `nmap` binary to be installed separately:

**Windows**: Download from https://nmap.org/download.html
**Linux**: `sudo apt install nmap` or `sudo yum install nmap`
**Mac**: `brew install nmap`

## Modern Python Packaging

This project uses `pyproject.toml` (PEP 621) instead of `requirements.txt`:

- ✅ **Modular installation** with optional dependency groups
- ✅ **Better dependency resolution** with explicit version constraints
- ✅ **Single source of truth** for project metadata
- ✅ **Forward compatible** with modern Python tooling

Installation pattern:
```bash
pip install -e ".[group1,group2,...]"
```

## Development Setup

```bash
# Install with development tools
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy src/
```