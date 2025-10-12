"""
Device discovery package for AI-IoT Hub.

This package provides comprehensive device discovery capabilities using multiple methods
including network scanning, mDNS service discovery, UPnP, and HTTP fingerprinting.
"""

from .comprehensive_discovery import ComprehensiveDeviceDiscovery, get_discovery_engine

__all__ = ['ComprehensiveDeviceDiscovery', 'get_discovery_engine']