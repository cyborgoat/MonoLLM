#!/usr/bin/env python3
"""
UnifiedLLM Command-Line Interface - Interactive CLI for LLM provider access.

This module provides a comprehensive command-line interface for the UnifiedLLM
framework, enabling users to interact with multiple Large Language Model providers
through a unified set of commands. The CLI supports both interactive chat sessions
and single-shot text generation with extensive configuration options.

Key Features:
    - Interactive chat sessions with conversation history
    - Single-shot text generation with customizable parameters
    - Provider and model discovery and listing
    - Streaming and non-streaming response modes
    - Support for reasoning models with thinking steps
    - Rich terminal output with tables, panels, and markdown
    - Comprehensive error handling and user feedback
    - Configuration management through command-line options

Available Commands:
    - list-providers: Display all available LLM providers
    - list-models: Show models available for each provider
    - chat: Start an interactive chat session with a model
    - generate: Generate a single response to a prompt

Example Usage:
    List all providers:
        $ unified-llm list-providers

    List models for a specific provider:
        $ unified-llm list-models --provider qwen

    Start an interactive chat:
        $ unified-llm chat qwen-plus --temperature 0.7 --stream

    Generate a single response:
        $ unified-llm generate "Explain quantum computing" --model gpt-4o --thinking

    Use with custom configuration:
        $ unified-llm chat claude-3-sonnet --config-dir ./my-config

Advanced Features:
    - Streaming responses with real-time output
    - Reasoning model support with thinking step display
    - Conversation history management in chat mode
    - Rich formatting with syntax highlighting
    - Token usage tracking and display
    - Comprehensive error messages with suggestions

Configuration:
    The CLI respects the same configuration files as the Python API:
    - config/models.json: Model definitions and capabilities
    - Environment variables for API keys
    - Custom configuration directories via --config-dir

Author: cyborgoat
License: MIT License
Copyright: (c) 2025 cyborgoat

For more information, visit: https://github.com/cyborgoat/unified-llm
Documentation: https://cyborgoat.github.io/unified-llm/cli.html
"""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from monollm.core.client import UnifiedLLMClient
from monollm.core.exceptions import MonoLLMError, ProviderError
from monollm.core.models import RequestConfig, Message

# Initialize the main CLI application with help text
app = typer.Typer(
    help="Unified LLM Framework - Access multiple LLM providers with a single interface",
    add_completion=False,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Initialize Rich console for beautiful terminal output
console = Console()


@app.command()
def list_providers(
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path. Defaults to ./config if not specified."
    )
):
    """
    List all available LLM providers.
    
    Displays a comprehensive table showing all configured LLM providers,
    their capabilities, and connection status. This command helps users
    understand which providers are available and their features.
    
    The table includes:
    - Provider ID: Internal identifier used in commands
    - Name: Human-readable provider name
    - Base URL: API endpoint URL
    - OpenAI Protocol: Whether the provider uses OpenAI-compatible API
    - Streaming: Support for real-time streaming responses
    - MCP: Model Context Protocol support
    
    Examples:
        List all providers:
            $ unified-llm list-providers
            
        Use custom configuration directory:
            $ unified-llm list-providers --config-dir ./my-config
    """
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
    provider: Optional[str] = typer.Option(
        None, 
        "--provider", 
        "-p", 
        help="Filter models by specific provider ID. Shows all providers if not specified."
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path. Defaults to ./config if not specified."
    )
):
    """
    List all available models.
    
    Displays detailed information about models available across all providers
    or for a specific provider. Each model entry shows its capabilities,
    limitations, and supported features.
    
    The table includes:
    - Model ID: Identifier used in generation commands
    - Name: Human-readable model name
    - Max Tokens: Maximum output token limit
    - Temperature: Support for creativity/randomness control
    - Streaming: Real-time response streaming capability
    - Reasoning: Whether the model supports reasoning tasks
    - Thinking: Support for showing internal reasoning steps
    
    Examples:
        List all models:
            $ unified-llm list-models
            
        List models for specific provider:
            $ unified-llm list-models --provider qwen
            
        Use custom configuration:
            $ unified-llm list-models --provider openai --config-dir ./my-config
    """
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
    provider: Optional[str] = typer.Option(
        None, 
        "--provider", 
        "-p", 
        help="Specific provider to use. Auto-detected if not specified."
    ),
    temperature: Optional[float] = typer.Option(
        None, 
        "--temperature", 
        "-t", 
        help="Temperature for response creativity (0.0-2.0). Lower = more focused, higher = more creative."
    ),
    max_tokens: Optional[int] = typer.Option(
        None, 
        "--max-tokens", 
        "-m", 
        help="Maximum number of tokens in the response. Uses model default if not specified."
    ),
    stream: bool = typer.Option(
        False, 
        "--stream", 
        "-s", 
        help="Enable streaming responses for real-time output."
    ),
    show_thinking: bool = typer.Option(
        False, 
        "--thinking", 
        help="Show thinking steps for reasoning models (o1, qwq, deepseek-r1)."
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path. Defaults to ./config if not specified."
    ),
):
    """
    Interactive chat with an LLM model.
    
    Starts an interactive chat session with the specified model, maintaining
    conversation history and providing a rich terminal interface. The chat
    supports multiple turns, streaming responses, and special commands.
    
    Special Commands:
    - 'exit': Quit the chat session
    - 'clear': Clear conversation history
    
    Features:
    - Persistent conversation history within the session
    - Real-time streaming responses (with --stream)
    - Thinking step display for reasoning models (with --thinking)
    - Rich markdown formatting for responses
    - Token usage tracking and display
    - Comprehensive error handling with helpful messages
    
    Examples:
        Basic chat:
            $ unified-llm chat gpt-4o
            
        Chat with streaming and custom temperature:
            $ unified-llm chat qwen-plus --stream --temperature 0.8
            
        Reasoning model with thinking steps:
            $ unified-llm chat qwq-32b --thinking --max-tokens 2000
            
        Specify provider explicitly:
            $ unified-llm chat claude-3-sonnet --provider anthropic
    """
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
                except MonoLLMError as e:
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
        except MonoLLMError as e:
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