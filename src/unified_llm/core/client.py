"""Main client for the unified LLM framework."""

import uuid
from pathlib import Path
from typing import Dict, List, Optional, Union
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .models import (
    Message,
    LLMResponse,
    StreamingResponse,
    RequestConfig,
    ProviderInfo,
    ModelInfo,
)
from .exceptions import (
    UnifiedLLMError,
    ConfigurationError,
    ModelNotFoundError,
    ValidationError,
)
from ..config.loader import ConfigLoader
from ..providers.base import BaseProvider
from ..providers.openai_provider import OpenAIProvider
from ..providers.anthropic_provider import AnthropicProvider
from ..providers.google_provider import GoogleProvider
from ..providers.qwen_provider import QwenProvider
from ..providers.deepseek_provider import DeepSeekProvider
from ..providers.volcengine_provider import VolcengineProvider


class UnifiedLLMClient:
    """Main client for unified access to multiple LLM providers."""
    
    def __init__(
        self,
        config_dir: Optional[Path] = None,
        console: Optional[Console] = None,
    ):
        """Initialize the unified LLM client.
        
        Args:
            config_dir: Directory containing configuration files
            console: Rich console for output (optional)
        """
        self.console = console or Console()
        self.config_loader = ConfigLoader(config_dir)
        self.providers: Dict[str, BaseProvider] = {}
        self.provider_info: Dict[str, ProviderInfo] = {}
        self.provider_metadata: Dict[str, Dict] = {}
        
        # Load configuration
        self._load_configuration()
    
    def _load_configuration(self) -> None:
        """Load configuration and initialize providers."""
        try:
            config = self.config_loader.load_full_config()
            
            # Extract provider info and metadata
            for provider_id, provider_data in config["providers"].items():
                self.provider_info[provider_id] = provider_data["provider_info"]
                self.provider_metadata[provider_id] = provider_data["metadata"]
            
            self.proxy_config = config["proxy"]
            self.timeout_config = config["timeout"]
            self.retry_config = config["retry"]
            
            # Initialize providers
            self._initialize_providers()
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")
    
    def _initialize_providers(self) -> None:
        """Initialize all available providers."""
        provider_classes = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "google": GoogleProvider,
            "qwen": QwenProvider,
            "deepseek": DeepSeekProvider,
            "volcengine": VolcengineProvider,
        }
        
        for provider_id, provider_info in self.provider_info.items():
            provider_class = provider_classes.get(provider_id)
            if not provider_class:
                self.console.print(f"[yellow]Warning: No implementation for provider '{provider_id}'[/yellow]")
                continue
            
            try:
                # Get API key and configuration from metadata
                metadata = self.provider_metadata.get(provider_id, {})
                api_key = metadata.get('api_key')
                base_url_override = metadata.get('base_url_override')
                
                if not api_key:
                    self.console.print(f"[yellow]Warning: No API key found for provider '{provider_id}'[/yellow]")
                    continue
                
                provider = provider_class(
                    provider_info=provider_info,
                    api_key=api_key,
                    base_url_override=base_url_override,
                    proxy_config=self.proxy_config,
                    timeout_config=self.timeout_config,
                    retry_config=self.retry_config,
                )
                
                self.providers[provider_id] = provider
                self.console.print(f"[green]✓[/green] Initialized provider: {provider_info.name}")
                
            except Exception as e:
                self.console.print(f"[red]✗[/red] Failed to initialize provider '{provider_id}': {e}")
    
    def list_providers(self) -> Dict[str, ProviderInfo]:
        """List all available providers."""
        return self.provider_info
    
    def list_models(self, provider_id: Optional[str] = None) -> Dict[str, Dict[str, ModelInfo]]:
        """List all available models.
        
        Args:
            provider_id: Optional provider ID to filter models
            
        Returns:
            Dictionary mapping provider IDs to their models
        """
        if provider_id:
            if provider_id not in self.provider_info:
                raise ModelNotFoundError(
                    f"Provider '{provider_id}' not found",
                    provider=provider_id,
                    model="",
                    available_models=list(self.provider_info.keys())
                )
            return {provider_id: self.provider_info[provider_id].models}
        
        return {
            provider_id: provider_info.models
            for provider_id, provider_info in self.provider_info.items()
        }
    
    def get_model_info(self, model_id: str, provider_id: Optional[str] = None) -> tuple[str, ModelInfo]:
        """Get information about a specific model.
        
        Args:
            model_id: Model identifier
            provider_id: Optional provider ID to search in
            
        Returns:
            Tuple of (provider_id, model_info)
        """
        if provider_id:
            if provider_id not in self.provider_info:
                raise ModelNotFoundError(
                    f"Provider '{provider_id}' not found",
                    provider=provider_id,
                    model=model_id
                )
            
            provider_info = self.provider_info[provider_id]
            if model_id not in provider_info.models:
                raise ModelNotFoundError(
                    f"Model '{model_id}' not found in provider '{provider_id}'",
                    provider=provider_id,
                    model=model_id,
                    available_models=list(provider_info.models.keys())
                )
            
            return provider_id, provider_info.models[model_id]
        
        # Search across all providers
        for provider_id, provider_info in self.provider_info.items():
            if model_id in provider_info.models:
                return provider_id, provider_info.models[model_id]
        
        # Collect all available models for error message
        all_models = []
        for provider_info in self.provider_info.values():
            all_models.extend(provider_info.models.keys())
        
        raise ModelNotFoundError(
            f"Model '{model_id}' not found in any provider",
            provider="",
            model=model_id,
            available_models=all_models
        )
    
    def _validate_request_config(self, config: RequestConfig) -> tuple[str, str, ModelInfo]:
        """Validate request configuration and resolve provider/model.
        
        Returns:
            Tuple of (provider_id, model_id, model_info)
        """
        # Resolve provider and model
        provider_id, model_info = self.get_model_info(config.model, config.provider)
        
        # Check if provider is available
        if provider_id not in self.providers:
            raise ConfigurationError(
                f"Provider '{provider_id}' is not available. Check your API key configuration."
            )
        
        # Validate temperature setting
        if config.temperature is not None and not model_info.supports_temperature:
            raise ValidationError(
                f"Model '{config.model}' does not support temperature control",
                field="temperature",
                value=config.temperature
            )
        
        # Validate streaming setting
        if config.stream and not model_info.supports_streaming:
            raise ValidationError(
                f"Model '{config.model}' does not support streaming",
                field="stream",
                value=config.stream
            )
        
        # Validate thinking steps setting
        if config.show_thinking and not model_info.supports_thinking:
            raise ValidationError(
                f"Model '{config.model}' does not support thinking steps",
                field="show_thinking",
                value=config.show_thinking
            )
        
        return provider_id, config.model, model_info
    
    async def generate(
        self,
        messages: Union[str, List[Message]],
        config: RequestConfig,
    ) -> LLMResponse:
        """Generate a response from an LLM.
        
        Args:
            messages: Either a string (converted to user message) or list of messages
            config: Request configuration
            
        Returns:
            LLM response
        """
        # Convert string to messages if needed
        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]
        
        # Validate configuration
        provider_id, model_id, model_info = self._validate_request_config(config)
        
        # Get provider
        provider = self.providers[provider_id]
        
        # Generate request ID
        request_id = str(uuid.uuid4())
        config_with_id = config.model_copy()
        config_with_id.metadata = config_with_id.metadata or {}
        config_with_id.metadata["request_id"] = request_id
        
        try:
            if config.stream:
                # For streaming, collect the response
                streaming_response = await provider.generate_stream(messages, config_with_id)
                return await streaming_response.collect()
            else:
                # Non-streaming response
                return await provider.generate(messages, config_with_id)
                
        except Exception as e:
            if isinstance(e, UnifiedLLMError):
                raise
            else:
                raise UnifiedLLMError(
                    f"Unexpected error during generation: {e}",
                    provider=provider_id,
                    model=model_id
                )
    
    async def generate_stream(
        self,
        messages: Union[str, List[Message]],
        config: RequestConfig,
    ) -> StreamingResponse:
        """Generate a streaming response from an LLM.
        
        Args:
            messages: Either a string (converted to user message) or list of messages
            config: Request configuration
            
        Returns:
            Streaming response
        """
        # Convert string to messages if needed
        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]
        
        # Force streaming
        config = config.model_copy()
        config.stream = True
        
        # Validate configuration
        provider_id, model_id, model_info = self._validate_request_config(config)
        
        # Get provider
        provider = self.providers[provider_id]
        
        # Generate request ID
        request_id = str(uuid.uuid4())
        config_with_id = config.model_copy()
        config_with_id.metadata = config_with_id.metadata or {}
        config_with_id.metadata["request_id"] = request_id
        
        try:
            return await provider.generate_stream(messages, config_with_id)
        except Exception as e:
            if isinstance(e, UnifiedLLMError):
                raise
            else:
                raise UnifiedLLMError(
                    f"Unexpected error during streaming generation: {e}",
                    provider=provider_id,
                    model=model_id
                )
    
    async def close(self) -> None:
        """Close all provider connections."""
        for provider in self.providers.values():
            await provider.close()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close() 