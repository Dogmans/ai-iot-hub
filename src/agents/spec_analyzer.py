"""
Specification Analyzer Agent

Parses raw device documentation (PDFs, URLs, Word docs) into structured 
JSON specifications using LLM capabilities.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List
import PyPDF2
import requests
from docx import Document

logger = logging.getLogger(__name__)

class SpecAnalyzer:
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt', '.docx']
    
    async def parse_document(self, doc_path: Path) -> Dict[str, Any]:
        """Parse any supported document format into structured spec"""
        doc_path = Path(doc_path)
        
        if not doc_path.exists():
            raise FileNotFoundError(f"Document not found: {doc_path}")
        
        # Extract text content based on file type
        if doc_path.suffix == '.pdf':
            content = self._extract_pdf_content(doc_path)
        elif doc_path.suffix == '.txt':
            content = self._extract_url_content(doc_path)
        elif doc_path.suffix == '.docx':
            content = self._extract_docx_content(doc_path)
        else:
            raise ValueError(f"Unsupported format: {doc_path.suffix}")
        
        logger.info(f"[SPEC_GEN] Extracted {len(content)} characters from {doc_path}")
        
        # Use LLM to parse content into structured spec
        spec = await self._generate_structured_spec(content, doc_path)
        
        # Cache the generated spec
        await self._cache_spec(spec, doc_path)
        
        return spec
    
    def _extract_pdf_content(self, pdf_path: Path) -> str:
        """Extract text content from PDF"""
        content = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                content.append(page.extract_text())
        return '\n'.join(content)
    
    def _extract_url_content(self, txt_path: Path) -> str:
        """Extract content from URL (if .txt contains URL) or read as text"""
        content = txt_path.read_text(encoding='utf-8')
        
        # Check if content is a URL
        if content.strip().startswith('http'):
            url = content.strip()
            logger.info(f"[SPEC_GEN] Fetching content from URL: {url}")
            
            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.error(f"Failed to fetch URL content: {e}")
                raise
        
        return content
    
    def _extract_docx_content(self, docx_path: Path) -> str:
        """Extract text content from Word document"""
        doc = Document(docx_path)
        content = []
        
        for paragraph in doc.paragraphs:
            content.append(paragraph.text)
            
        return '\n'.join(content)
    
    async def _generate_structured_spec(self, content: str, source_path: Path) -> Dict[str, Any]:
        """Use LLM to convert raw content into structured device spec"""
        
        # Use smolagents CodeAgent to analyze the documentation
        from smolagents import CodeAgent, InferenceClientModel
        
        model = InferenceClientModel(model_id="meta-llama/Meta-Llama-3.1-8B-Instruct")
        agent = CodeAgent(
            tools=[],
            model=model,
            additional_authorized_imports=['json', 're'],
            instructions="""You are a device specification analyzer. Your job is to parse IoT device documentation and extract structured information about communication protocols, endpoints, and capabilities."""
        )
        
        analysis_prompt = f"""
Analyze the following IoT device documentation and extract structured information:

DOCUMENTATION CONTENT:
{content[:5000]}...  # Truncate for token limits

TASK: Create a structured JSON specification with the following information:

1. **Device Type**: What kind of device is this? (thermostat, sensor, washing_machine, etc.)
2. **Protocol**: How does it communicate? (rest, tcp, mqtt, modbus_tcp, websocket)  
3. **Authentication**: What authentication is required? (none, api_key, bearer_token, basic_auth)
4. **Base URL/Connection**: API base URL or connection details
5. **Endpoints/Commands**: Available API endpoints or device commands
6. **Capabilities**: What can this device do? (temperature control, status monitoring, etc.)

Extract this information and return a JSON object with the structure:
```json
{{
  "device_type": "string",
  "protocol": "string", 
  "manufacturer": "string",
  "authentication": {{
    "type": "string",
    "parameters": {{}}
  }},
  "base_url": "string",
  "endpoints": [
    {{
      "name": "string",
      "method": "string",
      "path": "string", 
      "description": "string",
      "parameters": {{}}
    }}
  ],
  "capabilities": ["string"],
  "connection_info": {{
    "default_port": 80,
    "timeout": 30
  }}
}}
```

Generate the JSON specification now:
"""
        
        try:
            # Get LLM analysis
            response = agent.run(analysis_prompt)
            
            # Try to extract JSON from response
            import json
            import re
            
            # Look for JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    analyzed_spec = json.loads(json_match.group())
                    logger.info("LLM successfully analyzed device documentation")
                    
                    # Add metadata
                    analyzed_spec["source_document"] = str(source_path)
                    analyzed_spec["generated_at"] = "2025-01-12T00:00:00Z"
                    
                    return analyzed_spec
                    
                except json.JSONDecodeError:
                    logger.warning("LLM response was not valid JSON, using fallback")
            
        except Exception as e:
            logger.warning(f"LLM analysis failed: {e}, using fallback analysis")
        
        # Fallback to rule-based analysis if LLM fails
        template_spec = {
            "source_document": str(source_path),
            "device_type": self._infer_device_type(source_path),
            "protocol": self._infer_protocol(content),
            "manufacturer": "Unknown",
            "model": "Unknown",
            "endpoints": self._extract_endpoints(content),
            "authentication": {
                "type": "none",
                "parameters": {}
            },
            "data_formats": ["json"],
            "connection_info": {
                "default_port": self._infer_default_port(content),
                "timeout": 30
            },
            "capabilities": self._extract_capabilities(content),
            "generated_at": "2025-01-12T00:00:00Z"
        }
        
        return template_spec
    
    def _infer_device_type(self, source_path: Path) -> str:
        """Infer device type from path or filename"""
        path_parts = source_path.parts
        
        # Look for device type in path
        device_types = ['thermostat', 'sensor', 'camera', 'switch', 'gateway']
        for part in path_parts:
            for device_type in device_types:
                if device_type in part.lower():
                    return device_type
        
        return "unknown"
    
    def _infer_protocol(self, content: str) -> str:
        """Infer communication protocol from content"""
        content_lower = content.lower()
        
        if 'modbus' in content_lower:
            return 'modbus_tcp'
        elif 'rest' in content_lower or 'api' in content_lower:
            return 'rest'
        elif 'mqtt' in content_lower:
            return 'mqtt'
        elif 'websocket' in content_lower:
            return 'websocket'
        elif 'tcp' in content_lower:
            return 'tcp'
        elif 'http' in content_lower:
            return 'http'
        
        return 'unknown'
    
    def _infer_default_port(self, content: str) -> int:
        """Infer default port from content"""
        import re
        
        # Look for common port patterns
        port_pattern = r'port\s*:?\s*(\d+)'
        matches = re.findall(port_pattern, content.lower())
        
        if matches:
            return int(matches[0])
        
        # Default ports by protocol
        defaults = {
            'modbus': 502,
            'http': 80,
            'https': 443,
            'mqtt': 1883
        }
        
        for protocol, port in defaults.items():
            if protocol in content.lower():
                return port
        
        return 80  # Default fallback
    
    def _extract_endpoints(self, content: str) -> List[Dict[str, Any]]:
        """Extract API endpoints/commands from content"""
        # TODO: Implement intelligent endpoint extraction
        # This would use NLP/LLM to identify API endpoints, commands, etc.
        
        # Template endpoints
        return [
            {
                "name": "get_status",
                "method": "GET",
                "path": "/api/status",
                "description": "Get device status"
            },
            {
                "name": "set_temperature",
                "method": "POST", 
                "path": "/api/temperature",
                "description": "Set target temperature",
                "parameters": {
                    "temperature": {"type": "float", "required": True}
                }
            }
        ]
    
    def _extract_capabilities(self, content: str) -> List[str]:
        """Extract device capabilities from content"""
        capabilities = []
        
        capability_keywords = {
            'temperature': ['temperature', 'temp', 'heating', 'cooling'],
            'humidity': ['humidity', 'moisture'],
            'motion': ['motion', 'movement', 'pir'],
            'light': ['light', 'illumination', 'brightness'],
            'security': ['security', 'alarm', 'door', 'window']
        }
        
        content_lower = content.lower()
        for capability, keywords in capability_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                capabilities.append(capability)
        
        return capabilities
    
    async def _cache_spec(self, spec: Dict[str, Any], source_path: Path):
        """Cache generated spec to filesystem"""
        device_type = spec.get('device_type', 'unknown')
        manufacturer = spec.get('manufacturer', 'unknown')
        
        cache_filename = f"{manufacturer}_{device_type}_spec.json"
        cache_path = Path(f"devices/generated_specs/{cache_filename}")
        
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(cache_path, 'w') as f:
            json.dump(spec, f, indent=2)
        
        logger.info(f"[SPEC_GEN] Cached spec at: {cache_path}")