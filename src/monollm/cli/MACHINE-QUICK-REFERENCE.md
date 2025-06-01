# MonoLLM Machine Interface - Quick Reference

## Basic Usage Pattern
```bash
monollm <command> [arguments] --machine
```

## Information Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list-providers --machine` | List all providers | `monollm list-providers --machine` |
| `list-models --machine` | List all models | `monollm list-models --provider openai --machine` |
| `model-config MODEL --machine` | Model configuration | `monollm model-config qwq-32b --machine` |
| `env-info --machine` | Environment info | `monollm env-info --machine` |

## Configuration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `set-defaults MODEL [opts] --machine` | Set model defaults | `monollm set-defaults qwq-32b --temperature 0.8 --thinking --machine` |
| `proxy-config [opts] --machine` | Proxy configuration | `monollm proxy-config --http http://proxy:8080 --machine` |
| `validate-config MODEL [opts]` | Validate parameters | `monollm validate-config qwq-32b --temperature 0.8` |

## Generation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `generate PROMPT --model MODEL --machine` | Single generation | `monollm generate "Hello" --model gpt-4o --machine` |
| `generate-stream PROMPT --model MODEL` | Streaming (JSON per line) | `monollm generate-stream "Story" --model qwq-32b --thinking` |
| `chat-api MESSAGES --model MODEL` | Multi-turn chat | `monollm chat-api '[{"role":"user","content":"Hi"}]' --model gpt-4o` |

## JSON Response Formats

### Success Response
```json
{
  "content": "Response text",
  "model": "gpt-4o",
  "provider": "openai",
  "timestamp": "2025-06-01T12:00:00.000000",
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 20,
    "total_tokens": 30
  }
}
```

### Error Response
```json
{
  "error": true,
  "error_type": "ProviderError",
  "error_message": "API key not found",
  "timestamp": "2025-06-01T12:00:00.000000",
  "context": "generate"
}
```

### Streaming Chunk
```json
{"type": "chunk", "content": "Hello", "is_complete": false, "timestamp": "..."}
{"type": "chunk", "thinking": "Let me think...", "timestamp": "..."}
{"type": "chunk", "is_complete": true, "timestamp": "..."}
```

## Common Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--model MODEL` | Model to use | `--model gpt-4o` |
| `--provider PROVIDER` | Specific provider | `--provider openai` |
| `--temperature FLOAT` | Creativity (0.0-2.0) | `--temperature 0.8` |
| `--max-tokens INT` | Max output tokens | `--max-tokens 1000` |
| `--stream` | Enable streaming | `--stream` |
| `--thinking` | Show reasoning | `--thinking` |
| `--no-defaults` | Ignore saved defaults | `--no-defaults` |

## Integration Examples

### Rust (Tauri)
```rust
let output = Command::new("monollm")
    .args(&["generate", "Hello", "--model", "gpt-4o", "--machine"])
    .output()?;
let result: serde_json::Value = serde_json::from_slice(&output.stdout)?;
```

### Python
```python
import subprocess, json
result = subprocess.run(["monollm", "generate", "Hello", "--model", "gpt-4o", "--machine"], 
                       capture_output=True, text=True)
response = json.loads(result.stdout)
```

### JavaScript
```javascript
const { exec } = require('child_process');
exec('monollm generate "Hello" --model gpt-4o --machine', (error, stdout) => {
    const response = JSON.parse(stdout);
});
```

## Error Handling

Always check for the `error` field in responses:

```bash
# Check if response contains error
if response.get("error"):
    print(f"Error: {response['error_message']}")
else:
    print(f"Content: {response['content']}")
```

## Performance Tips

- Use `generate-stream` for long responses
- Set appropriate `--max-tokens` to control costs
- Use `validate-config` before making API calls
- Cache responses when possible
- Run commands concurrently for batch operations

## Complete Documentation

📖 **[Full Machine Interface Documentation](README-MACHINE.md)** 