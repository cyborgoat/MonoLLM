# Changelog

All notable changes to the UnifiedLLM project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation with Sphinx and GitHub Pages deployment
- Professional README with badges, examples, and detailed feature descriptions
- Contributing guide with development workflow and code style guidelines
- Comprehensive headers and documentation for all source files
- MIT License with proper copyright attribution

### Changed
- Updated copyright year to 2025
- Updated author attribution to cyborgoat
- Enhanced CLI with better help text and parameter descriptions
- Improved error messages and user feedback throughout the system

### Documentation
- Added comprehensive Sphinx documentation system
- Created detailed API reference documentation
- Added installation, configuration, and usage guides
- Created extensive examples and use case documentation
- Set up automatic GitHub Pages deployment

## [0.1.1] - 2025-05-31

### Added
- Enhanced CLI interface with rich terminal output
- Comprehensive error handling with custom exception hierarchy
- Support for reasoning models with thinking step display
- Streaming response support for real-time output
- Multi-turn conversation support with message history
- Proxy configuration support for HTTP/SOCKS5 proxies
- Token usage tracking and display
- Configuration management through JSON files and environment variables

### Providers
- ✅ **OpenAI**: Full support including reasoning models (o1, o1-mini)
- ✅ **Anthropic**: Claude models with MCP integration support
- ✅ **Qwen/DashScope**: Complete implementation including QwQ reasoning model
- ✅ **DeepSeek**: Full support including DeepSeek-R1 reasoning model
- 🚧 **Google Gemini**: Planned implementation
- 🚧 **Volcengine**: Planned implementation

### Features
- **Unified Interface**: Single API for all providers
- **Streaming Support**: Real-time response streaming
- **Reasoning Models**: Special handling for thinking steps
- **Temperature Control**: Creativity adjustment when supported
- **Token Management**: Cost control with output limits
- **MCP Integration**: Model Context Protocol support
- **OpenAI Protocol**: Preference for compatible APIs
- **Rich CLI**: Beautiful terminal interface with tables and formatting

### Technical
- Async/await architecture for optimal performance
- Pydantic models for type safety and validation
- Comprehensive error handling and retry mechanisms
- Rich console output with progress indicators
- Configuration validation and environment variable support

## [0.1.0] - 2025-05-31

### Added
- Initial project structure and core framework
- Basic client implementation for unified LLM access
- Core data models and type definitions
- Configuration system with JSON file support
- Basic CLI implementation
- Provider abstraction layer
- Initial OpenAI provider implementation

### Infrastructure
- Python 3.13+ support with modern async patterns
- UV package manager integration
- Pre-commit hooks for code quality
- Basic testing framework setup
- Initial documentation structure

### Core Components
- `UnifiedLLMClient`: Main client interface
- `RequestConfig`: Configuration management
- `LLMResponse`: Response handling
- `Message`: Conversation message structure
- Basic exception hierarchy

---

## Release Notes

### Version 0.1.1 Highlights

This release represents a major milestone in the UnifiedLLM project, bringing it from a basic framework to a production-ready system with comprehensive features and documentation.

**🎯 Key Achievements:**
- **Multi-Provider Support**: Successfully implemented 4 major LLM providers
- **Reasoning Model Support**: Special handling for advanced reasoning models
- **Professional Documentation**: Complete Sphinx documentation with GitHub Pages
- **Rich CLI Experience**: Beautiful terminal interface with comprehensive commands
- **Production Ready**: Robust error handling, configuration management, and testing

**🚀 Provider Status:**
- **Ready for Production**: OpenAI, Anthropic, Qwen, DeepSeek
- **In Development**: Google Gemini, Volcengine

**📚 Documentation:**
- Complete API reference with examples
- Installation and configuration guides
- CLI documentation with all commands
- Contributing guidelines for developers
- Comprehensive examples and use cases

**🛠️ Developer Experience:**
- Type-safe API with Pydantic models
- Comprehensive error handling
- Rich console output and progress indicators
- Easy configuration through environment variables
- Extensive testing and validation

### Migration Guide

#### From 0.1.0 to 0.1.1

**Breaking Changes:**
- None - this release maintains full backward compatibility

**New Features:**
- Enhanced CLI with new commands and options
- Streaming support for real-time responses
- Reasoning model support with thinking steps
- Improved error messages and handling

**Recommended Updates:**
```python
# Old way (still works)
response = await client.generate("Hello", RequestConfig(model="gpt-4o"))

# New way (recommended)
async with UnifiedLLMClient() as client:
    config = RequestConfig(model="gpt-4o", stream=True)
    async for chunk in await client.generate_stream("Hello", config):
        print(chunk.content, end="")
```

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and formatting guidelines
- Testing requirements
- Pull request process
- Issue reporting guidelines

## Support

- **Documentation**: https://cyborgoat.github.io/unified-llm/
- **Issues**: https://github.com/cyborgoat/unified-llm/issues
- **Discussions**: https://github.com/cyborgoat/unified-llm/discussions

---

**Created and maintained by [cyborgoat](https://github.com/cyborgoat)** • Licensed under [MIT License](LICENSE) 