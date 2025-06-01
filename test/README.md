# MonoLLM Test Suite

This directory contains comprehensive testing utilities for the MonoLLM framework. The test suite is designed to validate functionality across all supported providers and models, with specialized tests for different capabilities.

## 📁 Test Scripts Overview

### 🚀 `test_all_models.py` - Comprehensive Model Testing
Tests all configured models with basic functionality, streaming, and thinking capabilities.

**Usage:**
```bash
# Test all models
python test/test_all_models.py

# The script will automatically:
# - Discover all configured models
# - Test basic generation
# - Test streaming (if supported)
# - Test thinking mode (if supported)
# - Provide detailed success/failure reports
```

**Features:**
- ✅ Automatic model discovery
- 🌊 Streaming capability testing
- 🧠 Thinking mode validation
- 📊 Comprehensive reporting
- ⚠️ Graceful error handling

---

### 🎯 `test_single_model.py` - Individual Model Testing
Flexible testing tool for individual models with custom configurations.

**Usage:**
```bash
# Basic test
python test/test_single_model.py gpt-4o-mini

# Test with streaming
python test/test_single_model.py claude-3-5-sonnet-20241022 --stream

# Test reasoning models with thinking
python test/test_single_model.py qwq-32b --reasoning --stream

# Test with custom prompt
python test/test_single_model.py deepseek-chat --prompt "Explain quantum computing"

# Creative writing test
python test/test_single_model.py claude-3-5-sonnet-20241022 --creative

# Code generation test
python test/test_single_model.py gpt-4o-mini --code
```

**Options:**
- `--stream, -s`: Enable streaming mode
- `--thinking, -t`: Show thinking steps (for reasoning models)
- `--prompt, -p`: Custom prompt text
- `--temperature`: Set temperature (0.0-2.0)
- `--max-tokens`: Maximum tokens to generate
- `--reasoning`: Use reasoning prompt (auto-enables thinking)
- `--creative`: Use creative writing prompt
- `--code`: Use coding prompt

---

### 🧠 `test_thinking.py` - Reasoning Model Testing
Specialized testing for models with thinking capabilities (QwQ, o1, DeepSeek R1, etc.).

**Usage:**
```bash
# Test all thinking models
python test/test_thinking.py

# Test specific model
python test/test_thinking.py --model qwq-32b

# Test specific reasoning scenario
python test/test_thinking.py --test logic_puzzle

# List available tests
python test/test_thinking.py --list-tests
```

**Test Scenarios:**
- 🔢 **basic_math**: Simple arithmetic with step-by-step solving
- 🧩 **logic_puzzle**: Constraint satisfaction problems
- 📊 **multi_step_problem**: Complex multi-step calculations
- 🎯 **complex_reasoning**: Advanced problem-solving strategies
- 💻 **code_reasoning**: Code debugging and analysis

**Quality Metrics:**
- Step coverage analysis
- Thinking content length
- Quality scoring (0.0-1.0)
- Response time measurement

---

### 🔧 `test_providers.py` - Provider-Specific Testing
Tests individual providers and their unique features.

**Usage:**
```bash
# Test all providers
python test/test_providers.py

# Test specific provider
python test/test_providers.py --provider qwen

# Test specific functionality
python test/test_providers.py --provider anthropic --test streaming

# List available providers
python test/test_providers.py --list-providers
```

**Test Types:**
- `basic`: Basic functionality and response generation
- `streaming`: Streaming capability testing
- `thinking`: Reasoning model capabilities
- `edge_cases`: Provider-specific edge cases and error handling

**Provider-Specific Tests:**
- **OpenAI**: Temperature control, special characters, long prompts
- **Anthropic**: System messages, multi-turn conversations
- **Google**: Technical queries, multilingual support
- **Qwen**: Chinese language support, code generation, thinking mode
- **DeepSeek**: Code analysis, algorithm design, reasoning
- **Volcengine**: Cloud service comparisons

---

## 🎯 Quick Start Guide

### 1. **First Time Setup**
```bash
# Ensure you have API keys configured in .env
# Run a quick test to verify setup
python test/test_single_model.py qwq-32b --stream
```

### 2. **Test All Models**
```bash
# Comprehensive test of all models
python test/test_all_models.py
```

### 3. **Test Thinking Capabilities**
```bash
# Test reasoning models
python test/test_thinking.py
```

### 4. **Provider-Specific Testing**
```bash
# Test a specific provider
python test/test_providers.py --provider qwen
```

## 📊 Understanding Test Results

### ✅ Success Indicators
- **✅ PASS**: All tests passed successfully
- **🎉 All tests passed**: Individual test success
- **Quality Score**: 0.8+ indicates high-quality thinking

### ⚠️ Partial Success
- **⚠️ PARTIAL (2/3)**: Some tests failed
- **⏭️ SKIP**: Test not applicable (e.g., thinking test on non-reasoning model)

### ❌ Failure Indicators
- **❌ FAIL**: Test failed with error
- **Provider error**: API-related issues
- **Timeout**: Request took too long

## 🔍 Troubleshooting

### Common Issues

1. **API Key Missing**
   ```
   Warning: No API key found for provider 'openai'
   ```
   **Solution**: Add API key to `.env` file

2. **Model Not Found**
   ```
   Model 'gpt-5' not found in any provider
   ```
   **Solution**: Check `config/models.json` for available models

3. **Quota Exceeded**
   ```
   Error code: 429 - You exceeded your current quota
   ```
   **Solution**: Check API billing or use different provider

4. **Stream Only Models**
   ```
   Stream only model - forcing streaming
   ```
   **Info**: Some models (like QwQ) only work in streaming mode

### Debug Mode
Add verbose output by modifying the test scripts or checking console output for detailed error messages.

## 🚀 Advanced Usage

### Custom Test Scenarios
You can extend the test scripts by:

1. **Adding new reasoning prompts** in `test_thinking.py`
2. **Creating provider-specific tests** in `test_providers.py`
3. **Modifying test parameters** in individual scripts

### Batch Testing
```bash
# Test multiple models sequentially
for model in qwq-32b claude-3-5-sonnet-20241022 deepseek-chat; do
    echo "Testing $model..."
    python test/test_single_model.py $model --stream
done
```

### Performance Monitoring
The test scripts include timing information to help monitor:
- Response latency
- Streaming performance
- Thinking generation speed

## 📈 Test Coverage

Current test coverage includes:

- ✅ **6 Providers**: OpenAI, Anthropic, Google, Qwen, DeepSeek, Volcengine
- ✅ **22+ Models**: Including reasoning models (QwQ, o1, DeepSeek R1)
- ✅ **Multiple Capabilities**: Basic generation, streaming, thinking
- ✅ **Edge Cases**: Error handling, special characters, long prompts
- ✅ **Quality Metrics**: Response analysis and scoring

## 🤝 Contributing

To add new tests:

1. **For new models**: Update `config/models.json`
2. **For new providers**: Add test scenarios in `test_providers.py`
3. **For reasoning tests**: Add prompts in `test_thinking.py`
4. **For edge cases**: Extend provider-specific edge case lists

## 📝 Test Reports

All test scripts provide detailed reports including:
- Success/failure rates
- Performance metrics
- Quality scores (for thinking models)
- Error details and troubleshooting hints

The reports help identify:
- Which models are working correctly
- Performance characteristics
- Areas needing attention or configuration updates 