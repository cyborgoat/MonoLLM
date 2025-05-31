"""Basic usage example for UnifiedLLM with Qwen models."""

import asyncio
from unified_llm import UnifiedLLMClient, RequestConfig, Message


async def basic_generation():
    """Example of basic text generation with Qwen."""
    print("=== Basic Generation with Qwen ===")

    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="qwq-32b",  # Use Qwen's reasoning model
            temperature=0.7,
            max_tokens=100,
        )

        response = await client.generate(
            "Explain what artificial intelligence is in simple terms.", config
        )

        print(f"Response: {response.content}")
        if response.usage:
            print(f"Tokens used: {response.usage.total_tokens}")


async def streaming_example():
    """Example of streaming responses with Qwen."""
    print("\n=== Streaming Example with Qwen ===")

    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="qwq-32b",  # Use Qwen Plus for streaming
            stream=True,
        )

        print("Streaming response: ", end="")
        streaming_response = await client.generate_stream(
            "Tell me a short joke.", config
        )

        async for chunk in streaming_response:
            if chunk.content:
                print(chunk.content, end="", flush=True)

        print("\n")  # New line after streaming


async def conversation_example():
    """Example of multi-turn conversation with Qwen."""
    print("\n=== Conversation Example with Qwen ===")

    async with UnifiedLLMClient() as client:
        config = RequestConfig(model="qwq-32b")

        messages = [
            Message(role="system", content="You are a helpful math tutor."),
            Message(role="user", content="What is 15 × 23?"),
        ]

        response = await client.generate(messages, config)
        print(f"Assistant: {response.content}")

        # Continue the conversation
        messages.append(Message(role="assistant", content=response.content))
        messages.append(
            Message(
                role="user",
                content="Can you show me how to calculate that step by step?",
            )
        )

        response = await client.generate(messages, config)
        print(f"Assistant: {response.content}")


async def reasoning_example():
    """Example of using Qwen's reasoning capabilities."""
    print("\n=== Reasoning Example with QwQ ===")

    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="qwq-32b",  # QwQ is Qwen's reasoning model
            show_thinking=True,  # Show the reasoning process
            max_tokens=500,
        )

        response = await client.generate(
            "Solve this step by step: If a train travels 60 miles in 45 minutes, what is its speed in miles per hour?",
            config,
        )

        if response.thinking:
            print("Thinking process:")
            print(response.thinking)
            print("\nFinal answer:")

        print(response.content)

        if response.usage:
            print(f"Tokens used: {response.usage.total_tokens}")


async def list_available_models():
    """Example of listing available models."""
    print("\n=== Available Models ===")

    client = UnifiedLLMClient()

    # List all providers
    providers = client.list_providers()
    print("Available providers:")
    for provider_id, provider_info in providers.items():
        print(f"  - {provider_id}: {provider_info.name}")

    # List models for each provider, focusing on Qwen
    models = client.list_models()
    for provider_id, provider_models in models.items():
        if provider_models:  # Only show providers that have models
            provider_name = providers[provider_id].name
            print(f"\n{provider_name} models:")
            for model_id, model_info in provider_models.items():
                reasoning = " (Reasoning)" if model_info.is_reasoning_model else ""
                streaming = " (Streaming)" if model_info.supports_streaming else ""
                print(f"  - {model_id}: {model_info.name}{reasoning}{streaming}")


async def main():
    """Run all examples."""
    try:
        # First, show available models
        await list_available_models()

        # Then run the examples
        await basic_generation()
        await streaming_example()
        await conversation_example()
        await reasoning_example()

    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have set your Qwen API key as environment variable.")
        print("For example: export DASHSCOPE_API_KEY='your-api-key'")


if __name__ == "__main__":
    asyncio.run(main())
