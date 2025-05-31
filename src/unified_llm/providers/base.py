"""Base provider interface for the unified LLM framework."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncIterator
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from unified_llm.core.models import (
    Message, 
    LLMResponse, 
    StreamingResponse, 
    StreamChunk,
    RequestConfig,
    ProviderInfo,
    ProxyConfig,
    TimeoutConfig,
    RetryConfig
)
from unified_llm.core.exceptions import (
    ProviderError,
    AuthenticationError,
    RateLimitError,
    ConnectionError,
    QuotaExceededError
)


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(
        self,
        provider_info: ProviderInfo,
        api_key: Optional[str] = None,
        base_url_override: Optional[str] = None,
        proxy_config: Optional[ProxyConfig] = None,
        timeout_config: Optional[TimeoutConfig] = None,
        retry_config: Optional[RetryConfig] = None,
    ):
        """Initialize the provider.
        
        Args:
            provider_info: Information about this provider
            api_key: API key for authentication
            base_url_override: Override for the base URL
            proxy_config: Proxy configuration
            timeout_config: Timeout configuration
            retry_config: Retry configuration
        """
        self.provider_info = provider_info
        self.api_key = api_key
        self.base_url = base_url_override or provider_info.base_url
        self.proxy_config = proxy_config or ProxyConfig()
        self.timeout_config = timeout_config or TimeoutConfig()
        self.retry_config = retry_config or RetryConfig()
        
        # Create HTTP client
        self._create_http_client()
    
    def _create_http_client(self) -> None:
        """Create the HTTP client with appropriate configuration."""
        # Configure proxy
        proxy = None
        if self.proxy_config.enabled:
            if self.proxy_config.type == "socks5":
                proxy_url = f"socks5://"
                if self.proxy_config.username and self.proxy_config.password:
                    proxy_url += f"{self.proxy_config.username}:{self.proxy_config.password}@"
                proxy_url += f"{self.proxy_config.host}:{self.proxy_config.port}"
            else:
                proxy_url = f"{self.proxy_config.type}://"
                if self.proxy_config.username and self.proxy_config.password:
                    proxy_url += f"{self.proxy_config.username}:{self.proxy_config.password}@"
                proxy_url += f"{self.proxy_config.host}:{self.proxy_config.port}"
            
            proxy = proxy_url
        
        # Configure timeouts - provide all four parameters explicitly
        timeout = httpx.Timeout(
            connect=self.timeout_config.connect,
            read=self.timeout_config.read,
            write=self.timeout_config.write,
            pool=self.timeout_config.connect,  # Use connect timeout for pool timeout
        )
        
        # Create client with proper parameters
        client_kwargs = {
            "timeout": timeout,
            "follow_redirects": True,
        }
        
        if proxy:
            client_kwargs["proxy"] = proxy
        
        self.client = httpx.AsyncClient(**client_kwargs)
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the provider name."""
        pass
    
    @abstractmethod
    async def generate(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> LLMResponse:
        """Generate a response from the LLM.
        
        Args:
            messages: List of conversation messages
            config: Request configuration
            
        Returns:
            LLM response
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> StreamingResponse:
        """Generate a streaming response from the LLM.
        
        Args:
            messages: List of conversation messages
            config: Request configuration
            
        Returns:
            Streaming response
        """
        pass
    
    def _get_retry_decorator(self):
        """Get the retry decorator with current configuration."""
        return retry(
            stop=stop_after_attempt(self.retry_config.max_attempts),
            wait=wait_exponential(multiplier=self.retry_config.backoff_factor),
            retry=retry_if_exception_type((
                httpx.HTTPStatusError,
                httpx.ConnectError,
                httpx.TimeoutException,
            )),
        )
    
    def _handle_http_error(self, error: httpx.HTTPStatusError) -> None:
        """Handle HTTP errors and convert to appropriate exceptions."""
        status_code = error.response.status_code
        message = f"HTTP {status_code}: {error.response.text}"
        
        if status_code == 401:
            raise AuthenticationError(
                message=message,
                provider=self.get_provider_name(),
            )
        elif status_code == 402:
            raise QuotaExceededError(
                message=message,
                provider=self.get_provider_name(),
            )
        elif status_code == 429:
            retry_after = error.response.headers.get("retry-after")
            raise RateLimitError(
                message=message,
                provider=self.get_provider_name(),
                retry_after=int(retry_after) if retry_after else None,
            )
        elif status_code in self.retry_config.retry_on_status:
            raise ProviderError(
                message=message,
                provider=self.get_provider_name(),
                status_code=status_code,
            )
        else:
            raise ProviderError(
                message=message,
                provider=self.get_provider_name(),
                status_code=status_code,
            )
    
    def _handle_connection_error(self, error: Exception) -> None:
        """Handle connection errors."""
        if isinstance(error, httpx.ConnectError):
            raise ConnectionError(
                message=f"Failed to connect to {self.base_url}: {error}",
                provider=self.get_provider_name(),
            )
        elif isinstance(error, httpx.TimeoutException):
            raise ConnectionError(
                message=f"Request timed out: {error}",
                provider=self.get_provider_name(),
                timeout=self.timeout_config.read,
            )
        else:
            raise ProviderError(
                message=f"Unexpected error: {error}",
                provider=self.get_provider_name(),
            )
    
    async def close(self) -> None:
        """Close the HTTP client."""
        if hasattr(self, 'client'):
            await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close() 