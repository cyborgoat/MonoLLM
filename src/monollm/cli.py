#!/usr/bin/env python3
"""
MonoLLM Command-Line Interface - Interactive CLI for LLM provider access.

This module provides a comprehensive command-line interface for the MonoLLM
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
    - Machine-friendly JSON API for programmatic usage
    - Proxy configuration and model defaults management

Available Commands:
    - list-providers: Display all available LLM providers
    - list-models: Show models available for each provider
    - model-config: Show detailed model configuration
    - set-defaults: Set default parameters for models
    - proxy-config: Configure proxy settings
    - generate: Generate a single response to a prompt
    - generate-stream: Generate streaming response (machine interface)
    - chat: Start an interactive chat session with a model
    - chat-api: Multi-turn chat API (machine interface)
    - env-info: Show environment and configuration information
    - validate-config: Validate model configuration parameters

Interface Modes:
    - User Interface: Rich, interactive CLI with beautiful formatting
    - Machine Interface: JSON-based API for programmatic usage (use --machine flag)

Example Usage:
    User Interface (default):
        $ monollm list-providers
        $ monollm chat qwen-plus --temperature 0.7 --stream
        $ monollm generate "Explain quantum computing" --model gpt-4o --thinking

    Machine Interface (JSON output):
        $ monollm list-providers --machine
        $ monollm generate "Hello world" --model gpt-4o --machine
        $ monollm generate-stream "Tell a story" --model qwq-32b --thinking

    Configuration Management:
        $ monollm set-defaults gpt-4o --temperature 0.8 --stream
        $ monollm proxy-config --http http://proxy:8080
        $ monollm model-config qwq-32b

Advanced Features:
    - Streaming responses with real-time output
    - Reasoning model support with thinking step display
    - Conversation history management in chat mode
    - Rich formatting with syntax highlighting
    - Token usage tracking and display
    - Comprehensive error messages with suggestions
    - Model defaults and proxy configuration persistence
    - Configuration validation and adjustment

Configuration:
    The CLI respects the same configuration files as the Python API:
    - config/models.json: Model definitions and capabilities
    - config/user_defaults.json: User-defined model defaults
    - config/proxy.json: Proxy configuration
    - Environment variables for API keys
    - Custom configuration directories via --config-dir

Author: cyborgoat
License: MIT License
Copyright: (c) 2025 cyborgoat

For more information, visit: https://github.com/cyborgoat/MonoLLM
Documentation: https://cyborgoat.github.io/MonoLLM/cli.html
"""

from .cli.main import main

if __name__ == "__main__":
    main() 