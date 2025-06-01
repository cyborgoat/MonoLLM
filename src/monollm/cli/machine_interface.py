"""
Machine Interface for MonoLLM CLI

Provides a JSON-based API interface for programmatic usage, designed for
integration with external applications like Tauri sidecars. All output is
structured JSON for easy parsing.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config_manager import ConfigManager, ModelDefaults, ProxyConfig
from .output_formatter import OutputFormatter, OutputMode
from ..core.client import UnifiedLLMClient
from ..core.exceptions import MonoLLMError, ProviderError
from ..core.models import Message


class MachineInterface:
    """Machine-friendly JSON API interface."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_manager = ConfigManager(config_dir)
        self.formatter = OutputFormatter(OutputMode.MACHINE)
    
    async def list_providers(self) -> Dict[str, Any]:
        """List all available providers."""
        try:
            providers = self.config_manager.list_providers()
            return self.formatter.format_providers(providers)
        except Exception as e:
            return self.formatter.format_error(e, "list_providers")
    
    async def list_models(self, provider_id: Optional[str] = None) -> Dict[str, Any]:
        """List all available models."""
        try:
            models = self.config_manager.list_models(provider_id)
            return self.formatter.format_models(models, provider_id)
        except Exception as e:
            return self.formatter.format_error(e, "list_models")
    
    async def get_model_config(self, model_id: str, provider_id: Optional[str] = None) -> Dict[str, Any]:
        """Get detailed model configuration."""
        try:
            provider_id, model_info = self.config_manager.get_model_info(model_id, provider_id)
            return self.formatter.format_model_config(model_id, model_info, provider_id)
        except Exception as e:
            return self.formatter.format_error(e, "get_model_config")
    
    async def get_model_defaults(self, model_id: str) -> Dict[str, Any]:
        """Get default settings for a model."""
        try:
            defaults = self.config_manager.get_model_defaults(model_id)
            return {
                "model_id": model_id,
                "defaults": defaults.to_dict(),
                "timestamp": self.formatter.format_providers({})["timestamp"]
            }
        except Exception as e:
            return self.formatter.format_error(e, "get_model_defaults")
    
    async def set_model_defaults(
        self,
        model_id: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: Optional[bool] = None,
        show_thinking: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Set default settings for a model."""
        try:
            defaults = ModelDefaults(
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream or False,
                show_thinking=show_thinking or False
            )
            
            self.config_manager.set_model_defaults(model_id, defaults)
            
            return {
                "success": True,
                "model_id": model_id,
                "defaults_set": defaults.to_dict(),
                "timestamp": self.formatter.format_providers({})["timestamp"]
            }
        except Exception as e:
            return self.formatter.format_error(e, "set_model_defaults")
    
    async def get_proxy_config(self) -> Dict[str, Any]:
        """Get proxy configuration."""
        try:
            proxy_config = self.config_manager.get_proxy_config()
            return self.formatter.format_proxy_config(proxy_config.to_dict())
        except Exception as e:
            return self.formatter.format_error(e, "get_proxy_config")
    
    async def set_proxy_config(
        self,
        http: Optional[str] = None,
        https: Optional[str] = None,
        socks: Optional[str] = None
    ) -> Dict[str, Any]:
        """Set proxy configuration."""
        try:
            proxy_config = ProxyConfig(http=http, https=https, socks=socks)
            self.config_manager.set_proxy_config(proxy_config)
            
            return {
                "success": True,
                "proxy_config": proxy_config.to_dict(),
                "timestamp": self.formatter.format_providers({})["timestamp"]
            }
        except Exception as e:
            return self.formatter.format_error(e, "set_proxy_config")
    
    async def validate_config(
        self,
        model_id: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: Optional[bool] = None,
        show_thinking: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Validate configuration for a model."""
        try:
            config = {
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream,
                "show_thinking": show_thinking
            }
            
            validated_config = self.config_manager.validate_model_config(model_id, config)
            
            return {
                "model_id": model_id,
                "original_config": config,
                "validated_config": validated_config,
                "changes_made": config != validated_config,
                "timestamp": self.formatter.format_providers({})["timestamp"]
            }
        except Exception as e:
            return self.formatter.format_error(e, "validate_config")
    
    async def generate(
        self,
        prompt: str,
        model: str,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        show_thinking: bool = False,
        use_defaults: bool = True
    ) -> Dict[str, Any]:
        """Generate a response from the model."""
        try:
            config = self.config_manager.create_request_config(
                model=model,
                provider=provider,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                show_thinking=show_thinking,
                use_defaults=use_defaults
            )
            
            async with UnifiedLLMClient(config_dir=self.config_manager.config_dir) as client:
                if stream:
                    # For machine interface, collect all chunks and return complete response
                    chunks = []
                    content_parts = []
                    thinking_parts = []
                    
                    streaming_response = await client.generate_stream(prompt, config)
                    async for chunk in streaming_response:
                        chunk_data = self.formatter.format_stream_chunk(chunk, show_thinking)
                        chunks.append(chunk_data)
                        
                        if chunk.content:
                            content_parts.append(chunk.content)
                        if chunk.thinking and show_thinking:
                            thinking_parts.append(chunk.thinking)
                        
                        if chunk.is_complete:
                            break
                    
                    # Return complete response with chunks
                    result = {
                        "content": "".join(content_parts),
                        "thinking": "".join(thinking_parts) if thinking_parts else None,
                        "model": model,
                        "provider": provider,
                        "stream": True,
                        "chunks": chunks,
                        "timestamp": self.formatter.format_providers({})["timestamp"]
                    }
                    
                    return result
                else:
                    response = await client.generate(prompt, config)
                    return self.formatter.format_generation_response(response, show_thinking)
                    
        except Exception as e:
            return self.formatter.format_error(e, "generate")
    
    async def generate_stream(
        self,
        prompt: str,
        model: str,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        show_thinking: bool = False,
        use_defaults: bool = True
    ) -> None:
        """Generate streaming response (outputs JSON chunks to stdout)."""
        try:
            config = self.config_manager.create_request_config(
                model=model,
                provider=provider,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                show_thinking=show_thinking,
                use_defaults=use_defaults
            )
            
            async with UnifiedLLMClient(config_dir=self.config_manager.config_dir) as client:
                streaming_response = await client.generate_stream(prompt, config)
                
                async for chunk in streaming_response:
                    chunk_data = self.formatter.format_stream_chunk(chunk, show_thinking)
                    print(json.dumps(chunk_data, ensure_ascii=False))
                    
                    if chunk.is_complete:
                        break
                        
        except Exception as e:
            error_data = self.formatter.format_error(e, "generate_stream")
            print(json.dumps(error_data, ensure_ascii=False))
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        show_thinking: bool = False,
        use_defaults: bool = True
    ) -> Dict[str, Any]:
        """Multi-turn chat conversation."""
        try:
            # Convert dict messages to Message objects
            message_objects = [
                Message(role=msg["role"], content=msg["content"])
                for msg in messages
            ]
            
            config = self.config_manager.create_request_config(
                model=model,
                provider=provider,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                show_thinking=show_thinking,
                use_defaults=use_defaults
            )
            
            async with UnifiedLLMClient(config_dir=self.config_manager.config_dir) as client:
                if stream:
                    # Collect streaming response
                    chunks = []
                    content_parts = []
                    thinking_parts = []
                    
                    streaming_response = await client.generate_stream(message_objects, config)
                    async for chunk in streaming_response:
                        chunk_data = self.formatter.format_stream_chunk(chunk, show_thinking)
                        chunks.append(chunk_data)
                        
                        if chunk.content:
                            content_parts.append(chunk.content)
                        if chunk.thinking and show_thinking:
                            thinking_parts.append(chunk.thinking)
                        
                        if chunk.is_complete:
                            break
                    
                    result = {
                        "content": "".join(content_parts),
                        "thinking": "".join(thinking_parts) if thinking_parts else None,
                        "model": model,
                        "provider": provider,
                        "stream": True,
                        "chunks": chunks,
                        "conversation_length": len(messages) + 1,
                        "timestamp": self.formatter.format_providers({})["timestamp"]
                    }
                    
                    return result
                else:
                    response = await client.generate(message_objects, config)
                    result = self.formatter.format_generation_response(response, show_thinking)
                    result["conversation_length"] = len(messages) + 1
                    return result
                    
        except Exception as e:
            return self.formatter.format_error(e, "chat")
    
    async def get_environment_info(self) -> Dict[str, Any]:
        """Get environment and configuration information."""
        try:
            return self.config_manager.get_environment_info()
        except Exception as e:
            return self.formatter.format_error(e, "get_environment_info")
    
    async def export_config(self) -> Dict[str, Any]:
        """Export all configuration."""
        try:
            return self.config_manager.export_config()
        except Exception as e:
            return self.formatter.format_error(e, "export_config")
    
    async def import_config(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Import configuration."""
        try:
            self.config_manager.import_config(config_data)
            return {
                "success": True,
                "message": "Configuration imported successfully",
                "timestamp": self.formatter.format_providers({})["timestamp"]
            }
        except Exception as e:
            return self.formatter.format_error(e, "import_config")
    
    async def reset_defaults(self, model_id: Optional[str] = None) -> Dict[str, Any]:
        """Reset model defaults."""
        try:
            self.config_manager.reset_model_defaults(model_id)
            return {
                "success": True,
                "message": f"Defaults reset for {'all models' if not model_id else model_id}",
                "timestamp": self.formatter.format_providers({})["timestamp"]
            }
        except Exception as e:
            return self.formatter.format_error(e, "reset_defaults") 