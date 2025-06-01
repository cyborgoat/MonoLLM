#!/usr/bin/env python3
"""
MonoLLM Client - Main interface for unified LLM provider access.

This module provides the primary client interface for the MonoLLM framework,
enabling seamless access to multiple Large Language Model providers through a
single, consistent API.

Key Features:
    - Unified interface across multiple LLM providers
    - Automatic provider discovery and initialization
    - Configuration management and validation
    - Streaming and non-streaming response support
    - Error handling and retry mechanisms
    - Proxy support for network configurations

Supported Providers:
    - OpenAI (GPT models, including reasoning models)
    - Anthropic (Claude models)
    - Google (Gemini models)
    - Qwen/DashScope (Qwen models, including reasoning)
    - DeepSeek (DeepSeek models, including reasoning)
    - Volcengine (Doubao models)

Example Usage:
    Basic text generation:
        >>> import asyncio
        >>> from monollm import UnifiedLLMClient, RequestConfig
        >>> 
        >>> async def main():
        ...     async with UnifiedLLMClient() as client:
        ...         config = RequestConfig(model="qwen-plus", temperature=0.7)
        ...         response = await client.generate("Hello, world!", config)
        ...         print(response.content)
        >>> 
        >>> asyncio.run(main())

    Streaming responses:
        >>> async def stream_example():
        ...     async with UnifiedLLMClient() as client:
        ...         config = RequestConfig(model="gpt-4o", stream=True)
        ...         async for chunk in await client.generate_stream("Tell me a story", config):
        ...             if chunk.content:
        ...                 print(chunk.content, end="", flush=True)

    Multi-turn conversation:
        >>> from monollm.core.models import Message
        >>> 
        >>> async def conversation_example():
        ...     async with UnifiedLLMClient() as client:
        ...         messages = [
        ...             Message(role="system", content="You are a helpful assistant."),
        ...             Message(role="user", content="What is Python?"),
        ...         ]
        ...         config = RequestConfig(model="claude-3-sonnet")
        ...         response = await client.generate(messages, config)
        ...         print(response.content)

Author: cyborgoat
License: MIT License
Copyright: (c) 2025 cyborgoat

For more information, visit: https://github.com/cyborgoat/MonoLLM
Documentation: https://cyborgoat.github.io/MonoLLM/
"""

import uuid
from pathlib import Path
from typing import Dict, List, Optional, Union

from rich.console import Console

from monollm.config.loader import ConfigLoader
from monollm.core.exceptions import (
    ConfigurationError,
    ModelNotFoundError,
    MonoLLMError,
    ValidationError,
)
from monollm.core.models import (
    LLMResponse,
    Message,
    ModelInfo,
    ProviderInfo,
    RequestConfig,
    StreamingResponse,
)
from monollm.providers.anthropic_provider import AnthropicProvider
from monollm.providers.base import BaseProvider
from monollm.providers.deepseek_provider import DeepSeekProvider
from monollm.providers.google_provider import GoogleProvider
from monollm.providers.openai_provider import OpenAIProvider
from monollm.providers.qwen_provider import QwenProvider
from monollm.providers.volcengine_provider import VolcengineProvider


class UnifiedLLMClient:
    """
    Main client for unified access to multiple LLM providers.
    
    This class serves as the primary interface for interacting with various
    Large Language Model providers through a single, consistent API. It handles
    provider initialization, configuration management, request routing, and
    response processing.
    
    The client automatically discovers and initializes available providers based
    on configuration files and environment variables. It supports both streaming
    and non-streaming responses, handles errors gracefully, and provides detailed
    logging and progress information.
    
    Attributes:
        console (Console): Rich console for formatted output and logging
        config_loader (ConfigLoader): Configuration management system
        providers (Dict[str, BaseProvider]): Initialized provider instances
        provider_info (Dict[str, ProviderInfo]): Provider metadata and capabilities
        provider_metadata (Dict[str, Dict]): Additional provider configuration
        proxy_config (Dict): Network proxy configuration
        timeout_config (Dict): Request timeout settings
        retry_config (Dict): Retry mechanism configuration
    
    Thread Safety:
        This class is designed to be used with asyncio and is not thread-safe.
        Create separate instances for use in different threads.
    
    Resource Management:
        The client implements async context manager protocol for proper resource
        cleanup. Always use within an async context manager or call close() manually.
    """

    def __init__(
            self,
            config_dir: Optional[Path] = None,
            console: Optional[Console] = None,
    ):
        """
        Initialize the unified LLM client.
        
        Sets up the client with configuration loading, provider discovery,
        and console output. The client will automatically load configuration
        from the specified directory or use default locations.

        Args:
            config_dir (Optional[Path]): Directory containing configuration files.
                If None, uses default configuration directory (./config).
            console (Optional[Console]): Rich console instance for formatted output.
                If None, creates a new console instance.
                
        Raises:
            ConfigurationError: If configuration files cannot be loaded or are invalid.
            
        Note:
            Provider initialization happens during this call. Providers without
            valid API keys will be skipped with warnings, but the client will
            still initialize successfully.
        """
        self.console = console or Console()
        self.config_loader = ConfigLoader(config_dir)
        self.providers: Dict[str, BaseProvider] = {}
        self.provider_info: Dict[str, ProviderInfo] = {}
        self.provider_metadata: Dict[str, Dict] = {}

        # Load configuration
        self._load_configuration()

    def _load_configuration(self) -> None:
        """
        Load configuration and initialize providers.
        
        This internal method handles the complete configuration loading process,
        including provider metadata extraction, proxy settings, timeout configuration,
        and retry settings. It then triggers provider initialization.
        
        Raises:
            ConfigurationError: If configuration loading fails or configuration
                files are malformed.
        """
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
        """
        Initialize all available providers.
        
        This method attempts to initialize each configured provider by:
        1. Looking up the provider implementation class
        2. Extracting API keys and configuration from metadata
        3. Creating provider instances with proper configuration
        4. Handling initialization failures gracefully
        
        Providers that fail to initialize (e.g., missing API keys) are skipped
        with warning messages, but do not prevent other providers from working.
        
        Note:
            This method provides detailed console output about the initialization
            process, including success/failure status for each provider.
        """
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
                self.console.print(
                    f"[yellow]Warning: No implementation for provider '{provider_id}'[/yellow]"
                )
                continue

            try:
                # Get API key and configuration from metadata
                metadata = self.provider_metadata.get(provider_id, {})
                api_key = metadata.get("api_key")
                base_url_override = metadata.get("base_url_override")

                if not api_key:
                    self.console.print(
                        f"[yellow]Warning: No API key found for provider '{provider_id}'[/yellow]"
                    )
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
                self.console.print(
                    f"[green]✓[/green] Initialized provider: {provider_info.name}"
                )

            except Exception as e:
                self.console.print(
                    f"[red]✗[/red] Failed to initialize provider '{provider_id}': {e}"
                )

    def list_providers(self) -> Dict[str, ProviderInfo]:
        """
        List all available providers.
        
        Returns information about all configured providers, including both
        successfully initialized providers and those that failed to initialize.
        
        Returns:
            Dict[str, ProviderInfo]: Dictionary mapping provider IDs to their
                information objects containing name, capabilities, and model lists.
                
        Example:
            >>> client = UnifiedLLMClient()
            >>> providers = client.list_providers()
            >>> for provider_id, info in providers.items():
            ...     print(f"{provider_id}: {info.name}")
            ...     print(f"  Models: {list(info.models.keys())}")
        """
        return self.provider_info

    def list_models(
            self, provider_id: Optional[str] = None
    ) -> Dict[str, Dict[str, ModelInfo]]:
        """
        List all available models.
        
        Provides detailed information about models available across all providers
        or for a specific provider. Each model entry includes capabilities,
        limitations, and configuration options.

        Args:
            provider_id (Optional[str]): Optional provider ID to filter models.
                If None, returns models from all providers.

        Returns:
            Dict[str, Dict[str, ModelInfo]]: Nested dictionary structure where:
                - Outer keys are provider IDs
                - Inner keys are model IDs
                - Values are ModelInfo objects with model details
                
        Raises:
            ModelNotFoundError: If the specified provider_id is not found.
            
        Example:
            >>> # List all models
            >>> all_models = client.list_models()
            >>> 
            >>> # List models for specific provider
            >>> qwen_models = client.list_models("qwen")
            >>> for model_id, model_info in qwen_models["qwen"].items():
            ...     print(f"{model_id}: {model_info.name}")
        """
        if provider_id:
            if provider_id not in self.provider_info:
                raise ModelNotFoundError(
                    f"Provider '{provider_id}' not found",
                    provider=provider_id,
                    model="",
                    available_models=list(self.provider_info.keys()),
                )
            return {provider_id: self.provider_info[provider_id].models}

        return {
            provider_id: provider_info.models
            for provider_id, provider_info in self.provider_info.items()
        }

    def get_model_info(
            self, model_id: str, provider_id: Optional[str] = None
    ) -> tuple[str, ModelInfo]:
        """
        Get information about a specific model.
        
        Retrieves detailed information about a model, including its capabilities,
        limitations, and configuration options. Can search within a specific
        provider or across all providers.

        Args:
            model_id (str): Model identifier to search for.
            provider_id (Optional[str]): Optional provider ID to search within.
                If None, searches across all providers.

        Returns:
            tuple[str, ModelInfo]: Tuple containing:
                - provider_id (str): ID of the provider that owns the model
                - model_info (ModelInfo): Detailed model information object
                
        Raises:
            ModelNotFoundError: If the model is not found in the specified
                provider or across all providers.
                
        Example:
            >>> # Find model in any provider
            >>> provider_id, model_info = client.get_model_info("gpt-4o")
            >>> print(f"Found in provider: {provider_id}")
            >>> print(f"Max tokens: {model_info.max_tokens}")
            >>> 
            >>> # Find model in specific provider
            >>> provider_id, model_info = client.get_model_info("qwen-plus", "qwen")
        """
        if provider_id:
            if provider_id not in self.provider_info:
                raise ModelNotFoundError(
                    f"Provider '{provider_id}' not found",
                    provider=provider_id,
                    model=model_id,
                )

            provider_info = self.provider_info[provider_id]
            if model_id not in provider_info.models:
                raise ModelNotFoundError(
                    f"Model '{model_id}' not found in provider '{provider_id}'",
                    provider=provider_id,
                    model=model_id,
                    available_models=list(provider_info.models.keys()),
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
            available_models=all_models,
        )

    def _validate_request_config(
            self, config: RequestConfig
    ) -> tuple[str, str, ModelInfo]:
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
                value=config.temperature,
            )

        # Validate streaming setting
        if config.stream and not model_info.supports_streaming:
            raise ValidationError(
                f"Model '{config.model}' does not support streaming",
                field="stream",
                value=config.stream,
            )

        # Validate thinking steps setting
        if config.show_thinking and not model_info.supports_thinking:
            raise ValidationError(
                f"Model '{config.model}' does not support thinking steps",
                field="show_thinking",
                value=config.show_thinking,
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
                streaming_response = await provider.generate_stream(
                    messages, config_with_id
                )
                return await streaming_response.collect()
            else:
                # Non-streaming response
                return await provider.generate(messages, config_with_id)

        except Exception as e:
            if isinstance(e, MonoLLMError):
                raise
            else:
                raise MonoLLMError(
                    f"Unexpected error during generation: {e}",
                    provider=provider_id,
                    model=model_id,
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
            if isinstance(e, MonoLLMError):
                raise
            else:
                raise MonoLLMError(  # noqa: B904
                    f"Unexpected error during streaming generation: {e}",
                    provider=provider_id,
                    model=model_id,
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
