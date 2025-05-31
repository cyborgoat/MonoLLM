"""Command-line interface for the unified LLM framework."""

import asyncio
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

from .core.client import UnifiedLLMClient
from .core.models import RequestConfig, Message
from .core.exceptions import UnifiedLLMError, ProviderError

app = typer.Typer(help="Unified LLM Framework - Access multiple LLM providers with a single interface")
console = Console()


@app.command()
def list_providers(
    config_dir: Optional[Path] = typer.Option(None, "--config-dir", "-c", help="Configuration directory")
):
    """List all available LLM providers."""
    try:
        client = UnifiedLLMClient(config_dir=config_dir, console=console)
        providers = client.list_providers()
        
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
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def list_models(
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="Filter by provider"),
    config_dir: Optional[Path] = typer.Option(None, "--config-dir", "-c", help="Configuration directory")
):
    """List all available models."""
    try:
        client = UnifiedLLMClient(config_dir=config_dir, console=console)
        models = client.list_models(provider_id=provider)
        
        for provider_id, provider_models in models.items():
            provider_info = client.list_providers()[provider_id]
            
            table = Table(title=f"Models for {provider_info.name}")
            table.add_column("Model ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Max Tokens", style="blue")
            table.add_column("Temperature", style="yellow")
            table.add_column("Streaming", style="magenta")
            table.add_column("Reasoning", style="red")
            table.add_column("Thinking", style="bright_red")
            
            for model_id, model_info in provider_models.items():
                table.add_row(
                    model_id,
                    model_info.name,
                    str(model_info.max_tokens),
                    "✓" if model_info.supports_temperature else "✗",
                    "✓" if model_info.supports_streaming else "✗",
                    "✓" if model_info.is_reasoning_model else "✗",
                    "✓" if model_info.supports_thinking else "✗",
                )
            
            console.print(table)
            console.print()
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def chat(
    model: str = typer.Argument(..., help="Model to use (e.g., gpt-4o, claude-3-5-sonnet-20241022)"),
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="Specific provider to use"),
    temperature: Optional[float] = typer.Option(None, "--temperature", "-t", help="Temperature (0.0-2.0)"),
    max_tokens: Optional[int] = typer.Option(None, "--max-tokens", "-m", help="Maximum output tokens"),
    stream: bool = typer.Option(False, "--stream", "-s", help="Enable streaming"),
    show_thinking: bool = typer.Option(False, "--thinking", help="Show thinking steps for reasoning models"),
    config_dir: Optional[Path] = typer.Option(None, "--config-dir", "-c", help="Configuration directory"),
):
    """Interactive chat with an LLM model."""
    async def async_chat():
        try:
            client = UnifiedLLMClient(config_dir=config_dir, console=console)
            
            # Get model info
            provider_id, model_info = client.get_model_info(model, provider)
            
            console.print(Panel(
                f"[green]Connected to {model_info.name}[/green]\n"
                f"Provider: {client.list_providers()[provider_id].name}\n"
                f"Max tokens: {model_info.max_tokens:,}\n"
                f"Reasoning model: {'Yes' if model_info.is_reasoning_model else 'No'}\n"
                f"Supports thinking: {'Yes' if model_info.supports_thinking else 'No'}",
                title="Model Info"
            ))
            
            console.print("[dim]Type 'exit' to quit, 'clear' to clear history[/dim]")
            
            messages = []
            
            while True:
                # Get user input
                user_input = typer.prompt("\n🧑 You")
                
                if user_input.lower() == "exit":
                    break
                elif user_input.lower() == "clear":
                    messages = []
                    console.print("[dim]Chat history cleared[/dim]")
                    continue
                
                # Add user message
                messages.append(Message(role="user", content=user_input))
                
                # Create request config
                config = RequestConfig(
                    model=model,
                    provider=provider,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=stream,
                    show_thinking=show_thinking,
                )
                
                try:
                    if stream:
                        # Streaming response
                        console.print("\n🤖 Assistant:", end="")
                        
                        streaming_response = await client.generate_stream(messages, config)
                        content_parts = []
                        thinking_parts = []
                        
                        async for chunk in streaming_response:
                            if chunk.content:
                                console.print(chunk.content, end="")
                                content_parts.append(chunk.content)
                            
                            if chunk.thinking and show_thinking:
                                console.print(f"\n[dim]💭 {chunk.thinking}[/dim]", end="")
                                thinking_parts.append(chunk.thinking)
                        
                        console.print()  # New line after streaming
                        
                        # Add assistant message to history
                        assistant_content = "".join(content_parts)
                        messages.append(Message(role="assistant", content=assistant_content))
                        
                    else:
                        # Non-streaming response
                        with console.status("[bold green]Generating response..."):
                            response = await client.generate(messages, config)
                        
                        # Show thinking if available
                        if response.thinking and show_thinking:
                            console.print(f"\n[dim]💭 Thinking:\n{response.thinking}[/dim]\n")
                        
                        # Show response
                        console.print(f"\n🤖 Assistant:")
                        console.print(Markdown(response.content))
                        
                        # Show usage info
                        if response.usage:
                            console.print(f"\n[dim]Tokens: {response.usage.prompt_tokens} + {response.usage.completion_tokens} = {response.usage.total_tokens}[/dim]")
                        
                        # Add assistant message to history
                        messages.append(Message(role="assistant", content=response.content))
                
                except ProviderError as e:
                    console.print(f"\n[red]Provider Error: {e.message}[/red]")
                    if hasattr(e, 'status_code') and e.status_code:
                        console.print(f"[red]Status: {e.status_code}[/red]")
                except UnifiedLLMError as e:
                    console.print(f"\n[red]Error: {e.message}[/red]")
                except Exception as e:
                    console.print(f"\n[red]Unexpected error: {e}[/red]")
        
        except Exception as e:
            console.print(f"[red]Failed to initialize client: {e}[/red]")
            raise typer.Exit(1)
    
    asyncio.run(async_chat())


@app.command()
def generate(
    prompt: str = typer.Argument(..., help="Prompt to send to the model"),
    model: str = typer.Option(..., "--model", "-m", help="Model to use"),
    provider: Optional[str] = typer.Option(None, "--provider", "-p", help="Specific provider to use"),
    temperature: Optional[float] = typer.Option(None, "--temperature", "-t", help="Temperature (0.0-2.0)"),
    max_tokens: Optional[int] = typer.Option(None, "--max-tokens", help="Maximum output tokens"),
    stream: bool = typer.Option(False, "--stream", "-s", help="Enable streaming"),
    show_thinking: bool = typer.Option(False, "--thinking", help="Show thinking steps for reasoning models"),
    config_dir: Optional[Path] = typer.Option(None, "--config-dir", "-c", help="Configuration directory"),
):
    """Generate a single response from an LLM model."""
    async def async_generate():
        try:
            client = UnifiedLLMClient(config_dir=config_dir, console=console)
            
            config = RequestConfig(
                model=model,
                provider=provider,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
                show_thinking=show_thinking,
            )
            
            if stream:
                # Streaming response
                streaming_response = await client.generate_stream(prompt, config)
                
                async for chunk in streaming_response:
                    if chunk.content:
                        console.print(chunk.content, end="")
                    
                    if chunk.thinking and show_thinking:
                        console.print(f"\n[dim]💭 {chunk.thinking}[/dim]")
                
                console.print()  # New line after streaming
            
            else:
                # Non-streaming response
                with console.status("[bold green]Generating response..."):
                    response = await client.generate(prompt, config)
                
                # Show thinking if available
                if response.thinking and show_thinking:
                    console.print(f"[dim]💭 Thinking:\n{response.thinking}[/dim]\n")
                
                # Show response
                console.print(Markdown(response.content))
                
                # Show usage info
                if response.usage:
                    console.print(f"\n[dim]Tokens: {response.usage.prompt_tokens} + {response.usage.completion_tokens} = {response.usage.total_tokens}[/dim]")
        
        except ProviderError as e:
            console.print(f"[red]Provider Error: {e.message}[/red]")
            if hasattr(e, 'status_code') and e.status_code:
                console.print(f"[red]Status: {e.status_code}[/red]")
            raise typer.Exit(1)
        except UnifiedLLMError as e:
            console.print(f"[red]Error: {e.message}[/red]")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Unexpected error: {e}[/red]")
            raise typer.Exit(1)
    
    asyncio.run(async_generate())


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main() 