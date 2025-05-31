# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-05-31

### Added
- ✅ **Complete proxy support for all providers** - All LLM providers now route through configured proxy settings
- ✅ **Environment-based configuration** - Moved from JSON to `.env` file-based configuration for better security and flexibility
- ✅ **Comprehensive provider implementations**:
  - **Anthropic Claude** - Full implementation with streaming support (claude-3-5-sonnet, claude-3-5-haiku)
  - **Google Gemini** - Direct HTTP API implementation with proxy support (gemini-2.0-flash-exp, gemini-1.5-pro, gemini-1.5-flash)
  - **Qwen (DashScope)** - OpenAI-compatible API implementation with reasoning model support (qwq-plus, qwq-32b, qwen3 series)
  - **DeepSeek** - Complete implementation with reasoning models (deepseek-reasoner R1, deepseek-chat V3)
  - **Volcengine** - Basic implementation with Doubao models
- ✅ **Reasoning model support** - Special handling for models with thinking capabilities
- ✅ **Streaming support** - All providers support both streaming and non-streaming responses
- ✅ **15+ models** across 5 providers with proper token usage tracking
- ✅ **Comprehensive proxy configuration** - HTTP and SOCKS5 proxy support with authentication
- ✅ **Environment variable security** - API keys managed through .env files
- ✅ **15-second timeout** optimization for faster response times

### Changed
- **Configuration system** - Migrated from JSON-based to environment variable-based configuration
- **Google Gemini provider** - Switched from SDK to direct HTTP API for better proxy integration
- **Base URLs** - Updated Qwen provider to use OpenAI-compatible endpoint
- **Model naming** - Corrected DeepSeek model names to match actual API
- **Timeout settings** - Reduced from 60s to 15s for better user experience

### Fixed
- ✅ **Proxy integration** - All providers now properly route through configured proxy (127.0.0.1:7890 tested)
- ✅ **Model name mapping** - Correct mapping between config names and actual API model names
- ✅ **HTTP client configuration** - Proper httpx client setup with proxy support for all providers
- ✅ **API endpoint URLs** - Corrected base URLs for all providers
- ✅ **Token usage tracking** - Proper parsing and display of token usage across all providers

### Tested Working Models
- **Google Gemini**: gemini-2.0-flash-exp, gemini-1.5-pro, gemini-1.5-flash
- **Anthropic Claude**: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022  
- **Qwen (DashScope)**: qwq-plus, qwq-32b, qwen3-32b, qwen3-8b, qwen3-0.6b
- **DeepSeek**: deepseek-chat, deepseek-reasoner (reasoning model)

### Technical Improvements
- **Parallel model initialization** - All providers initialize simultaneously
- **Proper error handling** - HTTP status error handling and connection error management
- **Stream processing** - Efficient chunk processing for streaming responses
- **Memory management** - Proper client lifecycle management with async context managers

## [0.1.0] - Initial Release

### Added
- Basic framework structure
- OpenAI provider implementation
- Command-line interface
- Configuration management
- Base provider abstraction 