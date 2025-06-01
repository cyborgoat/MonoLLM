"""
User Interface for MonoLLM CLI

Provides a rich, user-friendly command-line interface with beautiful formatting,
interactive features, and comprehensive help. This is the human-facing interface
with tables, panels, and rich terminal output.
"""

import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .config_manager import ConfigManager, ModelDefaults, ProxyConfig
from .output_formatter import OutputFormatter, OutputMode
from ..core.client import UnifiedLLMClient
from ..core.exceptions import MonoLLMError, ProviderError
from ..core.models import RequestConfig, Message


class UserInterface:
    """User-friendly CLI interface with rich formatting."""
    
    def __init__(self, config_dir: Optional[Path] = None, console: Optional[Console] = None):
        self.config_manager = ConfigManager(config_dir)
        self.console = console or Console()
        self.formatter = OutputFormatter(OutputMode.USER, self.console)
    
    async def list_providers(self) -> None:
        """List all available providers with rich formatting."""
        try:
            providers = self.config_manager.list_providers()
            table = self.formatter.format_providers(providers)
            self.formatter.output(table)
        except Exception as e:
            error_output = self.formatter.format_error(e, "list_providers")
            self.console.print(error_output)
    
    async def list_models(self, provider_id: Optional[str] = None) -> None:
        """List all available models with rich formatting."""
        try:
            models = self.config_manager.list_models(provider_id)
            tables = self.formatter.format_models(models, provider_id)
            self.formatter.output(tables)
        except Exception as e:
            error_output = self.formatter.format_error(e, "list_models")
            self.console.print(error_output)
    
    async def show_model_config(self, model_id: str, provider_id: Optional[str] = None) -> None:
        """Show detailed model configuration."""
        try:
            provider_id, model_info = self.config_manager.get_model_info(model_id, provider_id)
            panel = self.formatter.format_model_config(model_id, model_info, provider_id)
            self.formatter.output(panel)
            
            # Also show current defaults
            defaults = self.config_manager.get_model_defaults(model_id)
            if any([defaults.temperature, defaults.max_tokens, defaults.stream, defaults.show_thinking]):
                defaults_text = f"""
**Temperature**: {defaults.temperature if defaults.temperature is not None else 'Not set'}
**Max Tokens**: {defaults.max_tokens if defaults.max_tokens is not None else 'Not set'}
**Stream**: {'Yes' if defaults.stream else 'No'}
**Show Thinking**: {'Yes' if defaults.show_thinking else 'No'}
"""
                defaults_panel = Panel(defaults_text.strip(), title="Current User Defaults")
                self.formatter.output(defaults_panel)
            
        except Exception as e:
            error_output = self.formatter.format_error(e, "show_model_config")
            self.console.print(error_output)
    
    async def set_model_defaults(
        self,
        model_id: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: Optional[bool] = None,
        show_thinking: Optional[bool] = None
    ) -> None:
        """Set default settings for a model."""
        try:
            defaults = ModelDefaults(
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream or False,
                show_thinking=show_thinking or False
            )
            
            self.config_manager.set_model_defaults(model_id, defaults)
            
            success_text = f"""
**Model**: {model_id}
**Temperature**: {temperature if temperature is not None else 'Not changed'}
**Max Tokens**: {max_tokens if max_tokens is not None else 'Not changed'}
**Stream**: {'Yes' if stream else 'No' if stream is not None else 'Not changed'}
**Show Thinking**: {'Yes' if show_thinking else 'No' if show_thinking is not None else 'Not changed'}
"""
            success_panel = Panel(success_text.strip(), title="✅ Defaults Updated", style="green")
            self.formatter.output(success_panel)
            
        except Exception as e:
            error_output = self.formatter.format_error(e, "set_model_defaults")
            self.console.print(error_output)
    
    async def show_proxy_config(self) -> None:
        """Show current proxy configuration."""
        try:
            proxy_config = self.config_manager.get_proxy_config()
            panel = self.formatter.format_proxy_config(proxy_config.to_dict())
            self.formatter.output(panel)
        except Exception as e:
            error_output = self.formatter.format_error(e, "show_proxy_config")
            self.console.print(error_output)
    
    async def set_proxy_config(
        self,
        http: Optional[str] = None,
        https: Optional[str] = None,
        socks: Optional[str] = None
    ) -> None:
        """Set proxy configuration."""
        try:
            proxy_config = ProxyConfig(http=http, https=https, socks=socks)
            self.config_manager.set_proxy_config(proxy_config)
            
            success_text = f"""
**HTTP Proxy**: {http or 'Not set'}
**HTTPS Proxy**: {https or 'Not set'}
**SOCKS Proxy**: {socks or 'Not set'}
"""
            success_panel = Panel(success_text.strip(), title="✅ Proxy Configuration Updated", style="green")
            self.formatter.output(success_panel)
            
        except Exception as e:
            error_output = self.formatter.format_error(e, "set_proxy_config")
            self.console.print(error_output)
    
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
    ) -> None:
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
            
            async with UnifiedLLMClient(config_dir=self.config_manager.config_dir, console=self.console) as client:
                if stream:
                    # Streaming response
                    self.console.print(f"\n🤖 {model}:", end="")
                    
                    streaming_response = await client.generate_stream(prompt, config)
                    async for chunk in streaming_response:
                        if chunk.content:
                            self.console.print(chunk.content, end="")
                        
                        if chunk.thinking and show_thinking:
                            self.console.print(f"\n[dim]💭 {chunk.thinking}[/dim]", end="")
                        
                        if chunk.is_complete:
                            break
                    
                    self.console.print()  # New line after streaming
                else:
                    # Non-streaming response
                    with self.console.status("[bold green]Generating response..."):
                        response = await client.generate(prompt, config)
                    
                    self.formatter.format_generation_response(response, show_thinking)
                    
        except ProviderError as e:
            self.console.print(f"[red]Provider Error: {e.message}[/red]")
            if hasattr(e, 'status_code') and e.status_code:
                self.console.print(f"[red]Status: {e.status_code}[/red]")
        except MonoLLMError as e:
            self.console.print(f"[red]Error: {e.message}[/red]")
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {e}[/red]")
    
    async def chat(
        self,
        model: str,
        provider: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        show_thinking: bool = False,
        use_defaults: bool = True
    ) -> None:
        """Interactive chat with an LLM model."""
        try:
            async with UnifiedLLMClient(config_dir=self.config_manager.config_dir, console=self.console) as client:
                # Get model info
                provider_id, model_info = client.get_model_info(model, provider)
                
                self.console.print(Panel(
                    f"[green]Connected to {model_info.name}[/green]\n"
                    f"Provider: {client.list_providers()[provider_id].name}\n"
                    f"Max tokens: {model_info.max_tokens:,}\n"
                    f"Supports thinking: {'Yes' if model_info.supports_thinking else 'No'}",
                    title="Model Info"
                ))
                
                self.console.print("[dim]Type 'exit' to quit, 'clear' to clear history[/dim]")
                
                messages = []
                
                while True:
                    # Get user input
                    try:
                        user_input = input("\n🧑 You: ")
                    except (EOFError, KeyboardInterrupt):
                        break
                    
                    if user_input.lower() == "exit":
                        break
                    elif user_input.lower() == "clear":
                        messages = []
                        self.console.print("[dim]Chat history cleared[/dim]")
                        continue
                    
                    # Add user message
                    messages.append(Message(role="user", content=user_input))
                    
                    # Create request config
                    config = self.config_manager.create_request_config(
                        model=model,
                        provider=provider,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        stream=stream,
                        show_thinking=show_thinking,
                        use_defaults=use_defaults
                    )
                    
                    try:
                        if stream:
                            # Streaming response
                            self.console.print("\n🤖 Assistant:", end="")
                            
                            streaming_response = await client.generate_stream(messages, config)
                            content_parts = []
                            thinking_parts = []
                            
                            async for chunk in streaming_response:
                                if chunk.content:
                                    self.console.print(chunk.content, end="")
                                    content_parts.append(chunk.content)
                                
                                if chunk.thinking and show_thinking:
                                    self.console.print(f"\n[dim]💭 {chunk.thinking}[/dim]", end="")
                                    thinking_parts.append(chunk.thinking)
                            
                            self.console.print()  # New line after streaming
                            
                            # Add assistant message to history
                            assistant_content = "".join(content_parts)
                            messages.append(Message(role="assistant", content=assistant_content))
                            
                        else:
                            # Non-streaming response
                            with self.console.status("[bold green]Generating response..."):
                                response = await client.generate(messages, config)
                            
                            # Show thinking if available
                            if response.thinking and show_thinking:
                                self.console.print(f"\n[dim]💭 Thinking:\n{response.thinking}[/dim]\n")
                            
                            # Show response
                            self.console.print(f"\n🤖 Assistant:")
                            self.console.print(Markdown(response.content))
                            
                            # Show usage info
                            if response.usage:
                                self.console.print(f"\n[dim]Tokens: {response.usage.prompt_tokens} + {response.usage.completion_tokens} = {response.usage.total_tokens}[/dim]")
                            
                            # Add assistant message to history
                            messages.append(Message(role="assistant", content=response.content))
                    
                    except ProviderError as e:
                        self.console.print(f"\n[red]Provider Error: {e.message}[/red]")
                        if hasattr(e, 'status_code') and e.status_code:
                            self.console.print(f"[red]Status: {e.status_code}[/red]")
                    except MonoLLMError as e:
                        self.console.print(f"\n[red]Error: {e.message}[/red]")
                    except Exception as e:
                        self.console.print(f"\n[red]Unexpected error: {e}[/red]")
        
        except Exception as e:
            self.console.print(f"[red]Failed to initialize client: {e}[/red]")
    
    async def show_environment_info(self) -> None:
        """Show environment and configuration information."""
        try:
            env_info = self.config_manager.get_environment_info()
            
            # API Keys status
            api_status_text = ""
            for provider, has_key in env_info["api_key_status"].items():
                status = "✅ Configured" if has_key else "❌ Missing"
                api_status_text += f"**{provider.title()}**: {status}\n"
            
            api_panel = Panel(api_status_text.strip(), title="API Keys Status")
            
            # Environment info
            env_text = f"""
**Config Directory**: {env_info['config_dir']}
**User Config**: {'✅ Exists' if env_info['user_config_exists'] else '❌ Not found'}
**Proxy Config**: {'✅ Exists' if env_info['proxy_config_exists'] else '❌ Not found'}
**Python Version**: {env_info['python_version']}
"""
            env_panel = Panel(env_text.strip(), title="Environment Information")
            
            self.formatter.output([api_panel, env_panel])
            
        except Exception as e:
            error_output = self.formatter.format_error(e, "show_environment_info")
            self.console.print(error_output) 