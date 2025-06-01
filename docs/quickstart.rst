Quick Start Guide
=================

This guide will get you up and running with MonoLLM in just a few minutes.

Prerequisites
-------------

Before you begin, make sure you have:

1. **Python 3.13+** installed
2. **MonoLLM** installed (see :doc:`installation`)
3. **API keys** for at least one provider

Setting Up Your First Provider
-------------------------------

Let's start with Qwen, which offers excellent reasoning capabilities:

1. **Get your API key** from `DashScope <https://dashscope.aliyun.com/>`_
2. **Set the environment variable**:

   .. code-block:: bash

      export DASHSCOPE_API_KEY="your-dashscope-api-key"

3. **Verify the setup**:

   .. code-block:: bash

      monollm list-providers

Your First Generation
---------------------

Let's create your first text generation:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def main():
       # Initialize the client
       async with UnifiedLLMClient() as client:
           # Configure the request
           config = RequestConfig(
               model="qwq-32b",  # Qwen's reasoning model
               temperature=0.7,
               max_tokens=500,
           )
           
           # Generate response
           response = await client.generate(
               "Explain the concept of machine learning in simple terms.",
               config
           )
           
           # Print the result
           print("Response:", response.content)
           print(f"Provider: {response.provider}")
           print(f"Model: {response.model}")
           
           if response.usage:
               print(f"Tokens used: {response.usage.total_tokens}")

   # Run the example
   asyncio.run(main())

Save this as ``first_example.py`` and run:

.. code-block:: bash

   python first_example.py

Streaming Responses
-------------------

For real-time responses, use streaming:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def streaming_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwen-plus",
               stream=True,  # Enable streaming
           )
           
           print("Streaming response: ", end="", flush=True)
           
           streaming_response = await client.generate_stream(
               "Tell me a short story about a robot learning to paint.",
               config
           )
           
           # Process each chunk as it arrives
           async for chunk in streaming_response:
               if chunk.content:
                   print(chunk.content, end="", flush=True)
           
           print("\n")  # New line after streaming

   asyncio.run(streaming_example())

Using Reasoning Models
----------------------

Qwen's QwQ model can show its reasoning process:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def reasoning_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwq-32b",
               show_thinking=True,  # Show reasoning steps
               max_tokens=1000,
           )
           
           response = await client.generate(
               "If a train travels 120 miles in 2 hours, and then 180 miles in 3 hours, what is its average speed for the entire journey?",
               config
           )
           
           # Show the thinking process
           if response.thinking:
               print("🤔 Thinking process:")
               print(response.thinking)
               print("\n" + "="*50 + "\n")
           
           print("📝 Final answer:")
           print(response.content)

   asyncio.run(reasoning_example())

Multi-turn Conversations
------------------------

Build conversations with context:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig, Message

   async def conversation_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwen-plus")
           
           # Start with a system message and user question
           messages = [
               Message(role="system", content="You are a helpful math tutor."),
               Message(role="user", content="What is 15 × 23?"),
           ]
           
           # Get first response
           response = await client.generate(messages, config)
           print("Tutor:", response.content)
           
           # Continue the conversation
           messages.append(Message(role="assistant", content=response.content))
           messages.append(Message(
               role="user", 
               content="Can you show me how to calculate that step by step?"
           ))
           
           # Get follow-up response
           response = await client.generate(messages, config)
           print("Tutor:", response.content)

   asyncio.run(conversation_example())

Command Line Interface
----------------------

MonoLLM also provides a powerful CLI:

**List available providers:**

.. code-block:: bash

   monollm list-providers

**List models for a specific provider:**

.. code-block:: bash

   monollm list-models --provider qwen

**Generate text:**

.. code-block:: bash

   monollm generate "What is artificial intelligence?" --model qwq-32b

**Stream responses:**

.. code-block:: bash

   monollm generate "Tell me a joke" --model qwen-plus --stream

**Use reasoning with thinking:**

.. code-block:: bash

   monollm generate "Solve: 2x + 5 = 13" --model qwq-32b --thinking

**Set temperature and max tokens:**

.. code-block:: bash

   monollm generate "Write a haiku about coding" --model qwen-plus --temperature 0.9 --max-tokens 100

Working with Multiple Providers
-------------------------------

You can easily switch between providers:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def multi_provider_example():
       async with UnifiedLLMClient() as client:
           prompt = "What is the capital of France?"
           
           # Try different providers
           providers_models = [
               ("qwen", "qwen-plus"),
               ("anthropic", "claude-3-5-sonnet-20241022"),
               ("openai", "gpt-4o"),
           ]
           
           for provider, model in providers_models:
               try:
                   config = RequestConfig(model=model)
                   response = await client.generate(prompt, config)
                   print(f"{provider.upper()}: {response.content[:100]}...")
               except Exception as e:
                   print(f"{provider.upper()}: Error - {e}")

   asyncio.run(multi_provider_example())

Error Handling
--------------

Always handle potential errors:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig
   from monollm.core.exceptions import MonoLLMError, ProviderError

   async def error_handling_example():
       async with UnifiedLLMClient() as client:
           try:
               config = RequestConfig(model="non-existent-model")
               response = await client.generate("Hello", config)
               print(response.content)
           
           except MonoLLMError as e:
               print(f"MonoLLM Error: {e}")
           except ProviderError as e:
               print(f"Provider Error: {e}")
           except Exception as e:
               print(f"Unexpected Error: {e}")

   asyncio.run(error_handling_example())

Best Practices
--------------

1. **Use async context managers**: Always use ``async with UnifiedLLMClient()`` for proper resource management.

2. **Handle errors gracefully**: Wrap API calls in try-catch blocks.

3. **Set reasonable limits**: Use ``max_tokens`` to control costs and response length.

4. **Choose the right model**: Use reasoning models for complex problems, regular models for simple tasks.

5. **Use streaming for long responses**: Improve user experience with real-time output.

6. **Store API keys securely**: Use environment variables or secure key management.

Next Steps
----------

Now that you're familiar with the basics, explore:

* :doc:`configuration` - Advanced configuration options
* :doc:`providers` - Detailed provider documentation
* :doc:`examples` - More comprehensive examples
* :doc:`api/client` - Complete API reference
* :doc:`cli` - Full CLI documentation

Common Use Cases
----------------

**Content Generation:**

.. code-block:: python

   config = RequestConfig(model="qwen-plus", temperature=0.8, max_tokens=1000)
   response = await client.generate("Write a blog post about renewable energy", config)

**Code Assistance:**

.. code-block:: python

   config = RequestConfig(model="qwq-32b", temperature=0.2)
   response = await client.generate("Explain this Python function: def fibonacci(n):", config)

**Data Analysis:**

.. code-block:: python

   config = RequestConfig(model="qwq-32b", show_thinking=True)
   response = await client.generate("Analyze this sales data and find trends: [data]", config)

**Creative Writing:**

.. code-block:: python

   config = RequestConfig(model="qwen-plus", temperature=1.0, max_tokens=2000)
   response = await client.generate("Write a science fiction short story", config)

You're now ready to build amazing applications with MonoLLM! 🚀 