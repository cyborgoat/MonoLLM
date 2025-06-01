Quick Start Guide
=================

This guide will help you get started with MonoLLM quickly and efficiently.

Installation
------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.12 or higher
- API keys for the providers you want to use

Install MonoLLM
~~~~~~~~~~~~~~~

Using pip:

.. code-block:: bash

   pip install monollm

From source:

.. code-block:: bash

   git clone https://github.com/cyborgoat/MonoLLM.git
   cd MonoLLM
   pip install -e .

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set up your API keys as environment variables:

.. code-block:: bash

   # OpenAI
   export OPENAI_API_KEY="your-openai-api-key"
   
   # Anthropic
   export ANTHROPIC_API_KEY="your-anthropic-api-key"
   
   # Qwen/DashScope
   export DASHSCOPE_API_KEY="your-dashscope-api-key"
   
   # DeepSeek
   export DEEPSEEK_API_KEY="your-deepseek-api-key"
   
   # Google (optional)
   export GOOGLE_API_KEY="your-google-api-key"

Using .env File
~~~~~~~~~~~~~~~

Create a ``.env`` file in your project root:

.. code-block:: bash

   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   DASHSCOPE_API_KEY=your-dashscope-api-key
   DEEPSEEK_API_KEY=your-deepseek-api-key

Basic Usage
-----------

Simple Text Generation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def basic_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="gpt-4o-mini",
               temperature=0.7,
               max_tokens=100
           )
           
           response = await client.generate(
               "Explain machine learning in one paragraph",
               config
           )
           
           print(response.content)
           print(f"Tokens used: {response.usage.total_tokens}")

   asyncio.run(basic_example())

Streaming Responses
~~~~~~~~~~~~~~~~~~~

For real-time response streaming:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def streaming_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="claude-3-5-sonnet-20241022",
               temperature=0.7,
               stream=True
           )
           
           print("Streaming response:")
           async for chunk in await client.generate_stream(
               "Write a short story about a robot",
               config
           ):
               if chunk.content:
                   print(chunk.content, end="", flush=True)
               
               if chunk.is_complete:
                   print("\n\nStreaming complete!")
                   break

   asyncio.run(streaming_example())

Multi-turn Conversations
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig, Message

   async def conversation_example():
       async with UnifiedLLMClient() as client:
           messages = [
               Message(role="system", content="You are a helpful programming assistant."),
               Message(role="user", content="How do I create a list in Python?"),
               Message(role="assistant", content="You can create a list using square brackets: my_list = [1, 2, 3]"),
               Message(role="user", content="How do I add items to it?")
           ]
           
           config = RequestConfig(model="gpt-4o")
           response = await client.generate(messages, config)
           
           print("Assistant:", response.content)

   asyncio.run(conversation_example())

Reasoning Models
~~~~~~~~~~~~~~~~

Use models with thinking capabilities:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def reasoning_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwq-32b",  # Qwen's reasoning model
               temperature=0.7,
               show_thinking=True,
               stream=True  # Required for QwQ models
           )
           
           prompt = "Solve this step by step: If a train travels 60 miles in 45 minutes, what is its speed in mph?"
           
           thinking_content = ""
           final_answer = ""
           
           async for chunk in await client.generate_stream(prompt, config):
               if chunk.thinking:
                   thinking_content += chunk.thinking
               if chunk.content:
                   final_answer += chunk.content
               if chunk.is_complete:
                   break
           
           print("Thinking process:")
           print(thinking_content[:200] + "..." if len(thinking_content) > 200 else thinking_content)
           print("\nFinal answer:")
           print(final_answer)

   asyncio.run(reasoning_example())

Command Line Interface
----------------------

MonoLLM includes a powerful CLI for quick interactions:

List Available Providers
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   monollm list-providers

List Available Models
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   monollm list-models
   monollm list-models --provider qwen

Generate Text
~~~~~~~~~~~~~

.. code-block:: bash

   # Basic generation
   monollm generate "What is artificial intelligence?" --model gpt-4o-mini
   
   # With streaming
   monollm generate "Write a poem about coding" --model claude-3-5-sonnet-20241022 --stream
   
   # Reasoning model with thinking
   monollm generate "Solve: 2x + 5 = 13" --model qwq-32b --thinking

Interactive Chat
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Start interactive chat
   monollm chat gpt-4o --stream
   
   # Chat with reasoning model
   monollm chat qwq-32b --thinking

Error Handling
--------------

Always handle potential errors in production code:

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig
   from monollm.core.exceptions import (
       ProviderError, 
       RateLimitError, 
       QuotaExceededError,
       ModelNotFoundError
   )

   async def robust_example():
       async with UnifiedLLMClient() as client:
           try:
               config = RequestConfig(model="gpt-4o")
               response = await client.generate("Hello, world!", config)
               print(response.content)
               
           except ModelNotFoundError as e:
               print(f"Model not found: {e.message}")
           except RateLimitError as e:
               print(f"Rate limit exceeded: {e.message}")
           except QuotaExceededError as e:
               print(f"Quota exceeded: {e.message}")
           except ProviderError as e:
               print(f"Provider error: {e.message}")
           except Exception as e:
               print(f"Unexpected error: {e}")

   asyncio.run(robust_example())

Testing Your Setup
------------------

Use the built-in test utilities to verify your configuration:

.. code-block:: bash

   # Quick test with a working model
   python test/run_tests.py --quick
   
   # Test specific provider
   python test/run_tests.py --provider qwen
   
   # Test reasoning capabilities
   python test/run_tests.py --thinking

Next Steps
----------

- Read the :doc:`configuration` guide for advanced setup options
- Explore :doc:`examples` for more complex use cases
- Check the :doc:`api/client` reference for detailed API documentation
- Visit the :doc:`testing` guide to validate your setup

Common Issues
-------------

**API Key Not Found**
   Make sure your environment variables are set correctly or your ``.env`` file is in the right location.

**Model Not Available**
   Check if the model is configured in ``config/models.json`` and your API key has access to it.

**Rate Limiting**
   MonoLLM includes built-in retry mechanisms, but you may need to implement additional backoff strategies for high-volume usage.

**Streaming Issues**
   Some models require streaming mode (like QwQ models). The client will automatically enable streaming when needed. 