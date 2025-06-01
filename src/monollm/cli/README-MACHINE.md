# MonoLLM CLI - Machine Interface Documentation

This document provides comprehensive documentation for the MonoLLM CLI machine interface, designed for programmatic integration, automation, and external application usage (such as Tauri sidecars, web applications, and automation scripts).

## Quick Start

All machine interface commands use the `--machine` flag and return structured JSON:

```bash
# Basic usage pattern
monollm <command> [arguments] --machine

# Example
monollm list-providers --machine
```

## JSON Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2025-06-01T12:00:00.000000"
}
```

### Error Response
```json
{
  "error": true,
  "error_type": "ProviderError",
  "error_message": "Detailed error description",
  "timestamp": "2025-06-01T12:00:00.000000",
  "context": "command_name",
  "status_code": 401
}
```

## API Reference

### Information Commands

#### List Providers
```bash
monollm list-providers --machine
```

**Response:**
```json
{
  "providers": {
    "openai": {
      "name": "OpenAI",
      "base_url": "https://api.openai.com/v1",
      "uses_openai_protocol": true,
      "supports_streaming": true,
      "supports_mcp": false,
      "model_count": 15
    },
    "qwen": {
      "name": "Qwen (Alibaba Cloud)",
      "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "uses_openai_protocol": true,
      "supports_streaming": true,
      "supports_mcp": false,
      "model_count": 8
    }
  },
  "total_providers": 6,
  "timestamp": "2025-06-01T12:00:00.000000"
}
```

#### List Models
```bash
# All models
monollm list-models --machine

# Specific provider
monollm list-models --provider openai --machine
```

**Response:**
```json
{
  "models": {
    "openai": {
      "gpt-4o": {
        "name": "GPT-4o",
        "max_tokens": 128000,
        "supports_temperature": true,
        "supports_streaming": true,
        "supports_thinking": false,
        "stream_only": false
      },
      "o1-preview": {
        "name": "o1-preview",
        "max_tokens": 32768,
        "supports_temperature": false,
        "supports_streaming": false,
        "supports_thinking": true,
        "stream_only": false
      }
    }
  },
  "total_models": 25,
  "timestamp": "2025-06-01T12:00:00.000000"
}
```

#### Model Configuration
```bash
monollm model-config qwq-32b --machine
```

**Response:**
```json
{
  "model_id": "qwq-32b",
  "provider_id": "qwen",
  "configuration": {
    "name": "QwQ-32B-Preview",
    "max_tokens": 32768,
    "supports_temperature": true,
    "supports_streaming": true,
    "supports_thinking": true,
    "stream_only": true,
    "default_temperature": 0.7,
    "temperature_range": [0.0, 2.0]
  },
  "timestamp": "2025-06-01T12:00:00.000000"
}
```

#### Environment Information
```bash
monollm env-info --machine
```

**Response:**
```json
{
  "config_dir": "/path/to/config",
  "user_config_exists": true,
  "proxy_config_exists": false,
  "api_key_status": {
    "openai": true,
    "anthropic": false,
    "qwen": true,
    "deepseek": true,
    "google": false,
    "volcengine": false
  },
  "python_version": "3.12.0"
}
```

### Configuration Commands

#### Get Model Defaults
```bash
monollm model-config qwq-32b --machine
```

The response includes current defaults in the model configuration.

#### Set Model Defaults
```bash
monollm set-defaults qwq-32b --temperature 0.8 --thinking --stream --machine
```

**Response:**
```json
{
  "success": true,
  "model_id": "qwq-32b",
  "defaults_set": {
    "temperature": 0.8,
    "max_tokens": null,
    "stream": true,
    "show_thinking": true
  },
  "timestamp": "2025-06-01T12:00:00.000000"
}
```

#### Proxy Configuration
```bash
# Get current proxy config
monollm proxy-config --show --machine

# Set proxy config
monollm proxy-config --http http://proxy:8080 --https https://proxy:8080 --machine
```

**Get Response:**
```json
{
  "proxy_config": {
    "http": "http://proxy:8080",
    "https": "https://proxy:8080",
    "socks": null
  },
  "timestamp": "2025-06-01T12:00:00.000000"
}
```

**Set Response:**
```json
{
  "success": true,
  "proxy_config": {
    "http": "http://proxy:8080",
    "https": "https://proxy:8080",
    "socks": null
  },
  "timestamp": "2025-06-01T12:00:00.000000"
}
```

#### Validate Configuration
```bash
monollm validate-config qwq-32b --temperature 0.8 --stream false --thinking true
```

**Response:**
```json
{
  "model_id": "qwq-32b",
  "original_config": {
    "temperature": 0.8,
    "max_tokens": null,
    "stream": false,
    "show_thinking": true
  },
  "validated_config": {
    "temperature": 0.8,
    "max_tokens": null,
    "stream": true,
    "show_thinking": true
  },
  "changes_made": true,
  "timestamp": "2025-06-01T12:00:00.000000"
}
```

### Generation Commands

#### Single Generation
```bash
monollm generate "What is quantum computing?" --model gpt-4o --machine
```

**Response:**
```json
{
  "content": "Quantum computing is a revolutionary computing paradigm...",
  "model": "gpt-4o",
  "provider": "openai",
  "timestamp": "2025-06-01T12:00:00.000000",
  "request_id": "req_123456",
  "usage": {
    "prompt_tokens": 15,
    "completion_tokens": 150,
    "total_tokens": 165,
    "reasoning_tokens": 0
  }
}
```

#### Generation with Thinking
```bash
monollm generate "Solve: 2x + 5 = 13" --model qwq-32b --thinking --machine
```

**Response:**
```json
{
  "content": "To solve 2x + 5 = 13:\n\n2x = 13 - 5\n2x = 8\nx = 4",
  "thinking": "I need to solve this linear equation step by step...",
  "model": "qwq-32b",
  "provider": "qwen",
  "timestamp": "2025-06-01T12:00:00.000000",
  "request_id": "req_789012",
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 45,
    "total_tokens": 57,
    "reasoning_tokens": 120
  }
}
```

#### Streaming Generation
```bash
monollm generate-stream "Tell me a story" --model qwq-32b --thinking
```

**Output (one JSON object per line):**
```json
{"type": "chunk", "content": "Once", "is_complete": false, "timestamp": "2025-06-01T12:00:00.000000"}
{"type": "chunk", "content": " upon", "is_complete": false, "timestamp": "2025-06-01T12:00:00.001000"}
{"type": "chunk", "thinking": "I should create an engaging story...", "timestamp": "2025-06-01T12:00:00.002000"}
{"type": "chunk", "content": " a time", "is_complete": false, "timestamp": "2025-06-01T12:00:00.003000"}
{"type": "chunk", "is_complete": true, "timestamp": "2025-06-01T12:00:00.004000"}
```

#### Multi-turn Chat
```bash
monollm chat-api '[{"role": "user", "content": "Hello"}]' --model gpt-4o --machine
```

**Response:**
```json
{
  "content": "Hello! How can I help you today?",
  "model": "gpt-4o",
  "provider": "openai",
  "conversation_length": 2,
  "timestamp": "2025-06-01T12:00:00.000000",
  "request_id": "req_345678",
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 12,
    "total_tokens": 20,
    "reasoning_tokens": 0
  }
}
```

## Integration Examples

### Rust (Tauri Sidecar)

```rust
use serde_json::Value;
use std::process::Command;
use tokio::process::Command as AsyncCommand;

// Synchronous execution
fn list_providers() -> Result<Value, Box<dyn std::error::Error>> {
    let output = Command::new("monollm")
        .args(&["list-providers", "--machine"])
        .output()?;
    
    if output.status.success() {
        let result: Value = serde_json::from_slice(&output.stdout)?;
        Ok(result)
    } else {
        let error: Value = serde_json::from_slice(&output.stderr)?;
        Err(format!("Command failed: {}", error).into())
    }
}

// Asynchronous execution
async fn generate_response(prompt: &str, model: &str) -> Result<Value, Box<dyn std::error::Error>> {
    let output = AsyncCommand::new("monollm")
        .args(&[
            "generate", prompt,
            "--model", model,
            "--machine"
        ])
        .output()
        .await?;
    
    if output.status.success() {
        let result: Value = serde_json::from_slice(&output.stdout)?;
        Ok(result)
    } else {
        let error: Value = serde_json::from_slice(&output.stderr)?;
        Err(format!("Generation failed: {}", error).into())
    }
}

// Streaming response handler
async fn handle_streaming_response(prompt: &str, model: &str) -> Result<(), Box<dyn std::error::Error>> {
    use tokio::io::{AsyncBufReadExt, BufReader};
    
    let mut child = AsyncCommand::new("monollm")
        .args(&[
            "generate-stream", prompt,
            "--model", model,
            "--thinking"
        ])
        .stdout(std::process::Stdio::piped())
        .spawn()?;
    
    let stdout = child.stdout.take().unwrap();
    let reader = BufReader::new(stdout);
    let mut lines = reader.lines();
    
    while let Some(line) = lines.next_line().await? {
        let chunk: Value = serde_json::from_str(&line)?;
        
        if let Some(content) = chunk.get("content") {
            print!("{}", content.as_str().unwrap_or(""));
        }
        
        if chunk.get("is_complete").and_then(|v| v.as_bool()).unwrap_or(false) {
            break;
        }
    }
    
    Ok(())
}
```

### Python Integration

```python
import subprocess
import json
import asyncio
from typing import Dict, Any, AsyncGenerator

class MonoLLMClient:
    def __init__(self, config_dir: str = None):
        self.base_cmd = ["monollm"]
        if config_dir:
            self.base_cmd.extend(["--config-dir", config_dir])
    
    def _run_command(self, args: list) -> Dict[str, Any]:
        """Execute a command and return JSON result."""
        cmd = self.base_cmd + args + ["--machine"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            error_data = json.loads(result.stderr) if result.stderr else {
                "error": True,
                "error_message": "Unknown error"
            }
            raise Exception(f"Command failed: {error_data.get('error_message', 'Unknown error')}")
    
    def list_providers(self) -> Dict[str, Any]:
        """List all available providers."""
        return self._run_command(["list-providers"])
    
    def list_models(self, provider: str = None) -> Dict[str, Any]:
        """List available models."""
        args = ["list-models"]
        if provider:
            args.extend(["--provider", provider])
        return self._run_command(args)
    
    def get_model_config(self, model: str, provider: str = None) -> Dict[str, Any]:
        """Get model configuration."""
        args = ["model-config", model]
        if provider:
            args.extend(["--provider", provider])
        return self._run_command(args)
    
    def set_model_defaults(self, model: str, **kwargs) -> Dict[str, Any]:
        """Set model defaults."""
        args = ["set-defaults", model]
        
        if "temperature" in kwargs:
            args.extend(["--temperature", str(kwargs["temperature"])])
        if "max_tokens" in kwargs:
            args.extend(["--max-tokens", str(kwargs["max_tokens"])])
        if kwargs.get("stream"):
            args.append("--stream")
        if kwargs.get("thinking"):
            args.append("--thinking")
        
        return self._run_command(args)
    
    def generate(self, prompt: str, model: str, **kwargs) -> Dict[str, Any]:
        """Generate a response."""
        args = ["generate", prompt, "--model", model]
        
        if "provider" in kwargs:
            args.extend(["--provider", kwargs["provider"]])
        if "temperature" in kwargs:
            args.extend(["--temperature", str(kwargs["temperature"])])
        if "max_tokens" in kwargs:
            args.extend(["--max-tokens", str(kwargs["max_tokens"])])
        if kwargs.get("stream"):
            args.append("--stream")
        if kwargs.get("thinking"):
            args.append("--thinking")
        if kwargs.get("no_defaults"):
            args.append("--no-defaults")
        
        return self._run_command(args)
    
    async def generate_stream(self, prompt: str, model: str, **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate streaming response."""
        args = ["generate-stream", prompt, "--model", model]
        
        if "provider" in kwargs:
            args.extend(["--provider", kwargs["provider"]])
        if "temperature" in kwargs:
            args.extend(["--temperature", str(kwargs["temperature"])])
        if "max_tokens" in kwargs:
            args.extend(["--max-tokens", str(kwargs["max_tokens"])])
        if kwargs.get("thinking"):
            args.append("--thinking")
        if kwargs.get("no_defaults"):
            args.append("--no-defaults")
        
        cmd = self.base_cmd + args
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        async for line in process.stdout:
            if line:
                try:
                    chunk = json.loads(line.decode().strip())
                    yield chunk
                    
                    if chunk.get("is_complete"):
                        break
                except json.JSONDecodeError:
                    continue
        
        await process.wait()
    
    def chat(self, messages: list, model: str, **kwargs) -> Dict[str, Any]:
        """Multi-turn chat."""
        messages_json = json.dumps(messages)
        args = ["chat-api", messages_json, "--model", model]
        
        if "provider" in kwargs:
            args.extend(["--provider", kwargs["provider"]])
        if "temperature" in kwargs:
            args.extend(["--temperature", str(kwargs["temperature"])])
        if "max_tokens" in kwargs:
            args.extend(["--max-tokens", str(kwargs["max_tokens"])])
        if kwargs.get("stream"):
            args.append("--stream")
        if kwargs.get("thinking"):
            args.append("--thinking")
        if kwargs.get("no_defaults"):
            args.append("--no-defaults")
        
        return self._run_command(args)

# Usage example
async def main():
    client = MonoLLMClient()
    
    # List providers
    providers = client.list_providers()
    print(f"Available providers: {list(providers['providers'].keys())}")
    
    # Generate response
    response = client.generate(
        "What is quantum computing?",
        model="gpt-4o",
        temperature=0.7
    )
    print(f"Response: {response['content']}")
    
    # Streaming generation
    print("Streaming response:")
    async for chunk in client.generate_stream(
        "Tell me a story",
        model="qwq-32b",
        thinking=True
    ):
        if chunk.get("content"):
            print(chunk["content"], end="")
        if chunk.get("thinking"):
            print(f"\n[Thinking: {chunk['thinking']}]")
    
    # Multi-turn chat
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help you?"},
        {"role": "user", "content": "What's the weather like?"}
    ]
    
    chat_response = client.chat(messages, model="gpt-4o")
    print(f"Chat response: {chat_response['content']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript/Node.js Integration

```javascript
const { spawn, exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

class MonoLLMClient {
    constructor(configDir = null) {
        this.baseCmd = ['monollm'];
        if (configDir) {
            this.baseCmd.push('--config-dir', configDir);
        }
    }

    async runCommand(args) {
        const cmd = [...this.baseCmd, ...args, '--machine'].join(' ');
        
        try {
            const { stdout, stderr } = await execAsync(cmd);
            return JSON.parse(stdout);
        } catch (error) {
            if (error.stderr) {
                const errorData = JSON.parse(error.stderr);
                throw new Error(`Command failed: ${errorData.error_message}`);
            }
            throw error;
        }
    }

    async listProviders() {
        return await this.runCommand(['list-providers']);
    }

    async listModels(provider = null) {
        const args = ['list-models'];
        if (provider) {
            args.push('--provider', provider);
        }
        return await this.runCommand(args);
    }

    async getModelConfig(model, provider = null) {
        const args = ['model-config', model];
        if (provider) {
            args.push('--provider', provider);
        }
        return await this.runCommand(args);
    }

    async setModelDefaults(model, options = {}) {
        const args = ['set-defaults', model];
        
        if (options.temperature !== undefined) {
            args.push('--temperature', options.temperature.toString());
        }
        if (options.maxTokens !== undefined) {
            args.push('--max-tokens', options.maxTokens.toString());
        }
        if (options.stream) {
            args.push('--stream');
        }
        if (options.thinking) {
            args.push('--thinking');
        }
        
        return await this.runCommand(args);
    }

    async generate(prompt, model, options = {}) {
        const args = ['generate', prompt, '--model', model];
        
        if (options.provider) {
            args.push('--provider', options.provider);
        }
        if (options.temperature !== undefined) {
            args.push('--temperature', options.temperature.toString());
        }
        if (options.maxTokens !== undefined) {
            args.push('--max-tokens', options.maxTokens.toString());
        }
        if (options.stream) {
            args.push('--stream');
        }
        if (options.thinking) {
            args.push('--thinking');
        }
        if (options.noDefaults) {
            args.push('--no-defaults');
        }
        
        return await this.runCommand(args);
    }

    generateStream(prompt, model, options = {}) {
        return new Promise((resolve, reject) => {
            const args = ['generate-stream', prompt, '--model', model];
            
            if (options.provider) {
                args.push('--provider', options.provider);
            }
            if (options.temperature !== undefined) {
                args.push('--temperature', options.temperature.toString());
            }
            if (options.maxTokens !== undefined) {
                args.push('--max-tokens', options.maxTokens.toString());
            }
            if (options.thinking) {
                args.push('--thinking');
            }
            if (options.noDefaults) {
                args.push('--no-defaults');
            }
            
            const cmd = [...this.baseCmd, ...args];
            const process = spawn(cmd[0], cmd.slice(1));
            
            const chunks = [];
            let buffer = '';
            
            process.stdout.on('data', (data) => {
                buffer += data.toString();
                const lines = buffer.split('\n');
                buffer = lines.pop(); // Keep incomplete line in buffer
                
                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const chunk = JSON.parse(line);
                            chunks.push(chunk);
                            
                            if (options.onChunk) {
                                options.onChunk(chunk);
                            }
                            
                            if (chunk.is_complete) {
                                resolve(chunks);
                                return;
                            }
                        } catch (error) {
                            // Ignore malformed JSON lines
                        }
                    }
                }
            });
            
            process.stderr.on('data', (data) => {
                try {
                    const error = JSON.parse(data.toString());
                    reject(new Error(`Stream failed: ${error.error_message}`));
                } catch {
                    reject(new Error(`Stream failed: ${data.toString()}`));
                }
            });
            
            process.on('close', (code) => {
                if (code !== 0 && chunks.length === 0) {
                    reject(new Error(`Process exited with code ${code}`));
                } else {
                    resolve(chunks);
                }
            });
        });
    }

    async chat(messages, model, options = {}) {
        const messagesJson = JSON.stringify(messages);
        const args = ['chat-api', messagesJson, '--model', model];
        
        if (options.provider) {
            args.push('--provider', options.provider);
        }
        if (options.temperature !== undefined) {
            args.push('--temperature', options.temperature.toString());
        }
        if (options.maxTokens !== undefined) {
            args.push('--max-tokens', options.maxTokens.toString());
        }
        if (options.stream) {
            args.push('--stream');
        }
        if (options.thinking) {
            args.push('--thinking');
        }
        if (options.noDefaults) {
            args.push('--no-defaults');
        }
        
        return await this.runCommand(args);
    }
}

// Usage example
async function main() {
    const client = new MonoLLMClient();
    
    try {
        // List providers
        const providers = await client.listProviders();
        console.log('Available providers:', Object.keys(providers.providers));
        
        // Generate response
        const response = await client.generate(
            'What is quantum computing?',
            'gpt-4o',
            { temperature: 0.7 }
        );
        console.log('Response:', response.content);
        
        // Streaming generation
        console.log('Streaming response:');
        await client.generateStream(
            'Tell me a story',
            'qwq-32b',
            {
                thinking: true,
                onChunk: (chunk) => {
                    if (chunk.content) {
                        process.stdout.write(chunk.content);
                    }
                    if (chunk.thinking) {
                        console.log(`\n[Thinking: ${chunk.thinking}]`);
                    }
                }
            }
        );
        
        // Multi-turn chat
        const messages = [
            { role: 'user', content: 'Hello' },
            { role: 'assistant', content: 'Hi! How can I help you?' },
            { role: 'user', content: "What's the weather like?" }
        ];
        
        const chatResponse = await client.chat(messages, 'gpt-4o');
        console.log('Chat response:', chatResponse.content);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
```

## Error Handling

### Common Error Types

1. **ProviderError**: API-related errors
2. **ModelNotFoundError**: Invalid model ID
3. **ConfigurationError**: Invalid parameters
4. **AuthenticationError**: Missing or invalid API keys
5. **NetworkError**: Connection issues

### Error Response Structure
```json
{
  "error": true,
  "error_type": "ProviderError",
  "error_message": "API key not found for provider 'openai'",
  "timestamp": "2025-06-01T12:00:00.000000",
  "context": "generate",
  "status_code": 401
}
```

### Best Practices for Error Handling

1. **Always check the `error` field** in responses
2. **Parse `error_type`** to handle different error categories
3. **Use `status_code`** for HTTP-related errors
4. **Implement retry logic** for network errors
5. **Validate configurations** before making API calls

## Performance Considerations

### Command Execution Overhead
- Each CLI command has startup overhead (~100-200ms)
- For high-frequency usage, consider batching operations
- Use streaming for long-running generations

### Memory Usage
- CLI commands are stateless and don't persist memory
- Large responses are streamed to reduce memory usage
- Configuration is loaded fresh for each command

### Concurrency
- CLI commands can be run concurrently
- Each command is independent and thread-safe
- Rate limiting is handled by individual providers

## Security Considerations

### API Key Management
- API keys are read from environment variables
- Never pass API keys as command-line arguments
- Use secure environment variable management

### Input Validation
- All inputs are validated before processing
- JSON inputs are parsed safely
- Command injection is prevented through proper argument handling

### Output Sanitization
- All outputs are properly escaped JSON
- No executable code in responses
- Error messages don't leak sensitive information

## Troubleshooting

### Debug Information
```bash
# Check environment and configuration
monollm env-info --machine

# Validate model configuration
monollm validate-config model-id --temperature 0.8

# Test basic connectivity
monollm list-providers --machine
```

### Common Issues and Solutions

1. **Command not found**
   - Ensure MonoLLM is installed: `pip install monollm`
   - Check PATH includes Python scripts directory

2. **API key errors**
   - Check environment variables: `monollm env-info --machine`
   - Verify API key format and permissions

3. **Model not available**
   - List available models: `monollm list-models --machine`
   - Check provider-specific model IDs

4. **Configuration errors**
   - Validate parameters: `monollm validate-config model-id --param value`
   - Check model capabilities: `monollm model-config model-id --machine`

5. **Network issues**
   - Check proxy configuration: `monollm proxy-config --show --machine`
   - Verify network connectivity to provider APIs

## Version Compatibility

This machine interface is designed to be stable across versions:

- **JSON structure**: Backward compatible additions only
- **Command names**: No breaking changes to existing commands
- **Error formats**: Consistent structure maintained
- **Response fields**: New fields added, existing fields preserved

Always check the `timestamp` field to ensure you're working with current data. 