#!/usr/bin/env python3
"""
MonoLLM Core Exceptions - Custom exception classes for error handling.

This module defines a comprehensive hierarchy of custom exceptions for the
MonoLLM framework. These exceptions provide detailed error information,
structured error handling, and consistent error reporting across all
components of the system.

Exception Hierarchy:
    MonoLLMError (base)
    ├── ProviderError
    │   ├── RateLimitError
    │   ├── AuthenticationError
    │   ├── ModelNotFoundError
    │   └── QuotaExceededError
    ├── ConfigurationError
    ├── ConnectionError
    └── ValidationError

Key Features:
    - Structured error information with provider, model, and error codes
    - HTTP status code mapping for provider errors
    - Metadata support for additional error context
    - Consistent error message formatting
    - Support for error recovery and retry logic

Error Handling Patterns:
    All exceptions include optional metadata for debugging and logging.
    Provider-specific errors include status codes and error codes for
    proper error classification and handling.

Example Usage:
    Basic error handling:
        >>> try:
        ...     response = await client.generate(prompt, config)
        ... except ProviderError as e:
        ...     print(f"Provider {e.provider} error: {e.message}")
        ...     if e.status_code == 429:
        ...         print("Rate limit exceeded")
        ... except MonoLLMError as e:
        ...     print(f"General error: {e.message}")

    Specific error handling:
        >>> try:
        ...     response = await client.generate(prompt, config)
        ... except RateLimitError as e:
        ...     print(f"Rate limited, retry after {e.retry_after} seconds")
        ... except AuthenticationError as e:
        ...     print("Invalid API key")
        ... except ModelNotFoundError as e:
        ...     print(f"Available models: {e.available_models}")

Author: cyborgoat
License: MIT License
Copyright: (c) 2025 cyborgoat

For more information, visit: https://github.com/cyborgoat/unified-llm
Documentation: https://cyborgoat.github.io/unified-llm/api/exceptions.html
"""

from typing import Optional, Dict, Any


class MonoLLMError(Exception):
    """
    Base exception for all unified LLM errors.

    This is the root exception class for all errors in the MonoLLM framework.
    It provides a consistent interface for error handling and includes optional
    metadata for debugging and logging purposes.

    Attributes:
        message (str): Human-readable error message
        provider (Optional[str]): Provider associated with the error
        model (Optional[str]): Model associated with the error
        error_code (Optional[str]): Structured error code for programmatic handling
        metadata (Dict[str, Any]): Additional error context and debugging information

    Examples:
        >>> raise MonoLLMError(
        ...     "Something went wrong",
        ...     provider="openai",
        ...     model="gpt-4o",
        ...     error_code="general_error",
        ...     metadata={"request_id": "req_123"}
        ... )
    """

    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        error_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a MonoLLM error.

        Args:
            message: Human-readable error message
            provider: Optional provider identifier
            model: Optional model identifier
            error_code: Optional structured error code
            metadata: Optional additional error context
        """
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.model = model
        self.error_code = error_code
        self.metadata = metadata or {}


class ProviderError(MonoLLMError):
    """
    Error from an LLM provider.

    This exception represents errors that originate from LLM provider APIs,
    including HTTP errors, API-specific errors, and service unavailability.
    It includes HTTP status codes for proper error classification.

    Attributes:
        status_code (Optional[int]): HTTP status code from the provider API

    Common Status Codes:
        - 400: Bad Request (invalid parameters)
        - 401: Unauthorized (invalid API key)
        - 402: Payment Required (quota exceeded)
        - 404: Not Found (model not found)
        - 429: Too Many Requests (rate limit exceeded)
        - 500: Internal Server Error (provider issue)
        - 503: Service Unavailable (temporary outage)

    Examples:
        >>> raise ProviderError(
        ...     "Invalid API key",
        ...     provider="openai",
        ...     status_code=401,
        ...     error_code="invalid_api_key"
        ... )
    """

    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a provider error.

        Args:
            message: Human-readable error message
            provider: Provider identifier
            model: Optional model identifier
            status_code: Optional HTTP status code
            error_code: Optional structured error code
            metadata: Optional additional error context
        """
        super().__init__(message, provider, model, error_code, metadata)
        self.status_code = status_code


class ConfigurationError(MonoLLMError):
    """
    Error in configuration.

    This exception is raised when there are issues with configuration files,
    environment variables, or other configuration-related problems that
    prevent the system from operating correctly.

    Attributes:
        config_type (Optional[str]): Type of configuration that caused the error

    Examples:
        >>> raise ConfigurationError(
        ...     "Missing API key for OpenAI provider",
        ...     config_type="api_key"
        ... )
    """

    def __init__(
        self,
        message: str,
        config_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a configuration error.

        Args:
            message: Human-readable error message
            config_type: Optional type of configuration
            metadata: Optional additional error context
        """
        super().__init__(message, metadata=metadata)
        self.config_type = config_type


class RateLimitError(ProviderError):
    """
    Rate limit exceeded error.

    This exception is raised when the provider's rate limit has been exceeded.
    It includes information about when the client can retry the request.

    Attributes:
        retry_after (Optional[int]): Seconds to wait before retrying

    Examples:
        >>> raise RateLimitError(
        ...     "Rate limit exceeded",
        ...     provider="openai",
        ...     retry_after=60
        ... )
    """

    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        retry_after: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a rate limit error.

        Args:
            message: Human-readable error message
            provider: Provider identifier
            model: Optional model identifier
            retry_after: Optional seconds to wait before retrying
            metadata: Optional additional error context
        """
        super().__init__(message, provider, model, 429, "rate_limit", metadata)
        self.retry_after = retry_after


class AuthenticationError(ProviderError):
    """
    Authentication error.

    This exception is raised when authentication with a provider fails,
    typically due to invalid or missing API keys.

    Examples:
        >>> raise AuthenticationError(
        ...     "Invalid API key",
        ...     provider="anthropic"
        ... )
    """

    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize an authentication error.

        Args:
            message: Human-readable error message
            provider: Provider identifier
            model: Optional model identifier
            metadata: Optional additional error context
        """
        super().__init__(message, provider, model, 401, "authentication", metadata)


class ModelNotFoundError(ProviderError):
    """
    Model not found error.

    This exception is raised when a requested model is not available
    from the specified provider. It includes a list of available models
    to help with error recovery.

    Attributes:
        available_models (list): List of available model identifiers

    Examples:
        >>> raise ModelNotFoundError(
        ...     "Model 'gpt-5' not found",
        ...     provider="openai",
        ...     model="gpt-5",
        ...     available_models=["gpt-4o", "gpt-4", "gpt-3.5-turbo"]
        ... )
    """

    def __init__(
        self,
        message: str,
        provider: str,
        model: str,
        available_models: Optional[list] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a model not found error.

        Args:
            message: Human-readable error message
            provider: Provider identifier
            model: Model identifier that was not found
            available_models: Optional list of available models
            metadata: Optional additional error context
        """
        super().__init__(message, provider, model, 404, "model_not_found", metadata)
        self.available_models = available_models or []


class QuotaExceededError(ProviderError):
    """
    Quota exceeded error.

    This exception is raised when the provider's usage quota has been
    exceeded, typically requiring payment or plan upgrade to continue.

    Attributes:
        quota_type (Optional[str]): Type of quota that was exceeded

    Examples:
        >>> raise QuotaExceededError(
        ...     "Monthly token quota exceeded",
        ...     provider="openai",
        ...     quota_type="monthly_tokens"
        ... )
    """

    def __init__(
        self,
        message: str,
        provider: str,
        model: Optional[str] = None,
        quota_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a quota exceeded error.

        Args:
            message: Human-readable error message
            provider: Provider identifier
            model: Optional model identifier
            quota_type: Optional type of quota exceeded
            metadata: Optional additional error context
        """
        super().__init__(message, provider, model, 402, "quota_exceeded", metadata)
        self.quota_type = quota_type


class ConnectionError(MonoLLMError):
    """
    Connection error.

    This exception is raised when there are network connectivity issues,
    timeouts, or other connection-related problems when communicating
    with provider APIs.

    Attributes:
        timeout (Optional[float]): Timeout value that was exceeded

    Examples:
        >>> raise ConnectionError(
        ...     "Connection timeout",
        ...     provider="anthropic",
        ...     timeout=30.0
        ... )
    """

    def __init__(
        self,
        message: str,
        provider: Optional[str] = None,
        timeout: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a connection error.

        Args:
            message: Human-readable error message
            provider: Optional provider identifier
            timeout: Optional timeout value that was exceeded
            metadata: Optional additional error context
        """
        super().__init__(message, provider, metadata=metadata)
        self.timeout = timeout


class ValidationError(MonoLLMError):
    """
    Validation error.

    This exception is raised when input validation fails, such as
    invalid parameter values, malformed requests, or constraint violations.

    Attributes:
        field (Optional[str]): Field name that failed validation
        value (Optional[Any]): Value that failed validation

    Examples:
        >>> raise ValidationError(
        ...     "Temperature must be between 0.0 and 2.0",
        ...     field="temperature",
        ...     value=3.0
        ... )
    """

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a validation error.

        Args:
            message: Human-readable error message
            field: Optional field name that failed validation
            value: Optional value that failed validation
            metadata: Optional additional error context
        """
        super().__init__(message, metadata=metadata)
        self.field = field
        self.value = value
