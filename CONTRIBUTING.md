# Contributing to UnifiedLLM

Thank you for your interest in contributing to UnifiedLLM! This project was created and is maintained by **[cyborgoat](https://github.com/cyborgoat)** (© 2025). We welcome contributions from everyone, whether you're fixing bugs, adding features, improving documentation, or helping with testing.

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+**
- **uv** (recommended) or **pip**
- **Git**

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/unified-llm.git
   cd unified-llm
   ```

2. **Install development dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync --dev
   
   # Or using pip
   pip install -e ".[dev]"
   ```

3. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

4. **Verify your setup**:
   ```bash
   # Run tests
   pytest
   
   # Check CLI
   unified-llm --help
   ```

## 🛠️ Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=monollm

# Run specific test file
pytest tests/test_client.py

# Run linting
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
mypy src/
```

### 4. Commit Your Changes

We use conventional commits for clear commit messages:

```bash
git add .
git commit -m "feat: add support for new provider"
# or
git commit -m "fix: resolve streaming timeout issue"
# or
git commit -m "docs: update installation guide"
```

**Commit Types:**
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear title and description
- Reference any related issues
- Include screenshots/examples if applicable

## 📝 Code Style Guidelines

### Python Code Style

We use the following tools for code quality:

- **Ruff**: For linting and formatting
- **MyPy**: For type checking
- **Pre-commit**: For automated checks

### Code Conventions

1. **Follow PEP 8** with these exceptions:
   - Line length: 88 characters (Black default)
   - Use double quotes for strings

2. **Type hints**: Always use type hints for function parameters and return values
   ```python
   async def generate(self, prompt: str, config: RequestConfig) -> LLMResponse:
       ...
   ```

3. **Docstrings**: Use Google-style docstrings
   ```python
   def example_function(param1: str, param2: int) -> bool:
       """Example function with Google-style docstring.
       
       Args:
           param1: Description of param1
           param2: Description of param2
           
       Returns:
           Description of return value
           
       Raises:
           ValueError: If param1 is empty
       """
       ...
   ```

4. **Async/await**: Use async/await consistently
   ```python
   # Good
   async def fetch_data():
       async with httpx.AsyncClient() as client:
           response = await client.get(url)
           return response.json()
   
   # Avoid
   def fetch_data():
       return asyncio.run(some_async_function())
   ```

## 🧪 Testing Guidelines

### Writing Tests

1. **Test file naming**: `test_*.py` in the `tests/` directory
2. **Test function naming**: `test_*` functions
3. **Use pytest fixtures** for common setup
4. **Mock external dependencies** (API calls, etc.)

### Test Structure

```python
import pytest
from unittest.mock import AsyncMock, patch
from monollm import UnifiedLLMClient, RequestConfig


class TestUnifiedLLMClient:
   """Test cases for UnifiedLLMClient."""

   @pytest.mark.asyncio
   async def test_generate_success(self, mock_client):
      """Test successful text generation."""
      # Arrange
      config = RequestConfig(model="test-model")
      expected_response = "Test response"

      # Act
      response = await mock_client.generate("Test prompt", config)

      # Assert
      assert response.content == expected_response
      assert response.model == "test-model"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=monollm --cov-report=html

# Run specific test
pytest tests/test_client.py::TestUnifiedLLMClient::test_generate_success

# Run tests matching pattern
pytest -k "test_generate"

# Run tests with verbose output
pytest -v
```

## 📚 Documentation Guidelines

### Code Documentation

1. **Docstrings**: All public functions, classes, and methods must have docstrings
2. **Type hints**: Use comprehensive type hints
3. **Comments**: Explain complex logic, not obvious code

### User Documentation

1. **Update relevant docs** when adding features
2. **Include examples** for new functionality
3. **Update CLI help** if adding commands
4. **Add to changelog** for user-facing changes

### Building Documentation

```bash
cd docs
make html

# Serve locally
cd _build/html
python -m http.server 8000
```

## 🔧 Adding New Providers

To add support for a new LLM provider:

### 1. Create Provider Class

```python
# src/monollm/providers/new_provider.py
from typing import AsyncIterator
from monollm.providers.base import BaseProvider
from monollm.core.models import LLMResponse, StreamingResponse, RequestConfig


class NewProvider(BaseProvider):
   """Provider for New LLM Service."""

   def __init__(self, api_key: str, base_url: str = None):
      self.api_key = api_key
      self.base_url = base_url or "https://api.newprovider.com/v1"

   async def generate(
           self,
           messages: list,
           config: RequestConfig
   ) -> LLMResponse:
      """Generate response using New Provider API."""
      # Implementation here
      pass

   async def generate_stream(
           self,
           messages: list,
           config: RequestConfig
   ) -> AsyncIterator[StreamingResponse]:
      """Generate streaming response."""
      # Implementation here
      pass
```

### 2. Add Provider Configuration

Update `config/models.json`:

```json
{
  "providers": {
    "newprovider": {
      "name": "New Provider",
      "base_url": "https://api.newprovider.com/v1",
      "uses_openai_protocol": true,
      "supports_streaming": true,
      "supports_mcp": false,
      "models": {
        "new-model-1": {
          "name": "New Model 1",
          "max_tokens": 4096,
          "supports_temperature": true,
          "supports_streaming": true,
          "is_reasoning_model": false
        }
      }
    }
  }
}
```

### 3. Register Provider

Update the provider registry in `src/unified_llm/core/client.py`.

### 4. Add Tests

Create comprehensive tests in `tests/test_providers.py`.

### 5. Update Documentation

- Add provider to README.md
- Update documentation
- Add examples

## 🐛 Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **Environment details**:
   - Python version
   - UnifiedLLM version
   - Operating system
   - Provider being used
5. **Error messages** and stack traces
6. **Minimal code example** that reproduces the issue

### Feature Requests

For feature requests, please include:

1. **Clear description** of the feature
2. **Use case** and motivation
3. **Proposed implementation** (if you have ideas)
4. **Examples** of how it would be used

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- **New provider implementations** (Google Gemini, Volcengine, etc.)
- **Bug fixes** and stability improvements
- **Performance optimizations**
- **Documentation improvements**

### Medium Priority
- **Additional CLI features**
- **Better error handling**
- **More comprehensive tests**
- **Example applications**

### Future Features
- **Function calling support**
- **Multimodal support** (images, audio)
- **Cost tracking and analytics**
- **Provider failover and load balancing**
- **Conversation memory management**

## 📋 Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] **Tests pass**: `pytest` runs without errors
- [ ] **Linting passes**: `ruff check` shows no issues
- [ ] **Type checking passes**: `mypy src/` shows no errors
- [ ] **Documentation updated** if needed
- [ ] **Changelog updated** for user-facing changes
- [ ] **Commit messages** follow conventional commit format
- [ ] **PR description** clearly explains the changes
- [ ] **Tests added** for new functionality

## 🤝 Code Review Process

1. **Automated checks** must pass (CI/CD)
2. **The maintainer (cyborgoat)** will review your PR
3. **Address feedback** promptly and professionally
4. **Squash commits** if requested before merging
5. **Celebrate** when your contribution is merged! 🎉

## 💬 Getting Help

If you need help or have questions:

1. **Check existing issues** and documentation first
2. **Open a discussion** on GitHub Discussions
3. **Contact the maintainer** via GitHub issues
4. **Ask questions** in your pull request

## 🙏 Recognition

Contributors are recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **Documentation** acknowledgments

## 👨‍💻 Maintainer

This project is created and maintained by **[cyborgoat](https://github.com/cyborgoat)**.

Thank you for contributing to UnifiedLLM! Your efforts help make this project better for everyone. 🚀 