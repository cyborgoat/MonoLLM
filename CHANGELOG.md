# Changelog

All notable changes to MonoLLM will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2025-06-01

### Added
- **Machine Interface & JSON API**: Comprehensive machine-friendly interface for programmatic usage
  - `--machine` flag for all CLI commands to output structured JSON
  - Consistent JSON response format with timestamps and error handling
  - Streaming JSON output with line-by-line chunks for real-time processing
  - Complete API coverage for all CLI operations
- **Tauri Sidecar Integration**: Perfect integration for desktop applications
  - Rust, Python, and JavaScript integration examples
  - Asynchronous and synchronous execution patterns
  - Streaming response handling for real-time UI updates
- **Enhanced CLI Commands**: Expanded command set with dual interface support
  - `generate-stream`: Machine-only streaming command with JSON chunks
  - `chat-api`: Multi-turn conversation API for programmatic usage
  - `validate-config`: Parameter validation before API calls
  - `env-info`: Environment and configuration information
  - `set-defaults`: Persistent model defaults management
  - `proxy-config`: HTTP/HTTPS/SOCKS proxy configuration
- **Configuration Management**: Persistent configuration system
  - Model-specific defaults stored in `config/user_defaults.json`
  - Proxy configuration in `config/proxy.json`
  - Parameter precedence: CLI args > defaults > model requirements
  - Configuration validation and automatic adjustment
- **Modular CLI Architecture**: Clean separation of concerns
  - `user_interface.py`: Rich, human-friendly interface
  - `machine_interface.py`: JSON-based programmatic interface
  - `config_manager.py`: Configuration and model management
  - `output_formatter.py`: Dual-mode output formatting
  - `main.py`: Unified command entry point

### Enhanced
- **CLI User Experience**: Rich terminal interface with beautiful formatting
  - Interactive chat sessions with conversation history
  - Rich tables and panels for information display
  - Progress indicators and streaming output
  - Comprehensive error messages with context
- **Output Formatting**: Dual-mode formatting system
  - User mode: Rich tables, panels, markdown rendering
  - Machine mode: Structured JSON with consistent schema
  - Error handling with detailed context and suggestions
- **Parameter Management**: Advanced parameter handling
  - Automatic validation against model capabilities
  - Temperature and token limit enforcement
  - Stream-only model detection and handling
  - Default value management per model

### Documentation
- **README-MACHINE.md**: Comprehensive machine interface documentation
  - Complete API reference with examples
  - Integration guides for Rust, Python, JavaScript
  - Error handling and troubleshooting
  - Performance and security considerations
- **MACHINE-QUICK-REFERENCE.md**: Concise quick reference card
  - Command summary with examples
  - JSON response format reference
  - Integration code snippets
- **Updated CLI Documentation**: Enhanced with machine interface examples
  - Tauri sidecar integration examples
  - Configuration management guide
  - Advanced usage patterns

### Changed
- **CLI Module Structure**: Reorganized for better maintainability
  - Replaced monolithic `cli.py` with modular architecture
  - Clear separation between user and machine interfaces
  - Improved code organization and testability
- **Command Interface**: Enhanced command set with consistent patterns
  - All commands support both user and machine modes
  - Consistent parameter naming and behavior
  - Improved help system and documentation

### Fixed
- **Configuration Persistence**: Reliable configuration management
  - Proper file handling and error recovery
  - Atomic configuration updates
  - Cross-platform compatibility

## [0.1.2] - 2025-06-01

### Added
- **Comprehensive Test Suite**: Complete testing framework with 7 test scripts
  - `test_all_models.py`: Test all configured models with streaming and thinking capabilities
  - `test_single_model.py`: Individual model testing with custom configurations
  - `test_thinking.py`: Specialized tests for reasoning models with quality analysis
  - `test_providers.py`: Provider-specific testing with edge cases
  - `run_tests.py`: Unified test runner with multiple options
- **Quality Metrics**: Thinking quality scoring system (0.0-1.0) with step coverage analysis
- **Test Scenarios**: 5 reasoning test scenarios (basic_math, logic_puzzle, multi_step_problem, complex_reasoning, code_reasoning)
- **Enhanced Documentation**: Professional, user-friendly documentation with comprehensive testing guide
- **Model Validation**: Automatic model capability detection and validation
- **Performance Monitoring**: Response timing, token usage tracking, and streaming performance metrics

### Changed
- **Parameter Unification**: Merged `is_reasoning_model` and `supports_thinking` into single `supports_thinking` parameter
- **Provider Improvements**: Enhanced QwenProvider, OpenAIProvider, DeepSeekProvider, and AnthropicProvider
- **Stream-Only Support**: Automatic streaming enablement for models that require it (QwQ models)
- **Documentation Overhaul**: Cleaner, more professional documentation with reduced emoji usage
- **CLI Enhancements**: Improved model listing with unified "Thinking" column instead of separate "Reasoning" column

### Fixed
- **Anthropic Provider**: Fixed `_parse_usage` method to handle None values and streaming response parsing
- **Qwen Provider**: Removed problematic `enable_thinking` parameter that wasn't supported by OpenAI client
- **Client Validation**: Auto-remove temperature parameter for models that don't support it
- **Model Configuration**: Updated QwQ models to include proper `supports_thinking` and `stream_only` flags
- **Import Statements**: Fixed all documentation imports from `unified_llm` to `monollm`

### Removed
- **Deprecated Parameter**: Removed `is_reasoning_model` field from ModelInfo class and all configurations
- **Redundant Documentation**: Cleaned up excessive emoji usage and redundant sections

## [0.1.1] - 2025-01-26

### Added
- Initial release of MonoLLM framework
- Support for multiple LLM providers (OpenAI, Anthropic, Qwen, DeepSeek, Google, Volcengine)
- Unified interface for text generation and streaming
- Reasoning model support with thinking steps
- Command-line interface (CLI)
- Configuration management through JSON files
- Comprehensive error handling and retry mechanisms

### Features
- **Unified Interface**: Single API for multiple LLM providers
- **Streaming Support**: Real-time response streaming
- **Reasoning Models**: Support for models with thinking capabilities (QwQ, o1, DeepSeek R1)
- **Multi-turn Conversations**: Context-aware conversation handling
- **Proxy Support**: HTTP/SOCKS5 proxy configuration
- **Token Management**: Usage tracking and cost estimation
- **Type Safety**: Full type hints and Pydantic models

### Supported Providers
- **OpenAI**: GPT-4o, GPT-4o-mini, o1, o1-mini models
- **Anthropic**: Claude 3.5 Sonnet, Claude 3.5 Haiku models
- **Qwen/DashScope**: QwQ-32B, Qwen3 series models
- **DeepSeek**: DeepSeek V3, DeepSeek R1 models
- **Google**: Gemini 2.0 Flash, Gemini 2.5 Pro models (basic support)
- **Volcengine**: Doubao models (basic support)

## [Unreleased]

### Planned
- Enhanced multimodal support for Google Gemini models
- Additional provider integrations
- Advanced conversation management features
- Performance optimizations and caching
- Extended CLI functionality

---

## Release Notes

### Version 0.1.2 Highlights

This release focuses on testing infrastructure, documentation improvements, and parameter unification to provide a more robust and user-friendly experience.

**Key Achievements:**
- **Comprehensive Testing**: 7 specialized test scripts with quality metrics and performance monitoring
- **Parameter Unification**: Simplified model configuration with unified `supports_thinking` parameter
- **Enhanced Documentation**: Professional, clean documentation with comprehensive testing guide
- **Provider Stability**: Fixed multiple provider issues and improved error handling
- **Quality Analysis**: Advanced thinking quality scoring and step coverage analysis

**Testing Infrastructure:**
- Automated model discovery and validation
- Reasoning quality analysis with 0.0-1.0 scoring
- Provider-specific edge case testing
- Performance monitoring and metrics
- Unified test runner with multiple options

**Documentation Improvements:**
- Cleaner, more professional appearance
- Comprehensive testing guide
- User-friendly quickstart
- Reduced emoji usage for professional look
- Enhanced API documentation

### Version 0.1.1 Highlights

Initial release bringing together multiple LLM providers under a unified interface.

**Core Features:**
- **Multi-Provider Support**: OpenAI, Anthropic, Qwen, DeepSeek
- **Reasoning Models**: Special support for thinking-capable models (QwQ, o1, DeepSeek R1)
- **Streaming Support**: Real-time response streaming
- **Rich CLI**: Beautiful terminal interface with comprehensive commands
- **Type Safety**: Full type hints and Pydantic models

**Provider Status:**
- **Production Ready**: OpenAI, Anthropic, Qwen, DeepSeek
- **Basic Support**: Google Gemini, Volcengine

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and formatting guidelines
- Testing requirements
- Pull request process
- Issue reporting guidelines

## Support

- **Documentation**: https://cyborgoat.github.io/MonoLLM/
- **Issues**: https://github.com/cyborgoat/MonoLLM/issues
- **Repository**: https://github.com/cyborgoat/MonoLLM

---

**Created and maintained by [cyborgoat](https://github.com/cyborgoat)** • Licensed under [MIT License](LICENSE) 