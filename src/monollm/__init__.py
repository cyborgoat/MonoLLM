#!/usr/bin/env python3
"""
MonoLLM - A unified framework for accessing multiple LLM providers.

MonoLLM is a powerful Python framework that provides a single, consistent
interface for interacting with multiple Large Language Model providers. It
abstracts away the differences between various LLM APIs, allowing developers
to seamlessly switch between providers while maintaining the same code structure.

Key Features:
    🔄 Unified Interface: Access multiple LLM providers through a single API
    🌐 Proxy Support: Configure HTTP/SOCKS5 proxies for all LLM calls
    📺 Streaming: Real-time streaming responses for better user experience
    🧠 Reasoning Models: Special support for reasoning models with thinking steps
    🌡️ Temperature Control: Fine-tune creativity and randomness when supported
    🔢 Token Management: Control costs with maximum output token limits
    🔧 MCP Integration: Model Context Protocol support when available
    🎯 OpenAI Protocol: Prefer OpenAI-compatible APIs for consistency
    ⚙️ JSON Configuration: Easy configuration management through JSON files

Supported Providers:
    - OpenAI (GPT models, including reasoning models like o1)
    - Anthropic (Claude models with MCP support)
    - Google (Gemini models) [Planned]
    - Qwen/DashScope (Qwen models, including reasoning QwQ)
    - DeepSeek (DeepSeek models, including reasoning R1)
    - Volcengine (Doubao models) [Planned]

Quick Start:
    Basic usage example:
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
        >>> from monollm import Message
        >>> 
        >>> async def chat_example():
        ...     async with UnifiedLLMClient() as client:
        ...         messages = [
        ...             Message(role="system", content="You are a helpful assistant."),
        ...             Message(role="user", content="What is Python?"),
        ...         ]
        ...         config = RequestConfig(model="claude-3-sonnet")
        ...         response = await client.generate(messages, config)
        ...         print(response.content)

Installation:
    Install from source:
        $ git clone https://github.com/cyborgoat/MonoLLM.git
        $ cd MonoLLM
        $ uv sync && uv pip install -e .

    Or with pip:
        $ pip install -e .

Configuration:
    Set up API keys as environment variables:
        $ export OPENAI_API_KEY="your-openai-key"
        $ export ANTHROPIC_API_KEY="your-anthropic-key"
        $ export DASHSCOPE_API_KEY="your-qwen-key"

CLI Usage:
    The framework includes a comprehensive CLI:
        $ monollm list-providers
        $ monollm chat gpt-4o --stream
        $ monollm generate "Explain AI" --model qwen-plus

Author: cyborgoat
License: MIT License
Copyright: (c) 2025 cyborgoat
Version: 0.1.1

For more information:
    - GitHub: https://github.com/cyborgoat/MonoLLM
    - Documentation: https://cyborgoat.github.io/MonoLLM/
    - Issues: https://github.com/cyborgoat/MonoLLM/issues
"""

from .core.client import UnifiedLLMClient
from .core.exceptions import (
    MonoLLMError,
    ProviderError,
    ConfigurationError,
    RateLimitError,
    AuthenticationError,
    ModelNotFoundError,
    QuotaExceededError,
    ConnectionError,
    ValidationError,
)
from .core.models import (
    LLMResponse,
    StreamingResponse,
    ModelInfo,
    ProviderInfo,
    RequestConfig,
    Message,
    Usage,
    StreamChunk,
)

# Version information
__version__ = "0.1.1"
__author__ = "cyborgoat"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 cyborgoat"

# Public API exports
__all__ = [
    # Core client
    "UnifiedLLMClient",

    # Data models
    "LLMResponse",
    "StreamingResponse",
    "ModelInfo",
    "ProviderInfo",
    "RequestConfig",
    "Message",
    "Usage",
    "StreamChunk",

    # Exceptions
    "MonoLLMError",
    "ProviderError",
    "ConfigurationError",
    "RateLimitError",
    "AuthenticationError",
    "ModelNotFoundError",
    "QuotaExceededError",
    "ConnectionError",
    "ValidationError",

    # Metadata
    "__version__",
    "__author__",
    "__license__",
    "__copyright__",
]
