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
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="gpt-4o",
               temperature=0.7,
               max_tokens=100,
           )
           
           response = await client.generate(
               "Explain quantum computing briefly.",
               config
           )
           
           print(f"Content: {response.content}")
           if response.usage:
               print(f"Tokens used: {response.usage.total_tokens}")
               print(f"Cost estimate: ${response.usage.total_tokens * 0.00001:.5f}")

   asyncio.run(main())

Streaming Responses
-------------------

For real-time responses, use streaming:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def main():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="gpt-4o",
               stream=True,
               temperature=0.7,
           )
           
           async for chunk in await client.generate_stream(
               "Tell me a short story about a robot.",
               config
           ):
               if chunk.content:
                   print(chunk.content, end="", flush=True)
           
           print()  # New line after streaming

   asyncio.run(main())

Using Reasoning Models
----------------------

Qwen's QwQ model can show its reasoning process:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def main():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwq-32b",  # Qwen's reasoning model
               temperature=0.1,
               max_tokens=2000,
           )
           
           response = await client.generate(
               "Solve this step by step: If a train travels 120 km in 2 hours, what is its average speed?",
               config
           )
           
           print("Response:", response.content)
           if response.thinking:
               print("\nThinking process:")
               print(response.thinking)

   asyncio.run(main())

Multi-turn Conversations
------------------------

Build conversations with context:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig, Message

   async def main():
       async with UnifiedLLMClient() as client:
           messages = [
               Message(role="system", content="You are a helpful assistant."),
               Message(role="user", content="What is Python?"),
               Message(role="assistant", content="Python is a high-level programming language..."),
               Message(role="user", content="Can you give me a simple example?"),
           ]
           
           config = RequestConfig(
               model="claude-3-sonnet",
               temperature=0.7,
           )
           
           response = await client.generate(messages, config)
           print(response.content)

   asyncio.run(main())

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

   async def main():
       async with UnifiedLLMClient() as client:
           # List all available providers
           providers = await client.list_providers()
           for provider in providers:
               print(f"Provider: {provider.name}")
               print(f"  Status: {provider.status}")
               print(f"  Models: {len(provider.models)}")
               print()

   asyncio.run(main())

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
2. **Handle exceptions**: Wrap calls in try-catch blocks for production use.
3. **Monitor usage**: Track token usage and costs.
4. **Configure timeouts**: Set appropriate timeouts for your use case.
5. **Use streaming**: For long responses, use streaming to improve user experience.

Next Steps
----------

- Read the :doc:`configuration` guide to set up providers
- Explore :doc:`examples` for more advanced usage patterns
- Check out the :doc:`cli` for command-line usage
- Review the API reference for detailed documentation

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