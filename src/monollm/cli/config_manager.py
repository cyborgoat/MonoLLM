"""
Configuration Manager for MonoLLM CLI

Handles configuration management including model settings, proxy configuration,
API keys, and other customizable parameters for both user and machine interfaces.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict

from ..core.client import UnifiedLLMClient
from ..core.models import RequestConfig


@dataclass
class ProxyConfig:
    """Proxy configuration settings."""
    http: Optional[str] = None
    https: Optional[str] = None
    socks: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Optional[str]]:
        """Convert to dictionary format."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProxyConfig':
        """Create from dictionary."""
        return cls(
            http=data.get('http'),
            https=data.get('https'),
            socks=data.get('socks')
        )


@dataclass
class ModelDefaults:
    """Default settings for a model."""
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: bool = False
    show_thinking: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelDefaults':
        """Create from dictionary."""
        return cls(
            temperature=data.get('temperature'),
            max_tokens=data.get('max_tokens'),
            stream=data.get('stream', False),
            show_thinking=data.get('show_thinking', False)
        )


class ConfigManager:
    """Manages configuration for MonoLLM CLI."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path("config")
        self.user_config_file = self.config_dir / "user_defaults.json"
        self.proxy_config_file = self.config_dir / "proxy.json"
        self._client = None
    
    @property
    def client(self) -> UnifiedLLMClient:
        """Get or create UnifiedLLMClient instance."""
        if self._client is None:
            self._client = UnifiedLLMClient(config_dir=self.config_dir)
        return self._client
    
    def get_model_info(self, model_id: str, provider_id: Optional[str] = None):
        """Get model information and provider."""
        return self.client.get_model_info(model_id, provider_id)
    
    def list_providers(self):
        """List all available providers."""
        return self.client.list_providers()
    
    def list_models(self, provider_id: Optional[str] = None):
        """List all available models."""
        return self.client.list_models(provider_id)
    
    def get_model_defaults(self, model_id: str) -> ModelDefaults:
        """Get default settings for a model."""
        user_config = self._load_user_config()
        model_defaults = user_config.get("model_defaults", {}).get(model_id, {})
        return ModelDefaults.from_dict(model_defaults)
    
    def set_model_defaults(self, model_id: str, defaults: ModelDefaults) -> None:
        """Set default settings for a model."""
        user_config = self._load_user_config()
        if "model_defaults" not in user_config:
            user_config["model_defaults"] = {}
        
        user_config["model_defaults"][model_id] = defaults.to_dict()
        self._save_user_config(user_config)
    
    def get_proxy_config(self) -> ProxyConfig:
        """Get proxy configuration."""
        if self.proxy_config_file.exists():
            try:
                with open(self.proxy_config_file, 'r') as f:
                    data = json.load(f)
                return ProxyConfig.from_dict(data)
            except (json.JSONDecodeError, KeyError):
                pass
        
        return ProxyConfig()
    
    def set_proxy_config(self, proxy_config: ProxyConfig) -> None:
        """Set proxy configuration."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.proxy_config_file, 'w') as f:
            json.dump(proxy_config.to_dict(), f, indent=2)
    
    def create_request_config(
        self,
        model: str,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: Optional[bool] = None,
        show_thinking: Optional[bool] = None,
        use_defaults: bool = True
    ) -> RequestConfig:
        """Create a RequestConfig with optional defaults."""
        
        # Get model defaults if requested
        if use_defaults:
            defaults = self.get_model_defaults(model)
        else:
            defaults = ModelDefaults()
        
        # Get proxy configuration
        proxy_config = self.get_proxy_config()
        proxy_dict = None
        if any([proxy_config.http, proxy_config.https, proxy_config.socks]):
            proxy_dict = {k: v for k, v in proxy_config.to_dict().items() if v is not None}
        
        # Create config with parameter precedence: explicit > defaults > None
        config = RequestConfig(
            model=model,
            provider=provider,
            temperature=temperature if temperature is not None else defaults.temperature,
            max_tokens=max_tokens if max_tokens is not None else defaults.max_tokens,
            stream=stream if stream is not None else defaults.stream,
            show_thinking=show_thinking if show_thinking is not None else defaults.show_thinking,
            proxy=proxy_dict
        )
        
        return config
    
    def validate_model_config(self, model_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and adjust configuration for a specific model."""
        try:
            provider_id, model_info = self.get_model_info(model_id)
            
            # Validate temperature
            if config.get('temperature') is not None and not model_info.supports_temperature:
                config['temperature'] = None
            
            # Validate streaming
            if config.get('stream') and not model_info.supports_streaming:
                config['stream'] = False
            
            # Force streaming for stream-only models
            if getattr(model_info, 'stream_only', False):
                config['stream'] = True
            
            # Validate thinking
            if config.get('show_thinking') and not model_info.supports_thinking:
                config['show_thinking'] = False
            
            # Validate max_tokens
            if config.get('max_tokens') and config['max_tokens'] > model_info.max_tokens:
                config['max_tokens'] = model_info.max_tokens
            
            return config
            
        except Exception:
            # If model validation fails, return config as-is
            return config
    
    def get_api_key_status(self) -> Dict[str, bool]:
        """Check which API keys are configured."""
        api_keys = {
            'openai': 'OPENAI_API_KEY',
            'anthropic': 'ANTHROPIC_API_KEY',
            'qwen': 'DASHSCOPE_API_KEY',
            'deepseek': 'DEEPSEEK_API_KEY',
            'google': 'GOOGLE_API_KEY',
            'volcengine': 'VOLCENGINE_API_KEY'
        }
        
        status = {}
        for provider, env_var in api_keys.items():
            status[provider] = bool(os.getenv(env_var))
        
        return status
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get environment information."""
        return {
            "config_dir": str(self.config_dir.absolute()),
            "user_config_exists": self.user_config_file.exists(),
            "proxy_config_exists": self.proxy_config_file.exists(),
            "api_key_status": self.get_api_key_status(),
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}"
        }
    
    def reset_model_defaults(self, model_id: Optional[str] = None) -> None:
        """Reset model defaults (specific model or all)."""
        user_config = self._load_user_config()
        
        if model_id:
            # Reset specific model
            if "model_defaults" in user_config and model_id in user_config["model_defaults"]:
                del user_config["model_defaults"][model_id]
        else:
            # Reset all model defaults
            user_config["model_defaults"] = {}
        
        self._save_user_config(user_config)
    
    def export_config(self) -> Dict[str, Any]:
        """Export all configuration for backup/sharing."""
        return {
            "user_config": self._load_user_config(),
            "proxy_config": self.get_proxy_config().to_dict(),
            "environment_info": self.get_environment_info()
        }
    
    def import_config(self, config_data: Dict[str, Any]) -> None:
        """Import configuration from backup."""
        if "user_config" in config_data:
            self._save_user_config(config_data["user_config"])
        
        if "proxy_config" in config_data:
            proxy_config = ProxyConfig.from_dict(config_data["proxy_config"])
            self.set_proxy_config(proxy_config)
    
    def _load_user_config(self) -> Dict[str, Any]:
        """Load user configuration file."""
        if self.user_config_file.exists():
            try:
                with open(self.user_config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        return {}
    
    def _save_user_config(self, config: Dict[str, Any]) -> None:
        """Save user configuration file."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.user_config_file, 'w') as f:
            json.dump(config, f, indent=2) 