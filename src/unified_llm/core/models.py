"""Core data models for the unified LLM framework."""

from typing import Any, Dict, List, Optional, Union, AsyncIterator, Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ModelInfo(BaseModel):
    """Information about a specific LLM model."""
    
    model_config = ConfigDict(frozen=True)
    
    name: str = Field(..., description="Display name of the model")
    max_tokens: int = Field(..., description="Maximum output tokens")
    supports_temperature: bool = Field(default=True, description="Whether temperature control is supported")
    supports_streaming: bool = Field(default=True, description="Whether streaming is supported")
    is_reasoning_model: bool = Field(default=False, description="Whether this is a reasoning model")
    supports_thinking: bool = Field(default=False, description="Whether thinking steps are available")


class ProviderInfo(BaseModel):
    """Information about an LLM provider."""
    
    model_config = ConfigDict(frozen=True)
    
    name: str = Field(..., description="Display name of the provider")
    base_url: str = Field(..., description="Base URL for API requests")
    uses_openai_protocol: bool = Field(default=False, description="Whether provider uses OpenAI-compatible API")
    supports_streaming: bool = Field(default=True, description="Whether provider supports streaming")
    supports_mcp: bool = Field(default=False, description="Whether provider supports MCP integration")
    models: Dict[str, ModelInfo] = Field(default_factory=dict, description="Available models")


class ProxyConfig(BaseModel):
    """Configuration for proxy settings."""
    
    enabled: bool = Field(default=False, description="Whether proxy is enabled")
    type: Literal["http", "https", "socks5"] = Field(default="http", description="Proxy type")
    host: Optional[str] = Field(default=None, description="Proxy host")
    port: Optional[int] = Field(default=None, description="Proxy port")
    username: Optional[str] = Field(default=None, description="Proxy username")
    password: Optional[str] = Field(default=None, description="Proxy password")


class TimeoutConfig(BaseModel):
    """Configuration for request timeouts."""
    
    connect: int = Field(default=30, description="Connection timeout in seconds")
    read: int = Field(default=60, description="Read timeout in seconds")
    write: int = Field(default=60, description="Write timeout in seconds")


class RetryConfig(BaseModel):
    """Configuration for retry behavior."""
    
    max_attempts: int = Field(default=3, description="Maximum retry attempts")
    backoff_factor: float = Field(default=1.0, description="Backoff factor for retries")
    retry_on_status: List[int] = Field(
        default_factory=lambda: [429, 500, 502, 503, 504],
        description="HTTP status codes to retry on"
    )


class RequestConfig(BaseModel):
    """Configuration for LLM requests."""
    
    model: str = Field(..., description="Model identifier")
    provider: Optional[str] = Field(default=None, description="Provider identifier")
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, gt=0, description="Maximum output tokens")
    stream: bool = Field(default=False, description="Whether to stream the response")
    show_thinking: bool = Field(default=False, description="Whether to show thinking steps for reasoning models")
    proxy: Optional[ProxyConfig] = Field(default=None, description="Proxy configuration")
    timeout: Optional[TimeoutConfig] = Field(default=None, description="Timeout configuration")
    retry: Optional[RetryConfig] = Field(default=None, description="Retry configuration")
    mcp_tools: Optional[List[Dict[str, Any]]] = Field(default=None, description="MCP tools to use")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class Message(BaseModel):
    """A message in the conversation."""
    
    role: Literal["system", "user", "assistant"] = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class Usage(BaseModel):
    """Token usage information."""
    
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(..., description="Number of tokens in the completion")
    total_tokens: int = Field(..., description="Total number of tokens")
    reasoning_tokens: Optional[int] = Field(default=None, description="Number of reasoning tokens (for reasoning models)")


class LLMResponse(BaseModel):
    """Response from an LLM."""
    
    content: str = Field(..., description="The generated content")
    provider: str = Field(..., description="Provider that generated the response")
    model: str = Field(..., description="Model that generated the response")
    usage: Optional[Usage] = Field(default=None, description="Token usage information")
    thinking: Optional[str] = Field(default=None, description="Thinking steps (for reasoning models)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="When the response was created")
    request_id: Optional[str] = Field(default=None, description="Unique identifier for the request")


class StreamChunk(BaseModel):
    """A chunk of streamed response."""
    
    content: str = Field(..., description="Content chunk")
    is_complete: bool = Field(default=False, description="Whether this is the final chunk")
    thinking: Optional[str] = Field(default=None, description="Thinking content (for reasoning models)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class StreamingResponse:
    """Streaming response from an LLM."""
    
    def __init__(
        self,
        chunks: AsyncIterator[StreamChunk],
        provider: str,
        model: str,
        request_id: Optional[str] = None,
    ):
        self.chunks = chunks
        self.provider = provider
        self.model = model
        self.request_id = request_id
        self.created_at = datetime.now()
        
    async def __aiter__(self) -> AsyncIterator[StreamChunk]:
        """Async iterator for streaming chunks."""
        async for chunk in self.chunks:
            yield chunk
    
    async def collect(self) -> LLMResponse:
        """Collect all chunks into a single response."""
        content_parts = []
        thinking_parts = []
        final_metadata = {}
        usage = None
        
        async for chunk in self.chunks:
            if chunk.content:
                content_parts.append(chunk.content)
            if chunk.thinking:
                thinking_parts.append(chunk.thinking)
            if chunk.metadata:
                final_metadata.update(chunk.metadata)
            if chunk.is_complete and "usage" in chunk.metadata:
                usage = Usage(**chunk.metadata["usage"])
        
        return LLMResponse(
            content="".join(content_parts),
            provider=self.provider,
            model=self.model,
            usage=usage,
            thinking="".join(thinking_parts) if thinking_parts else None,
            metadata=final_metadata,
            created_at=self.created_at,
            request_id=self.request_id,
        ) 