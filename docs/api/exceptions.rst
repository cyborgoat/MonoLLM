Exceptions
==========

MonoLLM defines a hierarchy of exceptions to help you handle different types of errors that may occur when working with LLM providers.

Exception Hierarchy
-------------------

All MonoLLM exceptions inherit from the base :class:`MonoLLMError` class:

.. code-block:: text

   MonoLLMError
   ├── ConfigurationError
   ├── ProviderError
   │   ├── AuthenticationError
   │   ├── RateLimitError
   │   ├── QuotaExceededError
   │   └── ModelNotFoundError
   ├── ConnectionError
   └── ValidationError

Base Exception
--------------

MonoLLMError
~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.MonoLLMError
   :members:
   :undoc-members:
   :show-inheritance:

Configuration Exceptions
------------------------

ConfigurationError
~~~~~~~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.ConfigurationError
   :members:
   :undoc-members:
   :show-inheritance:

Provider Exceptions
-------------------

ProviderError
~~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.ProviderError
   :members:
   :undoc-members:
   :show-inheritance:

AuthenticationError
~~~~~~~~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.AuthenticationError
   :members:
   :undoc-members:
   :show-inheritance:

RateLimitError
~~~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.RateLimitError
   :members:
   :undoc-members:
   :show-inheritance:

QuotaExceededError
~~~~~~~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.QuotaExceededError
   :members:
   :undoc-members:
   :show-inheritance:

ModelNotFoundError
~~~~~~~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.ModelNotFoundError
   :members:
   :undoc-members:
   :show-inheritance:

Network Exceptions
------------------

ConnectionError
~~~~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.ConnectionError
   :members:
   :undoc-members:
   :show-inheritance:

Validation Exceptions
---------------------

ValidationError
~~~~~~~~~~~~~~~

.. autoclass:: monollm.core.exceptions.ValidationError
   :members:
   :undoc-members:
   :show-inheritance:

Usage Examples
--------------

Basic Error Handling
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from monollm import UnifiedLLMClient, RequestConfig
   from monollm.core.exceptions import MonoLLMError, ProviderError

   async def basic_error_handling():
       async with UnifiedLLMClient() as client:
           try:
               config = RequestConfig(model="qwen-plus")
               response = await client.generate("Hello", config)
               print(response.content)
           except MonoLLMError as e:
               print(f"MonoLLM error: {e}")
           except Exception as e:
               print(f"Unexpected error: {e}")

Specific Error Handling
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from monollm.core.exceptions import (
       ConfigurationError,
       AuthenticationError,
       RateLimitError,
       ModelNotFoundError,
       ConnectionError
   )

   async def specific_error_handling():
       async with UnifiedLLMClient() as client:
           try:
               config = RequestConfig(model="invalid-model")
               response = await client.generate("Hello", config)
           except ConfigurationError as e:
               print(f"Configuration issue: {e}")
               print("Please check your API keys and configuration.")
           except AuthenticationError as e:
               print(f"Authentication failed: {e}")
               print("Please verify your API key is correct.")
           except RateLimitError as e:
               print(f"Rate limit exceeded: {e}")
               print("Please wait before making more requests.")
           except ModelNotFoundError as e:
               print(f"Model not found: {e}")
               print("Please check the model name and availability.")
           except ConnectionError as e:
               print(f"Connection failed: {e}")
               print("Please check your internet connection.")

Retry Logic with Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm.core.exceptions import RateLimitError, ConnectionError

   async def retry_on_error():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwen-plus")
           max_retries = 3
           
           for attempt in range(max_retries):
               try:
                   response = await client.generate("Hello", config)
                   return response.content
               except (RateLimitError, ConnectionError) as e:
                   if attempt < max_retries - 1:
                       wait_time = 2 ** attempt  # Exponential backoff
                       print(f"Attempt {attempt + 1} failed: {e}")
                       print(f"Retrying in {wait_time} seconds...")
                       await asyncio.sleep(wait_time)
                   else:
                       print(f"All {max_retries} attempts failed")
                       raise

Error Context Information
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   async def error_context_example():
       async with UnifiedLLMClient() as client:
           try:
               config = RequestConfig(model="qwen-plus")
               response = await client.generate("Hello", config)
           except ProviderError as e:
               # Provider errors often include additional context
               print(f"Provider: {e.provider}")
               print(f"Error code: {e.error_code}")
               print(f"Message: {e.message}")
               if hasattr(e, 'retry_after'):
                   print(f"Retry after: {e.retry_after} seconds")

Best Practices
--------------

1. **Catch specific exceptions** rather than using broad exception handlers
2. **Log error details** for debugging and monitoring
3. **Implement retry logic** for transient errors like rate limits
4. **Provide user-friendly error messages** in your application
5. **Monitor error rates** to identify issues with providers or configuration
6. **Use exponential backoff** when retrying failed requests 