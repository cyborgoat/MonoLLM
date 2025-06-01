"""OpenAI provider implementation."""

from typing import AsyncIterator, List, Dict, Any, Optional

import httpx
from openai import AsyncOpenAI

from monollm.core.models import (
    LLMResponse,
    StreamingResponse,
    RequestConfig,
    Message,
    Usage,
    StreamChunk,
)
from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the OpenAI provider."""
        super().__init__(*args, **kwargs)
        
        # Create OpenAI client
        self.openai_client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            http_client=self.client,
        )
    
    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "openai"
    
    def _convert_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """Convert internal messages to OpenAI format."""
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    
    def _build_request_params(self, messages: List[Message], config: RequestConfig) -> Dict[str, Any]:
        """Build request parameters for OpenAI API."""
        params = {
            "model": config.model,
            "messages": self._convert_messages(messages),
            "stream": config.stream,
        }
        
        # Add optional parameters
        if config.temperature is not None:
            params["temperature"] = config.temperature
        
        if config.max_tokens is not None:
            params["max_tokens"] = config.max_tokens
        
        # For reasoning models like o1, handle thinking mode
        model_info = self.provider_info.models.get(config.model)
        if model_info and model_info.supports_thinking:
            # o1 models don't support temperature or max_tokens in the traditional sense
            if "o1" in config.model:
                # Remove temperature and max_tokens for o1 models
                params.pop("temperature", None)
                params.pop("max_tokens", None)
        
        return params
    
    def _parse_usage(self, usage_data: Any) -> Optional[Usage]:
        """Parse usage information from OpenAI response."""
        if not usage_data:
            return None
        
        return Usage(
            prompt_tokens=usage_data.prompt_tokens,
            completion_tokens=usage_data.completion_tokens,
            total_tokens=usage_data.total_tokens,
            reasoning_tokens=getattr(usage_data, 'reasoning_tokens', None),
        )
    
    async def generate(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> LLMResponse:
        """Generate a response from OpenAI."""
        try:
            params = self._build_request_params(messages, config)
            
            response = await self.openai_client.chat.completions.create(**params)
            
            # Extract content and metadata
            content = response.choices[0].message.content or ""
            usage = self._parse_usage(response.usage)
            
            # Check for thinking steps in reasoning models
            thinking = None
            if hasattr(response.choices[0].message, 'reasoning'):
                thinking = response.choices[0].message.reasoning
            
            return LLMResponse(
                content=content,
                provider=self.get_provider_name(),
                model=config.model,
                usage=usage,
                thinking=thinking if config.show_thinking else None,
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
        """Generate streaming chunks from OpenAI."""
        try:
            params = self._build_request_params(messages, config)
            
            stream = await self.openai_client.chat.completions.create(**params)
            
            content_buffer = ""
            thinking_buffer = ""
            
            async for chunk in stream:
                if not chunk.choices:
                    continue
                
                choice = chunk.choices[0]
                
                # Handle content delta
                if choice.delta.content:
                    content_delta = choice.delta.content
                    content_buffer += content_delta
                    
                    yield StreamChunk(
                        content=content_delta,
                        is_complete=False,
                    )
                
                # Handle reasoning delta (for reasoning models)
                if hasattr(choice.delta, 'reasoning') and choice.delta.reasoning:
                    thinking_delta = choice.delta.reasoning
                    thinking_buffer += thinking_delta
                    
                    if config.show_thinking:
                        yield StreamChunk(
                            content="",
                            thinking=thinking_delta,
                            is_complete=False,
                        )
                
                # Handle completion
                if choice.finish_reason:
                    usage = self._parse_usage(getattr(chunk, 'usage', None))
                    
                    yield StreamChunk(
                        content="",
                        is_complete=True,
                        metadata={
                            "finish_reason": choice.finish_reason,
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
        """Generate a streaming response from OpenAI."""
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
        if hasattr(self, 'openai_client'):
            await self.openai_client.close() 