"""Google Gemini provider implementation."""

import json
from typing import List, Dict, Any, Optional, AsyncIterator
import httpx

from .base import BaseProvider
from ..core.models import (
    Message,
    LLMResponse,
    StreamingResponse,
    StreamChunk,
    RequestConfig,
    Usage,
)
from ..core.exceptions import ProviderError


class GoogleProvider(BaseProvider):
    """Google Gemini provider implementation using direct HTTP API."""
    
    def __init__(self, *args, **kwargs):
        """Initialize the Google provider."""
        super().__init__(*args, **kwargs)
        
        # Use direct API endpoint instead of SDK
        self.api_base = "https://generativelanguage.googleapis.com/v1beta"
    
    def get_provider_name(self) -> str:
        """Get the provider name."""
        return "google"
    
    def _convert_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Convert internal messages to Google format."""
        google_messages = []
        
        for msg in messages:
            if msg.role == "system":
                # Google doesn't have system role, treat as user message
                google_messages.append({
                    "role": "user",
                    "parts": [{"text": f"[System]: {msg.content}"}]
                })
            elif msg.role == "user":
                google_messages.append({
                    "role": "user", 
                    "parts": [{"text": msg.content}]
                })
            elif msg.role == "assistant":
                google_messages.append({
                    "role": "model",
                    "parts": [{"text": msg.content}]
                })
        
        return google_messages
    
    def _build_generation_config(self, config: RequestConfig) -> Dict[str, Any]:
        """Build generation config for Google API."""
        gen_config = {}
        
        if config.temperature is not None:
            gen_config["temperature"] = config.temperature
        
        if config.max_tokens is not None:
            gen_config["maxOutputTokens"] = config.max_tokens
        
        return gen_config
    
    def _build_safety_settings(self) -> List[Dict[str, Any]]:
        """Build safety settings (less restrictive)."""
        return [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    
    def _parse_usage(self, usage_metadata: Any) -> Optional[Usage]:
        """Parse usage information from Google response."""
        if not usage_metadata:
            return None
        
        return Usage(
            prompt_tokens=usage_metadata.get('promptTokenCount', 0),
            completion_tokens=usage_metadata.get('candidatesTokenCount', 0),
            total_tokens=usage_metadata.get('totalTokenCount', 0),
        )
    
    async def generate(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> LLMResponse:
        """Generate a response from Google Gemini."""
        try:
            # Convert messages to Google format
            google_messages = self._convert_messages(messages)
            
            # Build request payload
            payload = {
                "contents": google_messages,
                "generationConfig": self._build_generation_config(config),
                "safetySettings": self._build_safety_settings()
            }
            
            # Make API request
            url = f"{self.api_base}/models/{config.model}:generateContent"
            params = {"key": self.api_key}
            
            response = await self.client.post(
                url,
                json=payload,
                params=params
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract content
            content = ""
            if result.get("candidates") and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if candidate.get("content") and candidate["content"].get("parts"):
                    content = candidate["content"]["parts"][0].get("text", "")
            
            # Parse usage if available
            usage = self._parse_usage(result.get("usageMetadata"))
            
            return LLMResponse(
                content=content,
                provider=self.get_provider_name(),
                model=config.model,
                usage=usage,
                request_id=config.metadata.get("request_id") if config.metadata else None,
            )
        
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)
        except Exception as e:
            self._handle_connection_error(e)
    
    async def _stream_chunks(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> AsyncIterator[StreamChunk]:
        """Generate streaming chunks from Google Gemini."""
        try:
            # Convert messages to Google format
            google_messages = self._convert_messages(messages)
            
            # Build request payload
            payload = {
                "contents": google_messages,
                "generationConfig": self._build_generation_config(config),
                "safetySettings": self._build_safety_settings()
            }
            
            # Make streaming API request
            url = f"{self.api_base}/models/{config.model}:streamGenerateContent"
            params = {"key": self.api_key}
            
            content_buffer = ""
            
            async with self.client.stream(
                "POST",
                url,
                json=payload,
                params=params
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.strip():
                        # Remove "data: " prefix if present
                        if line.startswith("data: "):
                            line = line[6:]
                        
                        try:
                            chunk_data = json.loads(line)
                            
                            # Extract content from chunk
                            if chunk_data.get("candidates") and len(chunk_data["candidates"]) > 0:
                                candidate = chunk_data["candidates"][0]
                                if candidate.get("content") and candidate["content"].get("parts"):
                                    content_delta = candidate["content"]["parts"][0].get("text", "")
                                    if content_delta:
                                        content_buffer += content_delta
                                        
                                        yield StreamChunk(
                                            content=content_delta,
                                            is_complete=False,
                                        )
                                
                                # Check for finish reason
                                if candidate.get("finishReason"):
                                    yield StreamChunk(
                                        content="",
                                        is_complete=True,
                                        metadata={
                                            "finish_reason": candidate["finishReason"],
                                        }
                                    )
                                    break
                        
                        except json.JSONDecodeError:
                            continue  # Skip invalid JSON lines
            
            # Send completion chunk if we didn't get a finish reason
            yield StreamChunk(
                content="",
                is_complete=True,
                metadata={
                    "finish_reason": "stop",
                }
            )
        
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)
        except Exception as e:
            self._handle_connection_error(e)
    
    async def generate_stream(
        self,
        messages: List[Message],
        config: RequestConfig,
    ) -> StreamingResponse:
        """Generate a streaming response from Google Gemini."""
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