# MonoLLM CLI Module

This module provides both user-friendly and machine-friendly command-line interfaces for the MonoLLM framework. It's designed to support both interactive human usage and programmatic integration with external applications like Tauri sidecars.

## Architecture

The CLI module is organized into several components:

```
src/monollm/cli/
├── __init__.py           # Module initialization
├── main.py               # Main CLI entry point with all commands
├── user_interface.py     # Rich, human-friendly interface
├── machine_interface.py  # JSON-based programmatic interface
├── config_manager.py     # Configuration and model management
├── output_formatter.py   # Output formatting for both modes
└── README.md            # This file
```

## Interface Modes

### User Interface (Default)
- Rich terminal output with tables, panels, and colors
- Interactive chat sessions
- Beautiful formatting and progress indicators
- Human-readable error messages

### Machine Interface (--machine flag)
- Structured JSON output for all commands
- Consistent error format
- Timestamp information
- Suitable for programmatic consumption

## Available Commands

### Information Commands

#### `list-providers`
List all available LLM providers with their capabilities.

```bash
# User interface (rich table)
monollm list-providers

# Machine interface (JSON)
monollm list-providers --machine
```

#### `list-models`
List all available models, optionally filtered by provider.

```bash
# All models (user interface)
monollm list-models

# Specific provider (machine interface)
monollm list-models --provider qwen --machine
```

#### `model-config`
Show detailed configuration for a specific model.

```bash
# Show model capabilities and defaults
monollm model-config qwq-32b

# Machine-readable format
monollm model-config gpt-4o --machine
```

#### `env-info`
Display environment and configuration information.

```bash
# Show API key status, config files, etc.
monollm env-info

# JSON format for automation
monollm env-info --machine
```

### Configuration Commands

#### `set-defaults`
Set default parameters for a model that persist across sessions.

```bash
# Set defaults for a model
monollm set-defaults qwq-32b --temperature 0.8 --thinking --stream

# Machine interface
monollm set-defaults gpt-4o --temperature 0.7 --max-tokens 2000 --machine
```

#### `proxy-config`
Configure proxy settings for all LLM API calls.

```bash
# Show current proxy configuration
monollm proxy-config --show

# Set HTTP proxy
monollm proxy-config --http http://proxy:8080

# Set multiple proxies
monollm proxy-config --http http://proxy:8080 --https https://proxy:8080 --socks socks5://proxy:1080

# Machine interface
monollm proxy-config --show --machine
```

#### `validate-config`
Validate configuration parameters for a model (machine interface only).

```bash
# Check if parameters are valid for a model
monollm validate-config qwq-32b --temperature 0.8 --stream true --thinking true
```

### Generation Commands

#### `generate`
Generate a single response from an LLM model.

```bash
# Basic generation
monollm generate "What is quantum computing?" --model gpt-4o

# With custom parameters
monollm generate "Explain AI" --model claude-3-5-sonnet-20241022 --temperature 0.8 --stream

# Reasoning model with thinking
monollm generate "Solve: 2x + 5 = 13" --model qwq-32b --thinking

# Machine interface
monollm generate "Hello world" --model gpt-4o --machine

# Don't use saved defaults
monollm generate "Test" --model gpt-4o --no-defaults --temperature 0.5
```

#### `generate-stream`
Generate streaming response (machine interface only).

```bash
# Stream JSON chunks to stdout
monollm generate-stream "Tell me a story" --model qwq-32b --thinking

# Each line is a JSON object representing a chunk
monollm generate-stream "Explain physics" --model claude-3-5-sonnet-20241022
```

### Chat Commands

#### `chat`
Interactive chat session (user interface only).

```bash
# Start interactive chat
monollm chat gpt-4o

# With custom parameters
monollm chat qwq-32b --thinking --stream --temperature 0.8

# Special commands in chat:
# - 'exit': Quit the chat
# - 'clear': Clear conversation history
```

#### `chat-api`
Multi-turn chat API (machine interface only).

```bash
# Send conversation history as JSON
monollm chat-api '[{"role": "user", "content": "Hello"}]' --model gpt-4o

# With parameters
monollm chat-api '[{"role": "user", "content": "What is AI?"}, {"role": "assistant", "content": "AI is..."}, {"role": "user", "content": "Tell me more"}]' --model claude-3-5-sonnet-20241022 --temperature 0.7
```

## Configuration Management

### Model Defaults
The CLI supports saving default parameters for each model:

```bash
# Set defaults
monollm set-defaults qwq-32b --temperature 0.8 --thinking --stream

# View current defaults (included in model-config)
monollm model-config qwq-32b

# Defaults are automatically applied unless --no-defaults is used
monollm generate "Test" --model qwq-32b  # Uses saved defaults
monollm generate "Test" --model qwq-32b --no-defaults  # Ignores defaults
```

### Proxy Configuration
Configure proxies for all LLM API calls:

```bash
# Set HTTP proxy
monollm proxy-config --http http://proxy.company.com:8080

# Set HTTPS proxy
monollm proxy-config --https https://proxy.company.com:8080

# Set SOCKS proxy
monollm proxy-config --socks socks5://proxy.company.com:1080

# View current configuration
monollm proxy-config --show
```

### Configuration Files
The CLI creates and manages several configuration files:

- `config/models.json` - Model definitions (shared with Python API)
- `config/user_defaults.json` - User-defined model defaults
- `config/proxy.json` - Proxy configuration
- Environment variables for API keys

## Machine Interface Details

### JSON Output Format
All machine interface commands return structured JSON:

```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2025-06-01T20:09:48.534346"
}
```

### Error Format
Errors are consistently formatted:

```json
{
  "error": true,
  "error_type": "ProviderError",
  "error_message": "API key not found",
  "timestamp": "2025-06-01T20:09:48.534346",
  "context": "generate"
}
```

### Streaming Format
Streaming responses output one JSON object per line:

```json
{"type": "chunk", "content": "Hello", "is_complete": false, "timestamp": "..."}
{"type": "chunk", "content": " world", "is_complete": false, "timestamp": "..."}
{"type": "chunk", "thinking": "Let me think...", "timestamp": "..."}
{"type": "chunk", "is_complete": true, "timestamp": "..."}
```

## Integration Examples

### Tauri Sidecar Integration

```rust
// Rust code for Tauri app
use std::process::Command;

// List providers
let output = Command::new("monollm")
    .args(&["list-providers", "--machine"])
    .output()
    .expect("Failed to execute command");

let providers: serde_json::Value = serde_json::from_slice(&output.stdout)?;

// Generate response
let output = Command::new("monollm")
    .args(&[
        "generate", 
        "What is AI?", 
        "--model", "gpt-4o",
        "--machine"
    ])
    .output()
    .expect("Failed to execute command");

let response: serde_json::Value = serde_json::from_slice(&output.stdout)?;
```

### Python Integration

```python
import subprocess
import json

# List models
result = subprocess.run([
    "monollm", "list-models", "--machine"
], capture_output=True, text=True)

models = json.loads(result.stdout)

# Generate with streaming
process = subprocess.Popen([
    "monollm", "generate-stream", 
    "Tell me a story", 
    "--model", "qwq-32b", 
    "--thinking"
], stdout=subprocess.PIPE, text=True)

for line in process.stdout:
    chunk = json.loads(line)
    if chunk.get("content"):
        print(chunk["content"], end="")
```

### JavaScript/Node.js Integration

```javascript
const { spawn } = require('child_process');

// Generate response
function generateResponse(prompt, model) {
    return new Promise((resolve, reject) => {
        const process = spawn('monollm', [
            'generate', prompt, 
            '--model', model, 
            '--machine'
        ]);
        
        let output = '';
        process.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        process.on('close', (code) => {
            if (code === 0) {
                resolve(JSON.parse(output));
            } else {
                reject(new Error(`Process exited with code ${code}`));
            }
        });
    });
}

// Usage
generateResponse("What is quantum computing?", "gpt-4o")
    .then(response => console.log(response.content))
    .catch(error => console.error(error));
```

## Advanced Features

### Configuration Validation
The CLI automatically validates parameters against model capabilities:

```bash
# This will automatically adjust invalid parameters
monollm validate-config qwq-32b --temperature 0.8 --stream false

# Output shows what was changed:
{
  "model_id": "qwq-32b",
  "original_config": {"temperature": 0.8, "stream": false},
  "validated_config": {"temperature": 0.8, "stream": true},
  "changes_made": true
}
```

### Parameter Precedence
Parameters are applied in this order:
1. Explicit command-line arguments (highest priority)
2. Saved model defaults
3. Model-specific requirements (e.g., stream-only models)
4. Framework defaults (lowest priority)

### Error Handling
The CLI provides comprehensive error handling:
- API key validation
- Model availability checks
- Parameter validation
- Network error recovery
- Graceful degradation

## Best Practices

### For Interactive Use
- Use the default user interface for better readability
- Set up model defaults for frequently used configurations
- Use the chat command for multi-turn conversations

### For Programmatic Use
- Always use the `--machine` flag for consistent JSON output
- Parse the `error` field to detect failures
- Handle streaming responses line by line
- Validate configurations before making API calls

### For Production
- Set up proxy configuration if needed
- Monitor API key status with `env-info`
- Use configuration validation to prevent errors
- Implement proper error handling for all failure modes

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```bash
   monollm env-info --machine  # Check API key status
   ```

2. **Model Not Available**
   ```bash
   monollm list-models --machine  # Check available models
   ```

3. **Configuration Issues**
   ```bash
   monollm validate-config model-id --temperature 0.8  # Validate parameters
   ```

4. **Proxy Problems**
   ```bash
   monollm proxy-config --show  # Check proxy settings
   ```

### Debug Mode
For detailed error information, check the console output during command execution. The CLI provides comprehensive error messages with suggestions for resolution.

## Contributing

When extending the CLI module:

1. Add new commands to `main.py`
2. Implement logic in appropriate interface classes
3. Update output formatters for both user and machine modes
4. Add comprehensive error handling
5. Update this documentation

The modular design makes it easy to add new functionality while maintaining consistency across both interface modes. 