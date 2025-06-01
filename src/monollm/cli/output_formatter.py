"""
Output Formatter for MonoLLM CLI

Handles formatting output for both user-friendly and machine-friendly interfaces.
Provides structured JSON output for machine consumption and rich formatting for users.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from enum import Enum

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from ..core.models import LLMResponse, StreamChunk, ModelInfo, ProviderInfo, Usage


class OutputMode(Enum):
    """Output formatting modes."""
    USER = "user"
    MACHINE = "machine"


class OutputFormatter:
    """Handles output formatting for different interface modes."""
    
    def __init__(self, mode: OutputMode = OutputMode.USER, console: Optional[Console] = None):
        self.mode = mode
        self.console = console or Console()
    
    def format_providers(self, providers: Dict[str, ProviderInfo]) -> Union[str, Dict]:
        """Format provider information."""
        if self.mode == OutputMode.MACHINE:
            return {
                "providers": {
                    provider_id: {
                        "name": info.name,
                        "base_url": info.base_url,
                        "uses_openai_protocol": info.uses_openai_protocol,
                        "supports_streaming": info.supports_streaming,
                        "supports_mcp": info.supports_mcp,
                        "model_count": len(info.models)
                    }
                    for provider_id, info in providers.items()
                },
                "total_providers": len(providers),
                "timestamp": datetime.now().isoformat()
            }
        else:
            # User-friendly table format
            table = Table(title="Available LLM Providers")
            table.add_column("Provider ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Base URL", style="blue")
            table.add_column("OpenAI Protocol", style="yellow")
            table.add_column("Streaming", style="magenta")
            table.add_column("MCP", style="red")
            
            for provider_id, provider_info in providers.items():
                table.add_row(
                    provider_id,
                    provider_info.name,
                    provider_info.base_url,
                    "✓" if provider_info.uses_openai_protocol else "✗",
                    "✓" if provider_info.supports_streaming else "✗",
                    "✓" if provider_info.supports_mcp else "✗",
                )
            
            return table
    
    def format_models(self, models: Dict[str, Dict[str, ModelInfo]], provider_filter: Optional[str] = None) -> Union[str, Dict]:
        """Format model information."""
        if self.mode == OutputMode.MACHINE:
            result = {
                "models": {},
                "total_models": 0,
                "timestamp": datetime.now().isoformat()
            }
            
            for provider_id, provider_models in models.items():
                if provider_filter and provider_id != provider_filter:
                    continue
                    
                result["models"][provider_id] = {
                    model_id: {
                        "name": model_info.name,
                        "max_tokens": model_info.max_tokens,
                        "supports_temperature": model_info.supports_temperature,
                        "supports_streaming": model_info.supports_streaming,
                        "supports_thinking": model_info.supports_thinking,
                        "stream_only": getattr(model_info, 'stream_only', False)
                    }
                    for model_id, model_info in provider_models.items()
                }
                result["total_models"] += len(provider_models)
            
            return result
        else:
            # User-friendly table format
            tables = []
            for provider_id, provider_models in models.items():
                if provider_filter and provider_id != provider_filter:
                    continue
                    
                table = Table(title=f"Models for {provider_id}")
                table.add_column("Model ID", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Max Tokens", style="blue")
                table.add_column("Temperature", style="yellow")
                table.add_column("Streaming", style="magenta")
                table.add_column("Thinking", style="bright_red")
                table.add_column("Stream Only", style="orange1")
                
                for model_id, model_info in provider_models.items():
                    table.add_row(
                        model_id,
                        model_info.name,
                        str(model_info.max_tokens),
                        "✓" if model_info.supports_temperature else "✗",
                        "✓" if model_info.supports_streaming else "✗",
                        "✓" if model_info.supports_thinking else "✗",
                        "✓" if getattr(model_info, 'stream_only', False) else "✗",
                    )
                
                tables.append(table)
            
            return tables
    
    def format_model_config(self, model_id: str, model_info: ModelInfo, provider_id: str) -> Union[str, Dict]:
        """Format model configuration details."""
        if self.mode == OutputMode.MACHINE:
            return {
                "model_id": model_id,
                "provider_id": provider_id,
                "configuration": {
                    "name": model_info.name,
                    "max_tokens": model_info.max_tokens,
                    "supports_temperature": model_info.supports_temperature,
                    "supports_streaming": model_info.supports_streaming,
                    "supports_thinking": model_info.supports_thinking,
                    "stream_only": getattr(model_info, 'stream_only', False),
                    "default_temperature": 0.7 if model_info.supports_temperature else None,
                    "temperature_range": [0.0, 2.0] if model_info.supports_temperature else None
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            # User-friendly panel format
            config_text = f"""
**Model ID**: {model_id}
**Provider**: {provider_id}
**Name**: {model_info.name}
**Max Tokens**: {model_info.max_tokens:,}
**Temperature Support**: {'Yes' if model_info.supports_temperature else 'No'}
**Streaming Support**: {'Yes' if model_info.supports_streaming else 'No'}
**Thinking Support**: {'Yes' if model_info.supports_thinking else 'No'}
**Stream Only**: {'Yes' if getattr(model_info, 'stream_only', False) else 'No'}
"""
            if model_info.supports_temperature:
                config_text += "**Temperature Range**: 0.0 - 2.0\n**Default Temperature**: 0.7"
            
            return Panel(config_text.strip(), title="Model Configuration")
    
    def format_generation_response(self, response: LLMResponse, show_thinking: bool = False) -> Union[str, Dict]:
        """Format generation response."""
        if self.mode == OutputMode.MACHINE:
            result = {
                "content": response.content,
                "model": response.model,
                "provider": response.provider,
                "timestamp": response.created_at.isoformat() if response.created_at else None,
                "request_id": response.request_id
            }
            
            if response.thinking and show_thinking:
                result["thinking"] = response.thinking
            
            if response.usage:
                result["usage"] = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                    "reasoning_tokens": response.usage.reasoning_tokens
                }
            
            if response.metadata:
                result["metadata"] = response.metadata
            
            return result
        else:
            # User-friendly format
            if response.thinking and show_thinking:
                self.console.print(f"[dim]💭 Thinking:\n{response.thinking}[/dim]\n")
            
            self.console.print(Markdown(response.content))
            
            if response.usage:
                self.console.print(f"\n[dim]Tokens: {response.usage.prompt_tokens} + {response.usage.completion_tokens} = {response.usage.total_tokens}[/dim]")
            
            return ""
    
    def format_stream_chunk(self, chunk: StreamChunk, show_thinking: bool = False) -> Union[str, Dict]:
        """Format streaming chunk."""
        if self.mode == OutputMode.MACHINE:
            result = {
                "type": "chunk",
                "is_complete": chunk.is_complete,
                "timestamp": datetime.now().isoformat()
            }
            
            if chunk.content:
                result["content"] = chunk.content
            
            if chunk.thinking and show_thinking:
                result["thinking"] = chunk.thinking
            
            if chunk.metadata:
                result["metadata"] = chunk.metadata
            
            return result
        else:
            # User-friendly streaming output
            output = ""
            if chunk.content:
                output += chunk.content
            
            if chunk.thinking and show_thinking:
                output += f"\n[dim]💭 {chunk.thinking}[/dim]"
            
            return output
    
    def format_error(self, error: Exception, context: Optional[str] = None) -> Union[str, Dict]:
        """Format error information."""
        if self.mode == OutputMode.MACHINE:
            result = {
                "error": True,
                "error_type": type(error).__name__,
                "error_message": str(error),
                "timestamp": datetime.now().isoformat()
            }
            
            if context:
                result["context"] = context
            
            if hasattr(error, 'status_code'):
                result["status_code"] = error.status_code
            
            return result
        else:
            # User-friendly error display
            error_text = f"[red]Error: {error}[/red]"
            if hasattr(error, 'status_code') and error.status_code:
                error_text += f"\n[red]Status: {error.status_code}[/red]"
            if context:
                error_text += f"\n[dim]Context: {context}[/dim]"
            
            return error_text
    
    def format_proxy_config(self, proxy_config: Optional[Dict[str, Any]]) -> Union[str, Dict]:
        """Format proxy configuration."""
        if self.mode == OutputMode.MACHINE:
            return {
                "proxy_config": proxy_config,
                "timestamp": datetime.now().isoformat()
            }
        else:
            if proxy_config:
                config_text = f"""
**HTTP Proxy**: {proxy_config.get('http', 'Not configured')}
**HTTPS Proxy**: {proxy_config.get('https', 'Not configured')}
**SOCKS Proxy**: {proxy_config.get('socks', 'Not configured')}
"""
                return Panel(config_text.strip(), title="Proxy Configuration")
            else:
                return Panel("No proxy configuration", title="Proxy Configuration")
    
    def output(self, data: Any) -> None:
        """Output data in the appropriate format."""
        if self.mode == OutputMode.MACHINE:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            if isinstance(data, (Table, Panel)):
                self.console.print(data)
            elif isinstance(data, list):
                for item in data:
                    self.console.print(item)
                    self.console.print()
            else:
                self.console.print(data) 