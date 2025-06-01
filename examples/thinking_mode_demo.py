#!/usr/bin/env python3
"""
MonoLLM Thinking Mode Demo

This script demonstrates how to use thinking mode with reasoning models
like QwQ-32B to see the model's internal reasoning process.

The thinking mode shows:
1. The model's step-by-step reasoning process (thinking)
2. The final polished response (content)

This is particularly useful for:
- Mathematical problem solving
- Logical reasoning tasks
- Complex analysis where you want to see the thought process
"""

import asyncio
from monollm import UnifiedLLMClient, RequestConfig


async def demo_thinking_mode():
    """Demonstrate thinking mode with QwQ model."""
    
    print("🧠 MonoLLM Thinking Mode Demo")
    print("=" * 50)
    
    async with UnifiedLLMClient() as client:
        # Example 1: Mathematical problem
        print("\n📊 Example 1: Mathematical Problem")
        print("-" * 30)
        
        config = RequestConfig(
            model="qwq-32b",
            show_thinking=True,
            temperature=0.7,
            max_tokens=2000
        )
        
        response = await client.generate(
            "Solve this step by step: If a train travels 120 km in 2 hours, and then 180 km in 3 hours, what is its average speed for the entire journey?",
            config
        )
        
        if response.thinking:
            print("💭 Thinking Process:")
            print(response.thinking)
            print("\n" + "="*50)
        
        print("🎯 Final Answer:")
        print(response.content)
        
        # Example 2: Logical reasoning
        print("\n\n🧩 Example 2: Logical Reasoning")
        print("-" * 30)
        
        response = await client.generate(
            "Three friends - Alice, Bob, and Charlie - are standing in a line. Alice is not at the front. Bob is not at the back. Charlie is not in the middle. What is the order from front to back?",
            config
        )
        
        if response.thinking:
            print("💭 Thinking Process:")
            print(response.thinking)
            print("\n" + "="*50)
        
        print("🎯 Final Answer:")
        print(response.content)


async def demo_streaming_thinking():
    """Demonstrate streaming with thinking mode."""
    
    print("\n\n🌊 Streaming Thinking Mode Demo")
    print("=" * 50)
    
    async with UnifiedLLMClient() as client:
        config = RequestConfig(
            model="qwq-32b",
            show_thinking=True,
            stream=True,  # Enable streaming
            temperature=0.7
        )
        
        print("💭 Watch the thinking process in real-time:")
        print("-" * 40)
        
        streaming_response = await client.generate_stream(
            "Explain why the sky appears blue during the day but red/orange during sunset.",
            config
        )
        
        thinking_parts = []
        content_parts = []
        
        async for chunk in streaming_response:
            if chunk.thinking:
                print(f"💭 {chunk.thinking}", end="", flush=True)
                thinking_parts.append(chunk.thinking)
            elif chunk.content:
                if not content_parts:  # First content chunk
                    print("\n" + "="*50)
                    print("🎯 Final Answer:")
                print(chunk.content, end="", flush=True)
                content_parts.append(chunk.content)
        
        print("\n")  # Final newline


async def demo_comparison():
    """Compare responses with and without thinking mode."""
    
    print("\n\n🔄 Comparison: With vs Without Thinking")
    print("=" * 50)
    
    async with UnifiedLLMClient() as client:
        question = "What are the pros and cons of renewable energy?"
        
        # Without thinking
        print("🚫 Without Thinking Mode:")
        print("-" * 25)
        
        config_no_thinking = RequestConfig(
            model="qwq-32b",
            show_thinking=False,
            temperature=0.7,
            max_tokens=1000
        )
        
        response = await client.generate(question, config_no_thinking)
        print(response.content)
        
        # With thinking
        print("\n\n🧠 With Thinking Mode:")
        print("-" * 20)
        
        config_with_thinking = RequestConfig(
            model="qwq-32b",
            show_thinking=True,
            temperature=0.7,
            max_tokens=1000
        )
        
        response = await client.generate(question, config_with_thinking)
        
        if response.thinking:
            print("💭 Thinking Process:")
            print(response.thinking[:500] + "..." if len(response.thinking) > 500 else response.thinking)
            print("\n" + "="*50)
        
        print("🎯 Final Answer:")
        print(response.content)


async def main():
    """Run all demonstrations."""
    try:
        await demo_thinking_mode()
        await demo_streaming_thinking()
        await demo_comparison()
        
        print("\n\n✨ Demo completed!")
        print("\nKey takeaways:")
        print("• Thinking mode shows the model's reasoning process")
        print("• QwQ models automatically use streaming mode")
        print("• Use show_thinking=True to see internal reasoning")
        print("• Streaming allows real-time viewing of the thought process")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("• Set up your Qwen API key in environment variables")
        print("• Installed MonoLLM with: pip install -e .")


if __name__ == "__main__":
    asyncio.run(main()) 