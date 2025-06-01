"""
Main CLI Entry Point for MonoLLM

Provides both user-friendly and machine-friendly command-line interfaces.
Automatically detects the interface mode and routes commands appropriately.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any

import typer
from rich.console import Console

from .user_interface import UserInterface
from .machine_interface import MachineInterface
from .config_manager import ConfigManager


# Initialize the main CLI application
app = typer.Typer(
    help="MonoLLM Framework - Access multiple LLM providers with a single interface",
    add_completion=False,
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["-h", "--help"]},
)

# Initialize Rich console for beautiful terminal output
console = Console()


@app.command()
def list_providers(
    machine: bool = typer.Option(
        False,
        "--machine",
        "-m",
        help="Output in machine-readable JSON format"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    List all available LLM providers.
    
    Shows provider information including capabilities, API endpoints,
    and supported features. Use --machine for JSON output suitable
    for programmatic consumption.
    """
    async def run():
        if machine:
            interface = MachineInterface(config_dir)
            result = await interface.list_providers()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            interface = UserInterface(config_dir, console)
            await interface.list_providers()
    
    asyncio.run(run())


@app.command()
def list_models(
    provider: Optional[str] = typer.Option(
        None, 
        "--provider", 
        "-p", 
        help="Filter models by specific provider"
    ),
    machine: bool = typer.Option(
        False,
        "--machine",
        "-m",
        help="Output in machine-readable JSON format"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    List all available models.
    
    Shows detailed model information including capabilities,
    token limits, and supported features. Filter by provider
    or show all models across providers.
    """
    async def run():
        if machine:
            interface = MachineInterface(config_dir)
            result = await interface.list_models(provider)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            interface = UserInterface(config_dir, console)
            await interface.list_models(provider)
    
    asyncio.run(run())


@app.command()
def model_config(
    model: str = typer.Argument(..., help="Model ID to show configuration for"),
    provider: Optional[str] = typer.Option(
        None, 
        "--provider", 
        "-p", 
        help="Specific provider to use"
    ),
    machine: bool = typer.Option(
        False,
        "--machine",
        "-m",
        help="Output in machine-readable JSON format"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Show detailed model configuration and capabilities.
    
    Displays comprehensive information about a specific model
    including supported parameters, limits, and current defaults.
    """
    async def run():
        if machine:
            interface = MachineInterface(config_dir)
            result = await interface.get_model_config(model, provider)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            interface = UserInterface(config_dir, console)
            await interface.show_model_config(model, provider)
    
    asyncio.run(run())


@app.command()
def set_defaults(
    model: str = typer.Argument(..., help="Model ID to set defaults for"),
    temperature: Optional[float] = typer.Option(
        None, 
        "--temperature", 
        "-t", 
        help="Default temperature (0.0-2.0)"
    ),
    max_tokens: Optional[int] = typer.Option(
        None, 
        "--max-tokens", 
        help="Default maximum output tokens"
    ),
    stream: bool = typer.Option(
        False, 
        "--stream", 
        help="Enable streaming by default"
    ),
    thinking: bool = typer.Option(
        False, 
        "--thinking", 
        help="Show thinking steps by default"
    ),
    machine: bool = typer.Option(
        False,
        "--machine",
        "-m",
        help="Output in machine-readable JSON format"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Set default parameters for a model.
    
    Configure default settings that will be used when no explicit
    parameters are provided. These defaults are stored per-model
    and persist across CLI sessions.
    """
    async def run():
        if machine:
            interface = MachineInterface(config_dir)
            result = await interface.set_model_defaults(
                model, temperature, max_tokens, stream, thinking
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            interface = UserInterface(config_dir, console)
            await interface.set_model_defaults(
                model, temperature, max_tokens, stream, thinking
            )
    
    asyncio.run(run())


@app.command()
def proxy_config(
    show: bool = typer.Option(
        False,
        "--show",
        help="Show current proxy configuration"
    ),
    http: Optional[str] = typer.Option(
        None,
        "--http",
        help="HTTP proxy URL (e.g., http://proxy:8080)"
    ),
    https: Optional[str] = typer.Option(
        None,
        "--https", 
        help="HTTPS proxy URL"
    ),
    socks: Optional[str] = typer.Option(
        None,
        "--socks",
        help="SOCKS proxy URL (e.g., socks5://proxy:1080)"
    ),
    machine: bool = typer.Option(
        False,
        "--machine",
        "-m",
        help="Output in machine-readable JSON format"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Configure proxy settings for LLM API calls.
    
    Set up HTTP, HTTPS, or SOCKS proxies for all LLM provider
    communications. Use --show to display current configuration.
    """
    async def run():
        if machine:
            interface = MachineInterface(config_dir)
            if show or not any([http, https, socks]):
                result = await interface.get_proxy_config()
            else:
                result = await interface.set_proxy_config(http, https, socks)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            interface = UserInterface(config_dir, console)
            if show or not any([http, https, socks]):
                await interface.show_proxy_config()
            else:
                await interface.set_proxy_config(http, https, socks)
    
    asyncio.run(run())


@app.command()
def generate(
    prompt: str = typer.Argument(..., help="Prompt to send to the model"),
    model: str = typer.Option(..., "--model", "-M", help="Model to use"),
    provider: Optional[str] = typer.Option(
        None, 
        "--provider", 
        "-p", 
        help="Specific provider to use"
    ),
    temperature: Optional[float] = typer.Option(
        None, 
        "--temperature", 
        "-t", 
        help="Temperature (0.0-2.0)"
    ),
    max_tokens: Optional[int] = typer.Option(
        None, 
        "--max-tokens", 
        help="Maximum output tokens"
    ),
    stream: bool = typer.Option(
        False, 
        "--stream", 
        "-s", 
        help="Enable streaming"
    ),
    thinking: bool = typer.Option(
        False, 
        "--thinking", 
        help="Show thinking steps for reasoning models"
    ),
    no_defaults: bool = typer.Option(
        False,
        "--no-defaults",
        help="Don't use saved model defaults"
    ),
    machine: bool = typer.Option(
        False,
        "--machine",
        "-m",
        help="Output in machine-readable JSON format"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Generate a single response from an LLM model.
    
    Send a prompt to the specified model and receive a response.
    Supports streaming, thinking steps, and custom parameters.
    Use saved defaults unless --no-defaults is specified.
    """
    async def run():
        if machine:
            interface = MachineInterface(config_dir)
            result = await interface.generate(
                prompt, model, provider, temperature, max_tokens,
                stream, thinking, not no_defaults
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            interface = UserInterface(config_dir, console)
            await interface.generate(
                prompt, model, provider, temperature, max_tokens,
                stream, thinking, not no_defaults
            )
    
    asyncio.run(run())


@app.command()
def generate_stream(
    prompt: str = typer.Argument(..., help="Prompt to send to the model"),
    model: str = typer.Option(..., "--model", "-M", help="Model to use"),
    provider: Optional[str] = typer.Option(
        None, 
        "--provider", 
        "-p", 
        help="Specific provider to use"
    ),
    temperature: Optional[float] = typer.Option(
        None, 
        "--temperature", 
        "-t", 
        help="Temperature (0.0-2.0)"
    ),
    max_tokens: Optional[int] = typer.Option(
        None, 
        "--max-tokens", 
        help="Maximum output tokens"
    ),
    thinking: bool = typer.Option(
        False, 
        "--thinking", 
        help="Show thinking steps for reasoning models"
    ),
    no_defaults: bool = typer.Option(
        False,
        "--no-defaults",
        help="Don't use saved model defaults"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Generate streaming response (machine interface only).
    
    Outputs JSON chunks to stdout as they arrive. Designed for
    programmatic consumption where real-time streaming is needed.
    Each line contains a JSON object representing a chunk.
    """
    async def run():
        interface = MachineInterface(config_dir)
        await interface.generate_stream(
            prompt, model, provider, temperature, max_tokens,
            thinking, not no_defaults
        )
    
    asyncio.run(run())


@app.command()
def chat(
    model: str = typer.Argument(..., help="Model to use for chat"),
    provider: Optional[str] = typer.Option(
        None, 
        "--provider", 
        "-p", 
        help="Specific provider to use"
    ),
    temperature: Optional[float] = typer.Option(
        None, 
        "--temperature", 
        "-t", 
        help="Temperature (0.0-2.0)"
    ),
    max_tokens: Optional[int] = typer.Option(
        None, 
        "--max-tokens", 
        help="Maximum output tokens"
    ),
    stream: bool = typer.Option(
        False, 
        "--stream", 
        "-s", 
        help="Enable streaming"
    ),
    thinking: bool = typer.Option(
        False, 
        "--thinking", 
        help="Show thinking steps for reasoning models"
    ),
    no_defaults: bool = typer.Option(
        False,
        "--no-defaults",
        help="Don't use saved model defaults"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Interactive chat with an LLM model.
    
    Start an interactive chat session with conversation history.
    Type 'exit' to quit or 'clear' to clear history.
    Only available in user interface mode.
    """
    async def run():
        interface = UserInterface(config_dir, console)
        await interface.chat(
            model, provider, temperature, max_tokens,
            stream, thinking, not no_defaults
        )
    
    asyncio.run(run())


@app.command()
def chat_api(
    messages_json: str = typer.Argument(..., help="JSON array of messages"),
    model: str = typer.Option(..., "--model", "-M", help="Model to use"),
    provider: Optional[str] = typer.Option(
        None, 
        "--provider", 
        "-p", 
        help="Specific provider to use"
    ),
    temperature: Optional[float] = typer.Option(
        None, 
        "--temperature", 
        "-t", 
        help="Temperature (0.0-2.0)"
    ),
    max_tokens: Optional[int] = typer.Option(
        None, 
        "--max-tokens", 
        help="Maximum output tokens"
    ),
    stream: bool = typer.Option(
        False, 
        "--stream", 
        "-s", 
        help="Enable streaming"
    ),
    thinking: bool = typer.Option(
        False, 
        "--thinking", 
        help="Show thinking steps for reasoning models"
    ),
    no_defaults: bool = typer.Option(
        False,
        "--no-defaults",
        help="Don't use saved model defaults"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Multi-turn chat API (machine interface only).
    
    Send a conversation history and receive a response.
    Messages should be JSON array: [{"role": "user", "content": "..."}]
    Always outputs JSON format suitable for programmatic use.
    """
    async def run():
        try:
            messages = json.loads(messages_json)
            interface = MachineInterface(config_dir)
            result = await interface.chat(
                messages, model, provider, temperature, max_tokens,
                stream, thinking, not no_defaults
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as e:
            error_result = {
                "error": True,
                "error_type": "JSONDecodeError",
                "error_message": f"Invalid JSON in messages: {e}",
                "timestamp": "2025-01-01T00:00:00"
            }
            print(json.dumps(error_result, indent=2, ensure_ascii=False))
            sys.exit(1)
    
    asyncio.run(run())


@app.command()
def env_info(
    machine: bool = typer.Option(
        False,
        "--machine",
        "-m",
        help="Output in machine-readable JSON format"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Show environment and configuration information.
    
    Displays API key status, configuration file locations,
    and other environment details useful for troubleshooting.
    """
    async def run():
        if machine:
            interface = MachineInterface(config_dir)
            result = await interface.get_environment_info()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            interface = UserInterface(config_dir, console)
            await interface.show_environment_info()
    
    asyncio.run(run())


@app.command()
def validate_config(
    model: str = typer.Argument(..., help="Model ID to validate configuration for"),
    temperature: Optional[float] = typer.Option(
        None, 
        "--temperature", 
        "-t", 
        help="Temperature to validate"
    ),
    max_tokens: Optional[int] = typer.Option(
        None, 
        "--max-tokens", 
        help="Max tokens to validate"
    ),
    stream: Optional[bool] = typer.Option(
        None,
        "--stream",
        help="Stream setting to validate"
    ),
    thinking: Optional[bool] = typer.Option(
        None,
        "--thinking",
        help="Thinking setting to validate"
    ),
    config_dir: Optional[Path] = typer.Option(
        None, 
        "--config-dir", 
        "-c", 
        help="Configuration directory path"
    )
):
    """
    Validate configuration parameters for a model (machine interface only).
    
    Check if the provided parameters are valid for the specified model
    and return adjusted values if needed. Useful for validating settings
    before making API calls.
    """
    async def run():
        interface = MachineInterface(config_dir)
        result = await interface.validate_config(
            model, temperature, max_tokens, stream, thinking
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    asyncio.run(run())


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main() 