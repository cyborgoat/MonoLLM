"""UnifiedLLM - A framework for unified access to multiple LLM providers."""

from .core.client import UnifiedLLMClient
from .core.models import (
    LLMResponse,
    StreamingResponse,
    ModelInfo,
    ProviderInfo,
    RequestConfig,
    Message,
)
from .core.exceptions import (
    UnifiedLLMError,
    ProviderError,
    ConfigurationError,
    RateLimitError,
)

__version__ = "0.1.0"
__all__ = [
    "UnifiedLLMClient",
    "LLMResponse",
    "StreamingResponse",
    "ModelInfo",
    "ProviderInfo",
    "RequestConfig",
    "Message",
    "UnifiedLLMError",
    "ProviderError",
    "ConfigurationError",
    "RateLimitError",
] 