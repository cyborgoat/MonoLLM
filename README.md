# UnifiedLLM

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-github--pages-blue)](https://cyborgoat.github.io/unified-llm/)
[![GitHub Issues](https://img.shields.io/github/issues/cyborgoat/unified-llm)](https://github.com/cyborgoat/unified-llm/issues)

> **A powerful framework that provides a unified interface for multiple LLM providers, allowing developers to seamlessly switch between different AI models while maintaining consistent API interactions.**

## 🚀 Key Features

- **🔄 Unified Interface**: Access multiple LLM providers through a single, consistent API
- **🌐 Proxy Support**: Configure HTTP/SOCKS5 proxies for all LLM calls
- **📺 Streaming**: Real-time streaming responses for better user experience
- **🧠 Reasoning Models**: Special support for reasoning models with thinking steps
- **🌡️ Temperature Control**: Fine-tune creativity and randomness when supported
- **🔢 Token Management**: Control costs with maximum output token limits
- **🔧 MCP Integration**: Model Context Protocol support when available
- **🎯 OpenAI Protocol**: Prefer OpenAI-compatible APIs for consistency
- **⚙️ JSON Configuration**: Easy configuration management through JSON files

## 📋 Supported Providers

| Provider | Status | Streaming | Reasoning | MCP | OpenAI Protocol |
|----------|--------|-----------|-----------|-----|-----------------|
| **OpenAI** | ✅ Ready | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Anthropic** | ✅ Ready | ✅ Yes | ❌ No | ✅ Yes | ❌ No |
| **Google Gemini** | 🚧 Planned | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Qwen (DashScope)** | ✅ Ready | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **DeepSeek** | ✅ Ready | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Volcengine** | 🚧 Planned | ✅ Yes | ❌ No | ❌ No | ✅ Yes |

## 🛠️ Installation

### Prerequisites

- **Python 3.13+** (required)
- **uv** (recommended) or **pip**

### Quick Install

```bash
# Clone the repository
git clone https://github.com/cyborgoat/unified-llm.git
cd unified-llm

# Install with uv (recommended)
uv sync
uv pip install -e .

# Or install with pip
pip install -e .
```

### Verify Installation

```bash
# Check CLI is working
unified-llm --help

# List available providers
unified-llm list-providers
```

## ⚡ Quick Start

### 1. Set up API Keys

```bash
# Set API keys for the providers you want to use
export DASHSCOPE_API_KEY="your-dashscope-api-key"  # For Qwen
export ANTHROPIC_API_KEY="your-anthropic-api-key"  # For Claude
export OPENAI_API_KEY="your-openai-api-key"        # For GPT models
```

### 2. Basic Python Usage

```python
import asyncio
from unified_llm import UnifiedLLMClient, RequestConfig

async def main():
    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="qwq-32b",  # Qwen's reasoning model
            temperature=0.7,
            max_tokens=1000,
        )
        
        response = await client.generate(
            "Explain quantum computing in simple terms.",
            config
        )
        
        print(response.content)
        if response.usage:
            print(f"Tokens used: {response.usage.total_tokens}")

asyncio.run(main())
```

### 3. CLI Usage

```bash
# Generate text with streaming
unified-llm generate "What is artificial intelligence?" --model qwen-plus --stream

# Use reasoning model with thinking steps
unified-llm generate "Solve: 2x + 5 = 13" --model qwq-32b --thinking

# List available models
unified-llm list-models --provider qwen
```

## 📖 Documentation

- **📚 [Full Documentation](https://cyborgoat.github.io/unified-llm/)** - Comprehensive guides and API reference
- **🚀 [Quick Start Guide](https://cyborgoat.github.io/unified-llm/quickstart.html)** - Get up and running in minutes
- **⚙️ [Configuration Guide](https://cyborgoat.github.io/unified-llm/configuration.html)** - Advanced configuration options
- **💻 [CLI Documentation](https://cyborgoat.github.io/unified-llm/cli.html)** - Command-line interface guide
- **🔧 [Examples](https://cyborgoat.github.io/unified-llm/examples.html)** - Practical usage examples

## 🎯 Use Cases

### Content Generation
```python
config = RequestConfig(model="qwen-plus", temperature=0.8, max_tokens=1000)
response = await client.generate("Write a blog post about renewable energy", config)
```

### Code Assistance
```python
config = RequestConfig(model="qwq-32b", temperature=0.2)
response = await client.generate("Explain this Python function: def fibonacci(n):", config)
```

### Reasoning & Analysis
```python
config = RequestConfig(model="qwq-32b", show_thinking=True)
response = await client.generate("Analyze this data and find trends", config)
```

### Creative Writing
```python
config = RequestConfig(model="qwen-plus", temperature=1.0, max_tokens=2000)
response = await client.generate("Write a science fiction short story", config)
```

## 🔧 Advanced Features

### Streaming Responses
```python
async for chunk in await client.generate_stream(prompt, config):
    if chunk.content:
        print(chunk.content, end="", flush=True)
```

### Multi-turn Conversations
```python
messages = [
    Message(role="system", content="You are a helpful assistant."),
    Message(role="user", content="Hello!"),
]
response = await client.generate(messages, config)
```

### Error Handling
```python
from unified_llm.core.exceptions import UnifiedLLMError, ProviderError

try:
    response = await client.generate(prompt, config)
except ProviderError as e:
    print(f"Provider error: {e}")
except UnifiedLLMError as e:
    print(f"UnifiedLLM error: {e}")
```

## 🌐 Proxy Support

Configure HTTP/SOCKS5 proxies:

```bash
export PROXY_ENABLED=true
export PROXY_TYPE=http
export PROXY_HOST=127.0.0.1
export PROXY_PORT=7890
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](https://cyborgoat.github.io/unified-llm/development/contributing.html) for details.

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/cyborgoat/unified-llm.git
cd unified-llm
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Build documentation
cd docs && make html
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **GitHub**: https://github.com/cyborgoat/unified-llm
- **Documentation**: https://cyborgoat.github.io/unified-llm/
- **Issues**: https://github.com/cyborgoat/unified-llm/issues
- **Discussions**: https://github.com/cyborgoat/unified-llm/discussions

## 🙏 Acknowledgments

- Thanks to all the LLM providers for their amazing APIs
- Inspired by the need for a unified interface across multiple AI providers
- Built with modern Python async/await patterns for optimal performance

## 👨‍💻 Author

Created and maintained by **[cyborgoat](https://github.com/cyborgoat)**

---

**Made with ❤️ by cyborgoat** 