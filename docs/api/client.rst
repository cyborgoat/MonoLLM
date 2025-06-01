Client API
==========

The :class:`~monollm.core.client.UnifiedLLMClient` is the main entry point for interacting with multiple LLM providers through a unified interface.

UnifiedLLMClient
----------------

.. autoclass:: monollm.core.client.UnifiedLLMClient
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def main():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwq-32b")
           response = await client.generate("Hello, world!", config)
           print(response.content)

   asyncio.run(main())

Initialization Options
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from pathlib import Path
   from rich.console import Console

   # Custom configuration directory
   client = UnifiedLLMClient(config_dir=Path("./my_config"))

   # Custom console for logging
   console = Console()
   client = UnifiedLLMClient(console=console)

Provider Management
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   async with UnifiedLLMClient() as client:
       # List all available providers
       providers = client.list_providers()
       for provider_id, info in providers.items():
           print(f"{provider_id}: {info.name}")

       # List models for a specific provider
       models = client.list_models(provider_id="qwen")
       for model_id, info in models["qwen"].items():
           print(f"{model_id}: {info.name}")

       # Get information about a specific model
       provider_id, model_info = client.get_model_info("qwq-32b")
       print(f"Model: {model_info.name}")
       print(f"Provider: {provider_id}")
       print(f"Max tokens: {model_info.max_tokens}")

Text Generation
~~~~~~~~~~~~~~~

.. code-block:: python

   async with UnifiedLLMClient() as client:
       # Simple text generation
       config = RequestConfig(
           model="qwen-plus",
           temperature=0.7,
           max_tokens=1000
       )
       
       response = await client.generate(
           "Explain quantum computing",
           config
       )
       
       print(f"Response: {response.content}")
       print(f"Tokens used: {response.usage.total_tokens}")

Streaming Generation
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   async with UnifiedLLMClient() as client:
       config = RequestConfig(
           model="qwen-plus",
           stream=True
       )
       
       streaming_response = await client.generate_stream(
           "Tell me a story",
           config
       )
       
       async for chunk in streaming_response:
           if chunk.content:
               print(chunk.content, end="", flush=True)

Multi-turn Conversations
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from monollm import Message

   async with UnifiedLLMClient() as client:
       config = RequestConfig(model="qwen-plus")
       
       messages = [
           Message(role="system", content="You are a helpful assistant."),
           Message(role="user", content="What's the weather like?"),
       ]
       
       response = await client.generate(messages, config)
       
       # Continue the conversation
       messages.append(Message(role="assistant", content=response.content))
       messages.append(Message(role="user", content="What about tomorrow?"))
       
       response = await client.generate(messages, config)

Error Handling
~~~~~~~~~~~~~~

.. code-block:: python

   from monollm.core.exceptions import MonoLLMError, ProviderError

   async with UnifiedLLMClient() as client:
       try:
           config = RequestConfig(model="invalid-model")
           response = await client.generate("Hello", config)
       except MonoLLMError as e:
           print(f"MonoLLM error: {e}")
       except ProviderError as e:
           print(f"Provider error: {e}")

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # The client automatically loads configuration from:
   # 1. Environment variables
   # 2. Configuration files in config/ directory
   # 3. Default settings

   # You can specify a custom config directory
   from pathlib import Path
   
   client = UnifiedLLMClient(config_dir=Path("./custom_config"))

Context Manager Usage
~~~~~~~~~~~~~~~~~~~~~

The client should always be used as an async context manager to ensure proper resource cleanup:

.. code-block:: python

   # Recommended: Using async context manager
   async with UnifiedLLMClient() as client:
       # Your code here
       pass

   # Manual management (not recommended)
   client = UnifiedLLMClient()
   await client.initialize()
   try:
       # Your code here
       pass
   finally:
       await client.close()

Thread Safety
~~~~~~~~~~~~~~

The :class:`UnifiedLLMClient` is designed for use with asyncio and is not thread-safe. Each thread should have its own client instance:

.. code-block:: python

   import asyncio
   import threading

   async def worker():
       async with UnifiedLLMClient() as client:
           # Each thread gets its own client
           config = RequestConfig(model="qwen-plus")
           response = await client.generate("Hello", config)
           print(response.content)

   def run_in_thread():
       asyncio.run(worker())

   # Start multiple threads
   threads = []
   for i in range(3):
       thread = threading.Thread(target=run_in_thread)
       threads.append(thread)
       thread.start()

   for thread in threads:
       thread.join()

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Connection Pooling**: The client maintains connection pools for each provider
- **Async Operations**: All operations are async for better concurrency
- **Resource Management**: Use context managers for automatic cleanup
- **Caching**: Provider configurations are cached for better performance

.. note::
   The client automatically initializes providers on first use. This means the first request to a provider may take slightly longer as the provider is set up.

.. warning::
   Always use the client as an async context manager or manually call :meth:`~UnifiedLLMClient.close` to ensure proper cleanup of resources. 