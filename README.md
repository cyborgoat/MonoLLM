# UnifiedLLM

A framework that handles different LLM providers with a simplified interface, allowing users to access multiple LLM models through a single, unified API.

## Features

- 🔄 **Unified Interface**: Access multiple LLM providers through a single API
- 🌐 **Proxy Support**: Configure HTTP/SOCKS5 proxies for all LLM calls
- 📺 **Streaming**: Choose between streaming and non-streaming responses
- 🧠 **Reasoning Models**: Special support for reasoning models with thinking steps
- 🌡️ **Temperature Control**: Adjust creativity/randomness when supported
- 🔢 **Token Management**: Set maximum output tokens for cost control
- 🔧 **MCP Integration**: Support for Model Context Protocol when available
- 🎯 **OpenAI Protocol**: Prefer OpenAI-compatible APIs when available
- ⚙️ **JSON Configuration**: Easy configuration management through JSON files

## Supported Providers

| Provider | Status | Streaming | Reasoning | MCP | OpenAI Protocol |
|----------|--------|-----------|-----------|-----|-----------------|
| OpenAI | ✅ Implemented | ✅ | ✅ | ✅ | ✅ |
| Anthropic | 🚧 Planned | ✅ | ❌ | ✅ | ❌ |
| Google Gemini | 🚧 Planned | ✅ | ❌ | ❌ | ❌ |
| Qwen (DashScope) | 🚧 Planned | ✅ | ✅ | ❌ | ✅ |
| DeepSeek | 🚧 Planned | ✅ | ✅ | ❌ | ✅ |
| Volcengine | 🚧 Planned | ✅ | ❌ | ❌ | ✅ |

## Installation

### Prerequisites

- Python 3.13+
- uv (recommended) or pip

### Install with uv

```bash
# Clone the repository
git clone https://github.com/cyborgoat/unified-llm.git
cd unified-llm

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Install with pip

```bash
# Clone the repository
git clone https://github.com/cyborgoat/unified-llm.git
cd unified-llm

# Install dependencies
pip install -e .
```

## Configuration

### Environment Variables

Set up your API keys as environment variables:

```bash
# OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# Anthropic
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Google Gemini
export GOOGLE_API_KEY="your-google-api-key"

# Qwen (DashScope)
export DASHSCOPE_API_KEY="your-dashscope-api-key"

# DeepSeek
export DEEPSEEK_API_KEY="your-deepseek-api-key"

# Volcengine
export VOLCENGINE_API_KEY="your-volcengine-api-key"
```

You can also override base URLs:

```bash
export OPENAI_BASE_URL="https://your-custom-openai-endpoint.com/v1"
```

### Configuration Files

The framework uses JSON configuration files in the `config/` directory:

- `config/models.json`: Model definitions and capabilities
- `config/proxy.json`: Proxy and network settings

#### Proxy Configuration

Edit `config/proxy.json` to configure proxy settings:

```json
{
  "proxy": {
    "enabled": true,
    "type": "http",
    "host": "proxy.example.com",
    "port": 8080,
    "username": "user",
    "password": "pass",
    "socks5": {
      "enabled": false,
      "host": "socks5.example.com",
      "port": 1080
    }
  }
}
```

## Usage

### Command Line Interface

#### List Providers

```bash
unified-llm list-providers
```

#### List Models

```bash
# List all models
unified-llm list-models

# List models for specific provider
unified-llm list-models --provider openai
```

#### Interactive Chat

```bash
# Basic chat
unified-llm chat gpt-4o

# Chat with options
unified-llm chat gpt-4o --temperature 0.7 --stream --max-tokens 1000

# Chat with reasoning model
unified-llm chat o1 --thinking
```

#### Single Generation

```bash
# Basic generation
unified-llm generate "What is the capital of France?" --model gpt-4o

# With streaming
unified-llm generate "Explain quantum computing" --model gpt-4o --stream

# With reasoning model
unified-llm generate "Solve this math problem: 2x + 5 = 13" --model o1 --thinking
```

### Python API

#### Basic Usage

```python
import asyncio
from unified_llm import UnifiedLLMClient, RequestConfig

async def main():
    # Initialize client
    async with UnifiedLLMClient() as client:
        # Create request configuration
        config = RequestConfig(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=1000,
        )
        
        # Generate response
        response = await client.generate(
            "What is the capital of France?",
            config
        )
        
        print(response.content)
        print(f"Tokens used: {response.usage.total_tokens}")

asyncio.run(main())
```

#### Streaming

```python
import asyncio
from unified_llm import UnifiedLLMClient, RequestConfig

async def main():
    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="gpt-4o",
            stream=True,
        )
        
        streaming_response = await client.generate_stream(
            "Tell me a story",
            config
        )
        
        async for chunk in streaming_response:
            if chunk.content:
                print(chunk.content, end="", flush=True)

asyncio.run(main())
```

#### Reasoning Models

```python
import asyncio
from unified_llm import UnifiedLLMClient, RequestConfig

async def main():
    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="o1",
            show_thinking=True,
        )
        
        response = await client.generate(
            "Solve this complex math problem step by step: ...",
            config
        )
        
        if response.thinking:
            print("Thinking:")
            print(response.thinking)
            print("\nAnswer:")
        
        print(response.content)

asyncio.run(main())
```

#### Multi-turn Conversation

```python
import asyncio
from unified_llm import UnifiedLLMClient, RequestConfig, Message

async def main():
    async with UnifiedLLMClient() as client:
        config = RequestConfig(model="gpt-4o")
        
        messages = [
            Message(role="system", content="You are a helpful assistant."),
            Message(role="user", content="What's the weather like?"),
        ]
        
        response = await client.generate(messages, config)
        print(response.content)
        
        # Continue conversation
        messages.append(Message(role="assistant", content=response.content))
        messages.append(Message(role="user", content="What about tomorrow?"))
        
        response = await client.generate(messages, config)
        print(response.content)

asyncio.run(main())
```

## Model Capabilities

### Reasoning Models

Some models support "reasoning" or "thinking" capabilities:

- **OpenAI o1/o1-mini**: Shows internal reasoning steps
- **QwQ**: Qwen's reasoning model
- **DeepSeek R1**: DeepSeek's reasoning model

Enable thinking steps with `show_thinking=True` in your config.

### Temperature Support

Most models support temperature control (0.0 to 2.0):
- Lower values (0.0-0.3): More focused and deterministic
- Higher values (0.7-1.0): More creative and diverse

Note: Reasoning models typically don't support temperature adjustment.

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/cyborgoat/unified-llm.git
cd unified-llm

# Install with development dependencies
uv sync --dev

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=unified_llm
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Provider Implementation

To add a new provider, implement the `BaseProvider` interface:

```python
from unified_llm.providers.base import BaseProvider

class MyProvider(BaseProvider):
    def get_provider_name(self) -> str:
        return "myprovider"
    
    async def generate(self, messages, config) -> LLMResponse:
        # Implement your provider logic
        pass
    
    async def generate_stream(self, messages, config) -> StreamingResponse:
        # Implement streaming logic
        pass
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Complete Anthropic provider implementation
- [ ] Complete Google Gemini provider implementation
- [ ] Complete Qwen provider implementation
- [ ] Complete DeepSeek provider implementation
- [ ] Complete Volcengine provider implementation
- [ ] Add MCP (Model Context Protocol) support
- [ ] Add function calling support
- [ ] Add image/multimodal support
- [ ] Add conversation memory management
- [ ] Add cost tracking and usage analytics
- [ ] Add provider failover and load balancing 