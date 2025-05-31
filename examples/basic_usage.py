"""Basic usage example for UnifiedLLM."""

import asyncio
from unified_llm import UnifiedLLMClient, RequestConfig, Message


async def basic_generation():
    """Example of basic text generation."""
    print("=== Basic Generation ===")
    
    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="gpt-4o-mini",  # Use a cheaper model for examples
            temperature=0.7,
            max_tokens=100,
        )
        
        response = await client.generate(
            "Explain what artificial intelligence is in simple terms.",
            config
        )
        
        print(f"Response: {response.content}")
        if response.usage:
            print(f"Tokens used: {response.usage.total_tokens}")


async def streaming_example():
    """Example of streaming responses."""
    print("\n=== Streaming Example ===")
    
    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="gpt-4o-mini",
            stream=True,
        )
        
        print("Streaming response: ", end="")
        streaming_response = await client.generate_stream(
            "Tell me a short joke.",
            config
        )
        
        async for chunk in streaming_response:
            if chunk.content:
                print(chunk.content, end="", flush=True)
        
        print("\n")  # New line after streaming


async def conversation_example():
    """Example of multi-turn conversation."""
    print("\n=== Conversation Example ===")
    
    async with UnifiedLLMClient() as client:
        config = RequestConfig(model="gpt-4o-mini")
        
        messages = [
            Message(role="system", content="You are a helpful math tutor."),
            Message(role="user", content="What is 15 × 23?"),
        ]
        
        response = await client.generate(messages, config)
        print(f"Assistant: {response.content}")
        
        # Continue the conversation
        messages.append(Message(role="assistant", content=response.content))
        messages.append(Message(role="user", content="Can you show me how to calculate that step by step?"))
        
        response = await client.generate(messages, config)
        print(f"Assistant: {response.content}")


async def list_available_models():
    """Example of listing available models."""
    print("\n=== Available Models ===")
    
    client = UnifiedLLMClient()
    
    # List all providers
    providers = client.list_providers()
    print("Available providers:")
    for provider_id, provider_info in providers.items():
        print(f"  - {provider_id}: {provider_info.name}")
    
    # List models for each provider
    models = client.list_models()
    for provider_id, provider_models in models.items():
        if provider_models:  # Only show providers that have models
            provider_name = providers[provider_id].name
            print(f"\n{provider_name} models:")
            for model_id, model_info in provider_models.items():
                reasoning = " (Reasoning)" if model_info.is_reasoning_model else ""
                print(f"  - {model_id}: {model_info.name}{reasoning}")


async def main():
    """Run all examples."""
    try:
        # First, show available models
        await list_available_models()
        
        # Then run the examples
        await basic_generation()
        await streaming_example()
        await conversation_example()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set your API keys as environment variables.")
        print("For example: export OPENAI_API_KEY='your-api-key'")


if __name__ == "__main__":
    asyncio.run(main()) 