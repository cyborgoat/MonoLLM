Data Models
===========

MonoLLM provides several data models for representing requests, responses, and configuration.

Core Models
-----------

LLMResponse
~~~~~~~~~~~

.. autoclass:: monollm.core.models.LLMResponse
   :members:
   :undoc-members:
   :show-inheritance:

StreamingResponse
~~~~~~~~~~~~~~~~~

.. autoclass:: monollm.core.models.StreamingResponse
   :members:
   :undoc-members:
   :show-inheritance:

StreamChunk
~~~~~~~~~~~

.. autoclass:: monollm.core.models.StreamChunk
   :members:
   :undoc-members:
   :show-inheritance:

Configuration Models
--------------------

RequestConfig
~~~~~~~~~~~~~

.. autoclass:: monollm.core.models.RequestConfig
   :members:
   :undoc-members:
   :show-inheritance:

Message
~~~~~~~

.. autoclass:: monollm.core.models.Message
   :members:
   :undoc-members:
   :show-inheritance:

Usage
~~~~~

.. autoclass:: monollm.core.models.Usage
   :members:
   :undoc-members:
   :show-inheritance:

Provider Models
---------------

ProviderInfo
~~~~~~~~~~~~

.. autoclass:: monollm.core.models.ProviderInfo
   :members:
   :undoc-members:
   :show-inheritance:

ModelInfo
~~~~~~~~~

.. autoclass:: monollm.core.models.ModelInfo
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Creating a Request Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from monollm import RequestConfig

   # Basic configuration
   config = RequestConfig(
       model="qwen-plus",
       temperature=0.7,
       max_tokens=1000
   )

   # Advanced configuration
   config = RequestConfig(
       model="qwq-32b",
       temperature=0.1,
       max_tokens=2000,
       stream=True,
       show_thinking=True,
       metadata={"user_id": "123", "session_id": "abc"}
   )

Creating Messages
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from monollm import Message

   # System message
   system_msg = Message(
       role="system",
       content="You are a helpful assistant."
   )

   # User message
   user_msg = Message(
       role="user",
       content="What is Python?"
   )

   # Assistant message
   assistant_msg = Message(
       role="assistant",
       content="Python is a programming language..."
   )

Working with Responses
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from monollm import UnifiedLLMClient, RequestConfig

   async def example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwen-plus")
           response = await client.generate("Hello", config)
           
           # Access response data
           print(f"Content: {response.content}")
           print(f"Model: {response.model}")
           print(f"Provider: {response.provider}")
           
           if response.usage:
               print(f"Input tokens: {response.usage.prompt_tokens}")
               print(f"Output tokens: {response.usage.completion_tokens}")
               print(f"Total tokens: {response.usage.total_tokens}")
           
           if response.thinking:
               print(f"Thinking: {response.thinking}")

Streaming Responses
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   async def streaming_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwen-plus", stream=True)
           
           streaming_response = await client.generate_stream("Tell me a story", config)
           
           async for chunk in streaming_response:
               if chunk.content:
                   print(chunk.content, end="", flush=True)
               
               # Access chunk metadata
               if chunk.usage:
                   print(f"Tokens so far: {chunk.usage.total_tokens}") 