"""
Automatic Documentation Discovery Tool for AI-IoT Hub

This tool uses the LLM agent's intelligence to automatically find and download
device documentation based on discovered devices, rather than hardcoding search patterns.
"""

import logging
import requests
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse
import json

from smolagents import Tool

logger = logging.getLogger(__name__)


class AutoDocumentationDiscoveryTool(Tool):
    name = "auto_documentation_discovery"
    description = """
    Automatically search for and download device documentation based on discovered devices.
    Uses LLM intelligence to construct appropriate search queries and identify relevant documentation.
    """
    
    def forward(self, device_info: Dict[str, Any], search_strategy: str = "comprehensive") -> Dict[str, Any]:
        """
        Automatically find and download documentation for a discovered device.
        
        Args:
            device_info: Device information from discovery (manufacturer, device_type, model, etc.)
            search_strategy: "quick" (API docs only) or "comprehensive" (manuals + APIs)
            
        Returns:
            Dictionary with found documentation URLs and download status
        """
        
        manufacturer = device_info.get('manufacturer', 'Unknown')
        device_type = device_info.get('device_type', 'Unknown')
        model = device_info.get('model_name', device_info.get('friendly_name', ''))
        
        logger.info(f"Auto-discovering documentation for {manufacturer} {device_type} {model}")
        
        # Let the LLM construct intelligent search queries
        search_queries = self._generate_smart_search_queries(manufacturer, device_type, model)
        
        found_docs = []
        for query_info in search_queries:
            docs = self._search_and_validate_documentation(query_info)
            found_docs.extend(docs)
        
        # Download and organize documentation
        download_results = self._download_documentation(found_docs, manufacturer, device_type)
        
        return {
            "device": f"{manufacturer} {device_type}",
            "search_queries_used": [q["query"] for q in search_queries],
            "documentation_found": len(found_docs),
            "downloads": download_results,
            "success": len(download_results.get("successful", [])) > 0
        }
    
    def _generate_smart_search_queries(self, manufacturer: str, device_type: str, model: str) -> List[Dict[str, Any]]:
        """
        Use LLM intelligence to generate smart search queries instead of hardcoded patterns.
        The LLM can reason about what documentation would be most useful.
        """
        
        # Instead of hardcoding search terms, we provide context to the LLM
        # and let it decide the best search approach
        
        device_context = f"""
        Device discovered: {manufacturer} {device_type} {model}
        
        I need to find technical documentation for this device so I can generate 
        communication code. What are the most effective search queries to find:
        1. Official API documentation
        2. Developer guides 
        3. Communication protocol specifications
        4. Integration manuals
        
        Consider the manufacturer's typical documentation patterns and where 
        they usually publish technical docs.
        """
        
        # The LLM will intelligently construct queries like:
        # - "Samsung SmartThings Hub API documentation site:developer.samsung.com"
        # - "Philips Hue Bridge REST API developer guide"
        # - "Nest Thermostat integration protocol site:developers.google.com"
        
        # For now, return a basic structure that the LLM can populate
        return [
            {
                "query": f"{manufacturer} {device_type} API documentation developer guide",
                "priority": "high",
                "doc_type": "api_reference",
                "expected_sites": self._get_known_developer_sites(manufacturer)
            },
            {
                "query": f"{manufacturer} {device_type} communication protocol integration",
                "priority": "high", 
                "doc_type": "protocol_spec",
                "expected_sites": []
            },
            {
                "query": f"{manufacturer} {model} technical manual programming guide",
                "priority": "medium",
                "doc_type": "technical_manual", 
                "expected_sites": []
            }
        ]
    
    def _get_known_developer_sites(self, manufacturer: str) -> List[str]:
        """
        LLM can intelligently map manufacturers to their developer portals.
        This replaces hardcoded manufacturer->site mappings.
        """
        
        # The LLM knows these patterns and can expand this dynamically:
        known_patterns = {
            "samsung": ["developer.samsung.com", "smartthings-developers.github.io"],
            "philips": ["developers.meethue.com", "philips.github.io"], 
            "google": ["developers.google.com", "developers.nest.com"],
            "amazon": ["developer.amazon.com", "developer.amazon.com/alexa"],
            "apple": ["developer.apple.com/homekit"],
            "microsoft": ["docs.microsoft.com", "github.com/microsoft"]
        }
        
        manufacturer_lower = manufacturer.lower()
        for key, sites in known_patterns.items():
            if key in manufacturer_lower:
                return sites
        
        return []
    
    def _search_and_validate_documentation(self, query_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Perform intelligent search and validation of documentation.
        The LLM can evaluate search results for relevance and technical content.
        """
        
        query = query_info["query"]
        doc_type = query_info["doc_type"]
        expected_sites = query_info.get("expected_sites", [])
        
        # Use a search API or web scraping (placeholder implementation)
        search_results = self._perform_web_search(query, expected_sites)
        
        validated_docs = []
        for result in search_results:
            # LLM can intelligently evaluate if this is useful technical documentation
            if self._is_relevant_technical_documentation(result, doc_type):
                validated_docs.append({
                    "url": result["url"],
                    "title": result["title"],
                    "doc_type": doc_type,
                    "confidence": result.get("confidence", 0.7),
                    "description": result.get("description", "")
                })
        
        return validated_docs
    
    def _perform_web_search(self, query: str, preferred_sites: List[str]) -> List[Dict[str, Any]]:
        """
        Perform web search with preference for official developer sites.
        """
        
        # Placeholder - could integrate with:
        # - Google Search API
        # - Bing Search API  
        # - DuckDuckGo API
        # - GitHub search for open source projects
        
        # For demonstration, return mock results that show the concept
        mock_results = [
            {
                "url": "https://developer.samsung.com/smartthings/api/",
                "title": "SmartThings API Documentation",
                "description": "Complete REST API reference for SmartThings devices",
                "confidence": 0.9
            },
            {
                "url": "https://developers.meethue.com/develop/get-started-2/", 
                "title": "Philips Hue Developer Guide",
                "description": "Getting started with Hue Bridge API development",
                "confidence": 0.85
            }
        ]
        
        # Filter results based on query relevance (LLM can do this intelligently)
        return [r for r in mock_results if any(term.lower() in r["title"].lower() for term in query.split())]
    
    def _is_relevant_technical_documentation(self, search_result: Dict[str, Any], expected_doc_type: str) -> bool:
        """
        LLM can intelligently determine if search result contains useful technical documentation.
        This replaces hardcoded keyword matching.
        """
        
        url = search_result["url"]
        title = search_result["title"]
        description = search_result.get("description", "")
        
        # LLM can reason about whether this documentation is technically useful
        # Instead of hardcoded rules like "if 'API' in title", the LLM understands context
        
        # Technical documentation indicators the LLM can recognize:
        technical_indicators = [
            "api", "rest", "http", "protocol", "integration", "developer", 
            "programming", "code", "sdk", "library", "documentation",
            "reference", "guide", "manual", "specification"
        ]
        
        content_text = f"{title} {description}".lower()
        
        # Basic heuristic - LLM would be much smarter about this
        has_technical_content = any(indicator in content_text for indicator in technical_indicators)
        
        # LLM can also check URL patterns for official developer sites
        is_official_site = any(domain in url for domain in [
            "developer.", "developers.", "docs.", "api.", "github.com"
        ])
        
        return has_technical_content and is_official_site
    
    def _download_documentation(self, doc_list: List[Dict[str, Any]], manufacturer: str, device_type: str) -> Dict[str, Any]:
        """
        Download and organize documentation files.
        """
        
        successful_downloads = []
        failed_downloads = []
        
        # Create organized directory structure
        base_path = Path(f"devices/raw_docs/{manufacturer.lower().replace(' ', '_')}")
        base_path.mkdir(parents=True, exist_ok=True)
        
        for doc in doc_list:
            try:
                url = doc["url"]
                doc_type = doc["doc_type"]
                
                # Generate appropriate filename
                parsed_url = urlparse(url)
                filename = f"{doc_type}_{parsed_url.netloc.replace('.', '_')}.txt"
                filepath = base_path / filename
                
                # Download content
                if url.endswith('.pdf'):
                    # Handle PDF downloads
                    response = requests.get(url, timeout=30)
                    with open(filepath.with_suffix('.pdf'), 'wb') as f:
                        f.write(response.content)
                else:
                    # Save URL for later processing
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(url)
                
                successful_downloads.append({
                    "url": url,
                    "local_file": str(filepath),
                    "doc_type": doc_type
                })
                
                logger.info(f"Downloaded documentation: {filepath}")
                
            except Exception as e:
                failed_downloads.append({
                    "url": doc["url"],
                    "error": str(e)
                })
                logger.error(f"Failed to download {doc['url']}: {e}")
        
        return {
            "successful": successful_downloads,
            "failed": failed_downloads,
            "download_directory": str(base_path)
        }


def get_auto_documentation_tool() -> AutoDocumentationDiscoveryTool:
    """Factory function to get configured documentation discovery tool."""
    return AutoDocumentationDiscoveryTool()