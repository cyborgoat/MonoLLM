# MonoLLM

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-github--pages-blue)](https://cyborgoat.github.io/MonoLLM/)
[![GitHub Issues](https://img.shields.io/github/issues/cyborgoat/MonoLLM)](https://github.com/cyborgoat/MonoLLM/issues)

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
git clone https://github.com/cyborgoat/MonoLLM.git
cd MonoLLM

# Install with uv (recommended)
uv sync
uv pip install -e .

# Or install with pip
pip install -e .
```

### Verify Installation

```bash
# Check CLI is working
monollm --help

# List available providers
monollm list-providers
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
from monollm import UnifiedLLMClient, RequestConfig

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
monollm generate "What is artificial intelligence?" --model qwen-plus --stream

# Use reasoning model with thinking steps
monollm generate "Solve: 2x + 5 = 13" --model qwq-32b --thinking

# List available models
monollm list-models --provider qwen
```

## 📖 Documentation

- **📚 [Full Documentation](https://cyborgoat.github.io/MonoLLM/)** - Comprehensive guides and API reference
- **🚀 [Quick Start Guide](https://cyborgoat.github.io/MonoLLM/quickstart.html)** - Get up and running in minutes
- **⚙️ [Configuration Guide](https://cyborgoat.github.io/MonoLLM/configuration.html)** - Advanced configuration options
- **💻 [CLI Documentation](https://cyborgoat.github.io/MonoLLM/cli.html)** - Command-line interface guide
- **🤖 [Machine Interface](src/monollm/cli/README-MACHINE.md)** - JSON API for programmatic usage and Tauri sidecars
- **🔧 [Examples](https://cyborgoat.github.io/MonoLLM/examples.html)** - Practical usage examples

## 🤖 Machine Interface & Tauri Integration

MonoLLM provides a powerful machine-friendly JSON API perfect for integration with external applications, automation scripts, and Tauri sidecars:

```bash
# All commands support --machine flag for JSON output
monollm list-providers --machine
monollm generate "Hello world" --model gpt-4o --machine
monollm generate-stream "Tell a story" --model qwq-32b --thinking
```

### Tauri Sidecar Example

```rust
// Rust code for Tauri app
use std::process::Command;

let output = Command::new("monollm")
    .args(&["generate", "What is AI?", "--model", "gpt-4o", "--machine"])
    .output()
    .expect("Failed to execute command");

let response: serde_json::Value = serde_json::from_slice(&output.stdout)?;
println!("AI Response: {}", response["content"]);
```

### Key Machine Interface Features

- **🔄 Structured JSON**: All responses in consistent JSON format
- **📡 Streaming Support**: Real-time JSON chunks for streaming responses  
- **⚙️ Configuration API**: Programmatic model defaults and proxy management
- **🛡️ Error Handling**: Consistent error format with detailed context
- **🔧 Validation**: Parameter validation before API calls
- **📊 Usage Tracking**: Token usage and performance metrics

**📖 [Complete Machine Interface Documentation](src/monollm/cli/README-MACHINE.md)**

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

### Thinking Mode for Reasoning Models

MonoLLM supports reasoning models that can show their internal thought process:

```python
# Enable thinking mode to see step-by-step reasoning
config = RequestConfig(
    model="qwq-32b",  # QwQ reasoning model
    show_thinking=True,  # Show internal reasoning
    temperature=0.7
)

response = await client.generate(
    "Solve this step by step: If a train travels 120 km in 2 hours, then 180 km in 3 hours, what is its average speed?",
    config
)

# Access the thinking process
if response.thinking:
    print("💭 Thinking Process:")
    print(response.thinking)
    print("\n" + "="*50)

print("🎯 Final Answer:")
print(response.content)
```

**Supported Reasoning Models:**
- **QwQ-32B** (`qwq-32b`) - Stream-only reasoning model
- **QwQ-Plus** (`qwq-plus`) - Stream-only reasoning model  
- **Qwen3 Series** (`qwen3-32b`, `qwen3-8b`, etc.) - Support both modes
- **OpenAI o1** (`o1`, `o1-mini`) - Advanced reasoning models
- **DeepSeek R1** (`deepseek-reasoner`) - Reasoning model

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
from monollm.core.exceptions import MonoLLMError, ProviderError

try:
    response = await client.generate(prompt, config)
except ProviderError as e:
    print(f"Provider error: {e}")
except MonoLLMError as e:
    print(f"MonoLLM error: {e}")
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

We welcome contributions! Please see our [Contributing Guide](https://cyborgoat.github.io/MonoLLM/development/contributing.html) for details.

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/cyborgoat/MonoLLM.git
cd MonoLLM
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

- **GitHub**: <https://github.com/cyborgoat/MonoLLM>
- **Documentation**: <https://cyborgoat.github.io/MonoLLM/>
- **Issues**: <https://github.com/cyborgoat/MonoLLM/issues>
- **Discussions**: <https://github.com/cyborgoat/MonoLLM/discussions>

## 🙏 Acknowledgments

- Thanks to all the LLM providers for their amazing APIs
- Inspired by the need for a unified interface across multiple AI providers
- Built with modern Python async/await patterns for optimal performance

## 👨‍💻 Author

Created and maintained by **[cyborgoat](https://github.com/cyborgoat)**

---

**Made with ❤️ by cyborgoat**
