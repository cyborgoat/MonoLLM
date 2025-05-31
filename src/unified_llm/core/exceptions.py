"""Custom exceptions for the unified LLM framework."""

from typing import Optional, Dict, Any


class UnifiedLLMError(Exception):
    """Base exception for all unified LLM errors."""
    
    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        error_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.model = model
        self.error_code = error_code
        self.metadata = metadata or {}


class ProviderError(UnifiedLLMError):
    """Error from an LLM provider."""
    
    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, provider, model, error_code, metadata)
        self.status_code = status_code


class ConfigurationError(UnifiedLLMError):
    """Error in configuration."""
    
    def __init__(
        self,
        message: str,
        config_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, metadata=metadata)
        self.config_type = config_type


class RateLimitError(ProviderError):
    """Rate limit exceeded error."""
    
    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        retry_after: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, provider, model, 429, "rate_limit", metadata)
        self.retry_after = retry_after


class AuthenticationError(ProviderError):
    """Authentication error."""
    
    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, provider, model, 401, "authentication", metadata)


class ModelNotFoundError(ProviderError):
    """Model not found error."""
    
    def __init__(
        self,
        message: str,
        provider: str,
        model: str,
        available_models: Optional[list] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, provider, model, 404, "model_not_found", metadata)
        self.available_models = available_models or []


class QuotaExceededError(ProviderError):
    """Quota exceeded error."""
    
    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        quota_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, provider, model, 402, "quota_exceeded", metadata)
        self.quota_type = quota_type


class ConnectionError(UnifiedLLMError):
    """Connection error."""
    
    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        timeout: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, provider, metadata=metadata)
        self.timeout = timeout


class ValidationError(UnifiedLLMError):
    """Validation error."""
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, metadata=metadata)
        self.field = field
        self.value = value 