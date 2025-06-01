"""Anthropic provider implementation."""

from typing import List, Dict, Any, Optional, AsyncIterator

import httpx
from anthropic import AsyncAnthropic

from .base import BaseProvider
from ..core.models import (
    Message,
    LLMResponse,
    StreamingResponse,
    StreamChunk,
    RequestConfig,
    Usage,
)


class AnthropicProvider(BaseProvider):
    """Anthropic provider implementation."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the Anthropic provider."""
        super().__init__(*args, **kwargs)
        
        # Create Anthropic client
        self.anthropic_client = AsyncAnthropic(
            api_key=self.api_key,
            base_url=self.base_url,
            http_client=self.client,
        )
    
    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "anthropic"
    
    def _convert_messages(self, messages: List[Message]) -> tuple[List[Dict[str, str]], Optional[str]]:
        """Convert internal messages to Anthropic format.
        
        Returns:
            Tuple of (messages_list, system_message)
        """
        system_message = None
        anthropic_messages = []
        
        for msg in messages:
            if msg.role == "system":
                # Anthropic handles system messages separately
                system_message = msg.content
            else:
                anthropic_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        return anthropic_messages, system_message
    
    def _build_request_params(self, messages: List[Message], config: RequestConfig) -> Dict[str, Any]:
        """Build request parameters for Anthropic API."""
        anthropic_messages, system_message = self._convert_messages(messages)
        
        params = {
            "model": config.model,
            "messages": anthropic_messages,
            "max_tokens": config.max_tokens or 4096,  # Anthropic requires max_tokens
            "stream": config.stream,
        }
        
        # Add system message if present
        if system_message:
            params["system"] = system_message
        
        # Add optional parameters
        if config.temperature is not None:
            params["temperature"] = config.temperature
        
        return params
    
    def _parse_usage(self, usage_data: Any) -> Optional[Usage]:
        """Parse usage information from Anthropic response."""
        if not usage_data:
            return None
        
        return Usage(
            prompt_tokens=getattr(usage_data, 'input_tokens', 0),
            completion_tokens=getattr(usage_data, 'output_tokens', 0),
            total_tokens=getattr(usage_data, 'input_tokens', 0) + getattr(usage_data, 'output_tokens', 0),
        )
    
    async def generate(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> LLMResponse:
        """Generate a response from Anthropic."""
        try:
            params = self._build_request_params(messages, config)
            
            response = await self.anthropic_client.messages.create(**params)
            
            # Extract content and metadata
            content = ""
            if response.content and len(response.content) > 0:
                content = response.content[0].text if hasattr(response.content[0], 'text') else str(response.content[0])
            
            usage = self._parse_usage(response.usage)
            
            return LLMResponse(
                content=content,
                provider=self.get_provider_name(),
                model=config.model,
                usage=usage,
                request_id=config.metadata.get("request_id") if config.metadata else None,
            )
        
        except Exception as e:
            if isinstance(e, httpx.HTTPStatusError):
                self._handle_http_error(e)
            else:
                self._handle_connection_error(e)
    
    async def _stream_chunks(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> AsyncIterator[StreamChunk]:
        """Generate streaming chunks from Anthropic."""
        try:
            params = self._build_request_params(messages, config)
            
            stream = await self.anthropic_client.messages.create(**params)
            
            content_buffer = ""
            
            async for chunk in stream:
                if chunk.type == "content_block_delta":
                    if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                        content_delta = chunk.delta.text
                        content_buffer += content_delta
                        
                        yield StreamChunk(
                            content=content_delta,
                            is_complete=False,
                        )
                
                elif chunk.type == "message_delta":
                    # Handle completion with usage information
                    if hasattr(chunk, 'usage'):
                        usage = self._parse_usage(chunk.usage)
                        
                        yield StreamChunk(
                            content="",
                            is_complete=True,
                            metadata={
                                "stop_reason": getattr(chunk, 'delta', {}).get('stop_reason'),
                                "usage": usage.model_dump() if usage else None,
                            }
                        )
        
        except Exception as e:
            if isinstance(e, httpx.HTTPStatusError):
                self._handle_http_error(e)
            else:
                self._handle_connection_error(e)
    
    async def generate_stream(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> StreamingResponse:
        """Generate a streaming response from Anthropic."""
        chunks = self._stream_chunks(messages, config)
        
        return StreamingResponse(
            chunks=chunks,
            provider=self.get_provider_name(),
            model=config.model,
            request_id=config.metadata.get("request_id") if config.metadata else None,
        )
    
    async def close(self) -> None:
        """Close the provider."""
        await super().close()
        if hasattr(self, 'anthropic_client'):
            await self.anthropic_client.close() 