"""Configuration loader for the unified LLM framework."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from ..core.exceptions import ConfigurationError
from ..core.models import ProviderInfo, ModelInfo, ProxyConfig, TimeoutConfig, RetryConfig


class ConfigLoader:
    """Loads configuration from files and environment variables."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the configuration loader.
        
        Args:
            config_dir: Directory containing configuration files. 
                       Defaults to ./config relative to current directory.
        """
        self.config_dir = config_dir or Path("config")
        self.models_file = self.config_dir / "models.json"
        
        # Load environment variables from .env file
        load_dotenv()
    
    def load_providers(self) -> Dict[str, ProviderInfo]:
        """Load provider configurations from models.json."""
        if not self.models_file.exists():
            raise ConfigurationError(
                f"Models configuration file not found: {self.models_file}",
                config_type="models"
            )
        
        try:
            with open(self.models_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            providers = {}
            for provider_id, provider_data in data.get("providers", {}).items():
                models = {}
                for model_id, model_data in provider_data.get("models", {}).items():
                    models[model_id] = ModelInfo(**model_data)
                
                provider_info = ProviderInfo(
                    name=provider_data["name"],
                    base_url=provider_data["base_url"],
                    uses_openai_protocol=provider_data.get("uses_openai_protocol", False),
                    supports_streaming=provider_data.get("supports_streaming", True),
                    supports_mcp=provider_data.get("supports_mcp", False),
                    models=models
                )
                providers[provider_id] = provider_info
            
            return providers
        
        except (json.JSONDecodeError, KeyError) as e:
            raise ConfigurationError(
                f"Error parsing models configuration: {e}",
                config_type="models"
            )
    
    def load_proxy_config(self) -> Dict[str, Any]:
        """Load proxy configuration from environment variables (.env file)."""
        # Load proxy settings from environment variables
        proxy_enabled = os.getenv("PROXY_ENABLED", "false").lower() in ["true", "1", "yes"]
        proxy_type = os.getenv("PROXY_TYPE", "http")
        proxy_host = os.getenv("PROXY_HOST")
        proxy_port = None
        if os.getenv("PROXY_PORT"):
            try:
                proxy_port = int(os.getenv("PROXY_PORT"))
            except ValueError:
                proxy_port = None
        
        proxy_username = os.getenv("PROXY_USERNAME")
        proxy_password = os.getenv("PROXY_PASSWORD")
        
        # SOCKS5 settings (alternative way to enable proxy)
        socks5_enabled = os.getenv("SOCKS5_ENABLED", "false").lower() in ["true", "1", "yes"]
        socks5_host = os.getenv("SOCKS5_HOST")
        socks5_port = None
        if os.getenv("SOCKS5_PORT"):
            try:
                socks5_port = int(os.getenv("SOCKS5_PORT"))
            except ValueError:
                socks5_port = None
        
        socks5_username = os.getenv("SOCKS5_USERNAME")
        socks5_password = os.getenv("SOCKS5_PASSWORD")
        
        # If SOCKS5 is enabled, use SOCKS5 settings
        if socks5_enabled:
            proxy_enabled = True
            proxy_type = "socks5"
            proxy_host = socks5_host
            proxy_port = socks5_port
            proxy_username = socks5_username
            proxy_password = socks5_password
        
        # Create proxy config
        proxy_config = ProxyConfig(
            enabled=proxy_enabled,
            type=proxy_type,
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
        )
        
        # Timeout configuration
        timeout_config = TimeoutConfig(
            connect=30,
            read=15,
            write=15
        )
        
        # Retry configuration
        retry_config = RetryConfig(
            max_attempts=3,
            backoff_factor=1.0,
            retry_on_status=[429, 500, 502, 503, 504]
        )
        
        return {
            "proxy": proxy_config,
            "timeout": timeout_config,
            "retry": retry_config
        }
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for a provider from environment variables."""
        env_var_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "qwen": "DASHSCOPE_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "volcengine": "VOLCENGINE_API_KEY"
        }
        
        env_var = env_var_map.get(provider.lower())
        if env_var:
            return os.getenv(env_var)
        
        # Try generic pattern
        generic_env_var = f"{provider.upper()}_API_KEY"
        return os.getenv(generic_env_var)
    
    def get_base_url_override(self, provider: str) -> Optional[str]:
        """Get base URL override from environment variables."""
        env_var = f"{provider.upper()}_BASE_URL"
        return os.getenv(env_var)
    
    def load_full_config(self) -> Dict[str, Any]:
        """Load complete configuration."""
        providers = self.load_providers()
        proxy_config = self.load_proxy_config()
        
        # Add API keys and base URL overrides to a separate metadata dict
        providers_with_metadata = {}
        for provider_id, provider_info in providers.items():
            api_key = self.get_api_key(provider_id)
            base_url_override = self.get_base_url_override(provider_id)
            
            # Store metadata separately since ProviderInfo is frozen
            metadata = {
                "api_key": api_key,
                "original_base_url": provider_info.base_url
            }
            
            if base_url_override:
                metadata["base_url_override"] = base_url_override
            
            # Store both provider info and metadata
            providers_with_metadata[provider_id] = {
                "provider_info": provider_info,
                "metadata": metadata
            }
        
        return {
            "providers": providers_with_metadata,
            **proxy_config
        } 