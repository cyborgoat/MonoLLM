"""Configuration manager for the unified LLM framework."""

import os
from pathlib import Path
from typing import Dict, Any, Optional

from unified_llm.core.models import ProviderInfo, ProxyConfig, TimeoutConfig, RetryConfig
from .loader import ConfigLoader


class ConfigManager:
    """Manages configuration for the unified LLM framework."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.loader = ConfigLoader(config_dir)
        self._config_cache: Optional[Dict[str, Any]] = None
    
    def reload_config(self) -> None:
        """Reload configuration from files."""
        self._config_cache = None
    
    def get_config(self) -> Dict[str, Any]:
        """Get the complete configuration."""
        if self._config_cache is None:
            self._config_cache = self.loader.load_full_config()
        return self._config_cache
    
    def get_providers(self) -> Dict[str, ProviderInfo]:
        """Get provider configurations."""
        return self.get_config()["providers"]
    
    def get_proxy_config(self) -> ProxyConfig:
        """Get proxy configuration."""
        return self.get_config()["proxy"]
    
    def get_timeout_config(self) -> TimeoutConfig:
        """Get timeout configuration."""
        return self.get_config()["timeout"]
    
    def get_retry_config(self) -> RetryConfig:
        """Get retry configuration."""
        return self.get_config()["retry"]
    
    def get_provider(self, provider_id: str) -> Optional[ProviderInfo]:
        """Get a specific provider configuration.
        
        Args:
            provider_id: ID of the provider
            
        Returns:
            Provider info or None if not found
        """
        providers = self.get_providers()
        return providers.get(provider_id)
    
    def has_api_key(self, provider_id: str) -> bool:
        """Check if a provider has an API key configured.
        
        Args:
            provider_id: ID of the provider
            
        Returns:
            True if API key is available
        """
        api_key = self.loader.get_api_key(provider_id)
        return api_key is not None and api_key.strip() != "" 