#!/usr/bin/env python3
"""
MonoLLM Core Models - Data structures and type definitions.

This module defines the core data models and type definitions used throughout
the MonoLLM framework. It provides Pydantic-based models for configuration,
requests, responses, and metadata, ensuring type safety and data validation
across the entire system.

Key Components:
    - Model and Provider Information: Metadata about LLM models and providers
    - Configuration Models: Settings for requests, timeouts, retries, and proxies
    - Message and Conversation Models: Chat message structures
    - Response Models: LLM responses for both streaming and non-streaming
    - Usage and Metrics Models: Token usage and performance tracking

Data Validation:
    All models use Pydantic for automatic validation, serialization, and
    deserialization. This ensures data integrity and provides clear error
    messages when invalid data is encountered.

Thread Safety:
    All models are immutable by default (frozen=True) to ensure thread safety
    and prevent accidental modifications during concurrent operations.

Example Usage:
    Creating a request configuration:
        >>> config = RequestConfig(
        ...     model="gpt-4o",
        ...     temperature=0.7,
        ...     max_tokens=1000,
        ...     stream=True
        ... )

    Creating a conversation message:
        >>> message = Message(
        ...     role="user",
        ...     content="Hello, how are you?"
        ... )

    Working with responses:
        >>> response = LLMResponse(
        ...     content="I'm doing well, thank you!",
        ...     provider="openai",
        ...     model="gpt-4o",
        ...     usage=Usage(prompt_tokens=10, completion_tokens=8, total_tokens=18)
        ... )

Author: cyborgoat
License: MIT License
Copyright: (c) 2025 cyborgoat

For more information, visit: https://github.com/cyborgoat/unified-llm
Documentation: https://cyborgoat.github.io/unified-llm/api/models.html
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, AsyncIterator, Literal

from pydantic import BaseModel, Field, ConfigDict


class ModelInfo(BaseModel):
    """
    Information about a specific LLM model.
    
    This class encapsulates metadata about an individual language model,
    including its capabilities, limitations, and supported features. It's
    used by the client to validate requests and provide appropriate
    configuration options.
    
    Attributes:
        name (str): Human-readable display name of the model
        max_tokens (int): Maximum number of output tokens the model can generate
        supports_temperature (bool): Whether the model supports temperature control
        supports_streaming (bool): Whether the model can stream responses
        is_reasoning_model (bool): Whether this is a reasoning/thinking model
        supports_thinking (bool): Whether thinking steps are available for display
    
    Examples:
        >>> model = ModelInfo(
        ...     name="GPT-4 Omni",
        ...     max_tokens=4096,
        ...     supports_temperature=True,
        ...     supports_streaming=True,
        ...     is_reasoning_model=False,
        ...     supports_thinking=False
        ... )
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Display name of the model")
    max_tokens: int = Field(..., description="Maximum output tokens")
    supports_temperature: bool = Field(
        default=True, description="Whether temperature control is supported"
    )
    supports_streaming: bool = Field(
        default=True, description="Whether streaming is supported"
    )
    is_reasoning_model: bool = Field(
        default=False, description="Whether this is a reasoning model"
    )
    supports_thinking: bool = Field(
        default=False, description="Whether thinking steps are available"
    )


class ProviderInfo(BaseModel):
    """
    Information about an LLM provider.
    
    This class contains metadata about a language model provider, including
    its capabilities, API configuration, and available models. It's used
    during provider initialization and for capability checking.
    
    Attributes:
        name (str): Human-readable display name of the provider
        base_url (str): Base URL for API requests to this provider
        uses_openai_protocol (bool): Whether provider uses OpenAI-compatible API
        supports_streaming (bool): Whether provider supports streaming responses
        supports_mcp (bool): Whether provider supports Model Context Protocol
        models (Dict[str, ModelInfo]): Dictionary of available models
    
    Examples:
        >>> provider = ProviderInfo(
        ...     name="OpenAI",
        ...     base_url="https://api.openai.com/v1",
        ...     uses_openai_protocol=True,
        ...     supports_streaming=True,
        ...     supports_mcp=True,
        ...     models={"gpt-4o": ModelInfo(...)}
        ... )
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(..., description="Display name of the provider")
    base_url: str = Field(..., description="Base URL for API requests")
    uses_openai_protocol: bool = Field(
        default=False, description="Whether provider uses OpenAI-compatible API"
    )
    supports_streaming: bool = Field(
        default=True, description="Whether provider supports streaming"
    )
    supports_mcp: bool = Field(
        default=False, description="Whether provider supports MCP integration"
    )
    models: Dict[str, ModelInfo] = Field(
        default_factory=dict, description="Available models"
    )


class ProxyConfig(BaseModel):
    """
    Configuration for proxy settings.
    
    This class defines proxy configuration options for network requests.
    It supports HTTP, HTTPS, and SOCKS5 proxies with optional authentication.
    
    Attributes:
        enabled (bool): Whether proxy is enabled
        type (Literal): Type of proxy (http, https, socks5)
        host (Optional[str]): Proxy server hostname or IP address
        port (Optional[int]): Proxy server port number
        username (Optional[str]): Username for proxy authentication
        password (Optional[str]): Password for proxy authentication
    
    Examples:
        >>> proxy = ProxyConfig(
        ...     enabled=True,
        ...     type="http",
        ...     host="proxy.example.com",
        ...     port=8080,
        ...     username="user",
        ...     password="pass"
        ... )
    """

    enabled: bool = Field(default=False, description="Whether proxy is enabled")
    type: Literal["http", "https", "socks5"] = Field(
        default="http", description="Proxy type"
    )
    host: Optional[str] = Field(default=None, description="Proxy host")
    port: Optional[int] = Field(default=None, description="Proxy port")
    username: Optional[str] = Field(default=None, description="Proxy username")
    password: Optional[str] = Field(default=None, description="Proxy password")


class TimeoutConfig(BaseModel):
    """
    Configuration for request timeouts.
    
    This class defines timeout settings for various aspects of HTTP requests
    to LLM providers. Different timeout values can be set for connection
    establishment, reading responses, and writing requests.
    
    Attributes:
        connect (int): Connection timeout in seconds
        read (int): Read timeout in seconds for receiving responses
        write (int): Write timeout in seconds for sending requests
    
    Examples:
        >>> timeout = TimeoutConfig(
        ...     connect=30,
        ...     read=120,
        ...     write=60
        ... )
    """

    connect: int = Field(default=30, description="Connection timeout in seconds")
    read: int = Field(default=60, description="Read timeout in seconds")
    write: int = Field(default=60, description="Write timeout in seconds")


class RetryConfig(BaseModel):
    """
    Configuration for retry behavior.
    
    This class defines retry settings for failed requests, including the
    maximum number of attempts, backoff strategy, and which HTTP status
    codes should trigger retries.
    
    Attributes:
        max_attempts (int): Maximum number of retry attempts
        backoff_factor (float): Exponential backoff factor for retry delays
        retry_on_status (List[int]): HTTP status codes that trigger retries
    
    Examples:
        >>> retry = RetryConfig(
        ...     max_attempts=3,
        ...     backoff_factor=2.0,
        ...     retry_on_status=[429, 500, 502, 503, 504]
        ... )
    """

    max_attempts: int = Field(default=3, description="Maximum retry attempts")
    backoff_factor: float = Field(default=1.0, description="Backoff factor for retries")
    retry_on_status: List[int] = Field(
        default_factory=lambda: [429, 500, 502, 503, 504],
        description="HTTP status codes to retry on",
    )


class RequestConfig(BaseModel):
    """
    Configuration for LLM requests.
    
    This class encapsulates all configuration options for making requests
    to LLM providers. It includes model selection, generation parameters,
    streaming options, and various system-level configurations.
    
    Attributes:
        model (str): Model identifier to use for generation
        provider (Optional[str]): Specific provider to use (auto-detected if None)
        temperature (Optional[float]): Temperature for response creativity (0.0-2.0)
        max_tokens (Optional[int]): Maximum number of tokens to generate
        stream (bool): Whether to stream the response in real-time
        show_thinking (bool): Whether to show thinking steps for reasoning models
        proxy (Optional[ProxyConfig]): Proxy configuration override
        timeout (Optional[TimeoutConfig]): Timeout configuration override
        retry (Optional[RetryConfig]): Retry configuration override
        mcp_tools (Optional[List[Dict]]): MCP tools to make available
        metadata (Optional[Dict]): Additional request metadata
    
    Examples:
        >>> config = RequestConfig(
        ...     model="gpt-4o",
        ...     temperature=0.7,
        ...     max_tokens=1000,
        ...     stream=True,
        ...     show_thinking=False
        ... )
    """

    model: str = Field(..., description="Model identifier")
    provider: Optional[str] = Field(default=None, description="Provider identifier")
    temperature: Optional[float] = Field(
        default=None, ge=0.0, le=2.0, description="Temperature for generation"
    )
    max_tokens: Optional[int] = Field(
        default=None, gt=0, description="Maximum output tokens"
    )
    stream: bool = Field(default=False, description="Whether to stream the response")
    show_thinking: bool = Field(
        default=False, description="Whether to show thinking steps for reasoning models"
    )
    proxy: Optional[ProxyConfig] = Field(
        default=None, description="Proxy configuration"
    )
    timeout: Optional[TimeoutConfig] = Field(
        default=None, description="Timeout configuration"
    )
    retry: Optional[RetryConfig] = Field(
        default=None, description="Retry configuration"
    )
    mcp_tools: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="MCP tools to use"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class Message(BaseModel):
    """
    A message in a conversation.
    
    This class represents a single message in a conversation with an LLM.
    Messages have roles (system, user, assistant) and content, and can
    include additional metadata for tracking and processing.
    
    Attributes:
        role (Literal): Role of the message sender (system, user, assistant)
        content (str): Text content of the message
        metadata (Optional[Dict]): Additional metadata for the message
    
    Examples:
        >>> system_msg = Message(
        ...     role="system",
        ...     content="You are a helpful assistant."
        ... )
        >>> user_msg = Message(
        ...     role="user",
        ...     content="What is the capital of France?"
        ... )
        >>> assistant_msg = Message(
        ...     role="assistant",
        ...     content="The capital of France is Paris."
        ... )
    """

    role: Literal["system", "user", "assistant"] = Field(
        ..., description="Role of the message sender"
    )
    content: str = Field(..., description="Content of the message")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class Usage(BaseModel):
    """
    Token usage information.
    
    This class tracks token consumption for LLM requests, including
    prompt tokens, completion tokens, and special reasoning tokens
    for models that support thinking steps.
    
    Attributes:
        prompt_tokens (int): Number of tokens in the input prompt
        completion_tokens (int): Number of tokens in the generated completion
        total_tokens (int): Total number of tokens used
        reasoning_tokens (Optional[int]): Number of reasoning tokens (for reasoning models)
    
    Examples:
        >>> usage = Usage(
        ...     prompt_tokens=50,
        ...     completion_tokens=100,
        ...     total_tokens=150,
        ...     reasoning_tokens=25
        ... )
    """

    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(
        ..., description="Number of tokens in the completion"
    )
    total_tokens: int = Field(..., description="Total number of tokens")
    reasoning_tokens: Optional[int] = Field(
        default=None, description="Number of reasoning tokens (for reasoning models)"
    )


class LLMResponse(BaseModel):
    """
    Response from an LLM.
    
    This class encapsulates a complete response from a language model,
    including the generated content, metadata about the generation,
    token usage information, and optional thinking steps for reasoning models.
    
    Attributes:
        content (str): The generated text content
        provider (str): Provider that generated the response
        model (str): Model that generated the response
        usage (Optional[Usage]): Token usage information
        thinking (Optional[str]): Thinking steps for reasoning models
        metadata (Optional[Dict]): Additional response metadata
        created_at (datetime): Timestamp when the response was created
        request_id (Optional[str]): Unique identifier for the request
    
    Examples:
        >>> response = LLMResponse(
        ...     content="The capital of France is Paris.",
        ...     provider="openai",
        ...     model="gpt-4o",
        ...     usage=Usage(prompt_tokens=10, completion_tokens=8, total_tokens=18)
        ... )
    """

    content: str = Field(..., description="The generated content")
    provider: str = Field(..., description="Provider that generated the response")
    model: str = Field(..., description="Model that generated the response")
    usage: Optional[Usage] = Field(default=None, description="Token usage information")
    thinking: Optional[str] = Field(
        default=None, description="Thinking steps (for reasoning models)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="When the response was created"
    )
    request_id: Optional[str] = Field(
        default=None, description="Unique identifier for the request"
    )


class StreamChunk(BaseModel):
    """
    A chunk of streamed response.
    
    This class represents a single chunk in a streaming response from an LLM.
    Chunks contain incremental content and metadata, allowing for real-time
    display of generated text as it becomes available.
    
    Attributes:
        content (str): Content chunk (may be empty for metadata-only chunks)
        is_complete (bool): Whether this is the final chunk in the stream
        thinking (Optional[str]): Thinking content for reasoning models
        metadata (Optional[Dict]): Additional chunk metadata
    
    Examples:
        >>> chunk = StreamChunk(
        ...     content="Hello",
        ...     is_complete=False
        ... )
        >>> final_chunk = StreamChunk(
        ...     content="!",
        ...     is_complete=True
        ... )
    """

    content: str = Field(..., description="Content chunk")
    is_complete: bool = Field(
        default=False, description="Whether this is the final chunk"
    )
    thinking: Optional[str] = Field(
        default=None, description="Thinking content (for reasoning models)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )


class StreamingResponse:
    """
    Streaming response from an LLM.
    
    This class manages a streaming response from a language model, providing
    an async iterator interface for consuming chunks as they arrive. It also
    supports collecting all chunks into a single LLMResponse object.
    
    Attributes:
        chunks (AsyncIterator[StreamChunk]): Async iterator of response chunks
        provider (str): Provider that generated the response
        model (str): Model that generated the response
        request_id (Optional[str]): Unique identifier for the request
        created_at (datetime): Timestamp when the response was created
    
    Examples:
        >>> async for chunk in streaming_response:
        ...     if chunk.content:
        ...         print(chunk.content, end="", flush=True)
        
        >>> # Or collect all chunks into a single response
        >>> complete_response = await streaming_response.collect()
    """

    def __init__(
        self,
        chunks: AsyncIterator[StreamChunk],
        provider: str,
        model: str,
        request_id: Optional[str] = None,
    ):
        """
        Initialize a streaming response.
        
        Args:
            chunks: Async iterator of response chunks
            provider: Provider that generated the response
            model: Model that generated the response
            request_id: Optional unique identifier for the request
        """
        self.chunks = chunks
        self.provider = provider
        self.model = model
        self.request_id = request_id
        self.created_at = datetime.now()

    async def __aiter__(self) -> AsyncIterator[StreamChunk]:
        """
        Async iterator for streaming chunks.
        
        Yields:
            StreamChunk: Individual chunks of the streaming response
        """
        async for chunk in self.chunks:
            yield chunk

    async def collect(self) -> LLMResponse:
        """
        Collect all chunks into a single response.
        
        This method consumes the entire stream and combines all chunks
        into a single LLMResponse object. Useful when you want to work
        with the complete response after streaming is finished.
        
        Returns:
            LLMResponse: Complete response with all chunks combined
        
        Note:
            This method can only be called once per StreamingResponse instance,
            as it consumes the underlying async iterator.
        """
        content_parts = []
        thinking_parts = []
        final_metadata = {}

        async for chunk in self.chunks:
            if chunk.content:
                content_parts.append(chunk.content)
            if chunk.thinking:
                thinking_parts.append(chunk.thinking)
            if chunk.metadata:
                final_metadata.update(chunk.metadata)

        return LLMResponse(
            content="".join(content_parts),
            provider=self.provider,
            model=self.model,
            thinking="".join(thinking_parts) if thinking_parts else None,
            metadata=final_metadata if final_metadata else None,
            created_at=self.created_at,
            request_id=self.request_id,
        )
