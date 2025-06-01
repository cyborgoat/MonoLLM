Configuration
=============

MonoLLM provides flexible configuration options through environment variables, configuration files, and runtime parameters.

Environment Variables
---------------------

API Keys
~~~~~~~~

Set API keys for the providers you want to use:

.. code-block:: bash

   # Required: At least one provider API key
   export OPENAI_API_KEY="sk-proj-..."
   export ANTHROPIC_API_KEY="sk-ant-api03-..."
   export GOOGLE_API_KEY="AIzaSy..."
   export DASHSCOPE_API_KEY="sk-..."
   export DEEPSEEK_API_KEY="sk-..."
   export VOLCENGINE_API_KEY="..."

Base URLs (Optional)
~~~~~~~~~~~~~~~~~~~~

Override default API endpoints:

.. code-block:: bash

   export OPENAI_BASE_URL="https://your-custom-openai-endpoint.com/v1"
   export ANTHROPIC_BASE_URL="https://your-custom-anthropic-endpoint.com"
   export GOOGLE_BASE_URL="https://your-custom-google-endpoint.com"

Proxy Configuration
~~~~~~~~~~~~~~~~~~~

Configure HTTP/SOCKS5 proxies:

.. code-block:: bash

   # HTTP Proxy
   export PROXY_ENABLED=true
   export PROXY_TYPE=http
   export PROXY_HOST=127.0.0.1
   export PROXY_PORT=7890
   export PROXY_USERNAME=user  # Optional
   export PROXY_PASSWORD=pass  # Optional

   # SOCKS5 Proxy
   export SOCKS5_ENABLED=true
   export SOCKS5_HOST=127.0.0.1
   export SOCKS5_PORT=1080
   export SOCKS5_USERNAME=user  # Optional
   export SOCKS5_PASSWORD=pass  # Optional

Configuration Files
-------------------

MonoLLM uses JSON configuration files stored in the ``config/`` directory.

Directory Structure
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   config/
   ├── models.json      # Model definitions and capabilities
   ├── providers.json   # Provider configurations
   └── proxy.json       # Proxy and network settings

models.json
~~~~~~~~~~~

Defines available models and their capabilities:

.. code-block:: json

   {
     "providers": {
       "qwen": {
         "name": "Qwen (DashScope)",
         "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
         "uses_openai_protocol": true,
         "supports_streaming": true,
         "supports_mcp": false,
         "models": {
           "qwq-32b": {
             "name": "QwQ 32B",
             "max_tokens": 8192,
             "supports_temperature": true,
             "supports_streaming": true,
             "supports_thinking": true
           },
           "qwen-plus": {
             "name": "Qwen Plus",
             "max_tokens": 4096,
             "supports_temperature": true,
             "supports_streaming": true,
             "supports_thinking": false
           },
           "o1": {
             "name": "OpenAI o1",
             "max_tokens": 100000,
             "supports_temperature": false,
             "supports_streaming": false,
             "supports_thinking": true
           },
           "gpt-4o": {
             "name": "GPT-4o",
             "max_tokens": 128000,
             "supports_temperature": true,
             "supports_streaming": true,
             "supports_thinking": false
           }
         }
       }
     }
   }

providers.json
~~~~~~~~~~~~~~

Provider-specific configurations:

.. code-block:: json

   {
     "qwen": {
       "timeout": 30,
       "max_retries": 3,
       "retry_delay": 1.0
     },
     "anthropic": {
       "timeout": 60,
       "max_retries": 2,
       "retry_delay": 2.0
     }
   }

proxy.json
~~~~~~~~~~

Network and proxy settings:

.. code-block:: json

   {
     "proxy": {
       "enabled": true,
       "type": "http",
       "host": "127.0.0.1",
       "port": 7890,
       "username": null,
       "password": null
     },
     "socks5": {
       "enabled": false,
       "host": "127.0.0.1",
       "port": 1080,
       "username": null,
       "password": null
     },
     "timeout": 30,
     "max_connections": 100,
     "max_keepalive_connections": 20
   }

Runtime Configuration
---------------------

RequestConfig
~~~~~~~~~~~~~

Configure individual requests:

.. code-block:: python

   from monollm import RequestConfig

   config = RequestConfig(
       model="qwq-32b",
       provider="qwen",  # Optional: auto-detected from model
       temperature=0.7,  # 0.0 to 2.0
       max_tokens=1000,  # Maximum output tokens
       stream=False,     # Enable streaming
       show_thinking=False,  # Show reasoning for reasoning models
       metadata={"user_id": "123"}  # Custom metadata
   )

Client Configuration
~~~~~~~~~~~~~~~~~~~~

Configure the client instance:

.. code-block:: python

   from pathlib import Path
   from rich.console import Console
   from monollm import UnifiedLLMClient

   # Custom configuration directory
   client = UnifiedLLMClient(
       config_dir="./my_config"
   )

   # Custom console for rich output
   console = Console()
   client = UnifiedLLMClient(console=console)

Advanced Configuration
----------------------

Custom Provider Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add or modify provider configurations programmatically:

.. code-block:: python

   from monollm.core.models import ProviderConfig, ModelInfo

   # Create custom provider config
   provider_config = ProviderConfig(
       name="Custom Provider",
       api_key="your-api-key",
       base_url="https://api.custom.com/v1",
       timeout=45,
       proxy_url="http://proxy:8080"
   )

   # Define model capabilities
   model_info = ModelInfo(
       name="Custom Model",
       max_tokens=4096,
       supports_temperature=True,
       supports_streaming=True,
       supports_thinking=False
   )

Environment File (.env)
~~~~~~~~~~~~~~~~~~~~~~~

Create a ``.env`` file for local development:

.. code-block:: bash

   # .env file
   DASHSCOPE_API_KEY=sk-your-dashscope-key
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
   OPENAI_API_KEY=sk-proj-your-openai-key

   # Proxy settings
   PROXY_ENABLED=true
   PROXY_TYPE=http
   PROXY_HOST=127.0.0.1
   PROXY_PORT=7890

   # Custom base URLs
   OPENAI_BASE_URL=https://api.openai.com/v1

Load the environment file in your application:

.. code-block:: python

   from dotenv import load_dotenv
   load_dotenv()  # Load .env file

   from monollm import UnifiedLLMClient

Configuration Validation
-------------------------

MonoLLM validates configurations at startup and provides helpful error messages:

.. code-block:: python

   from monollm import UnifiedLLMClient
   from monollm.core.exceptions import ConfigurationError

   try:
       async with UnifiedLLMClient() as client:
           # Configuration will be validated here
           pass
   except ConfigurationError as e:
       print(f"Configuration error: {e}")

Common Configuration Patterns
------------------------------

Development Setup
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # .env for development
   DASHSCOPE_API_KEY=sk-dev-key
   PROXY_ENABLED=false
   DEBUG=true

Production Setup
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Environment variables for production
   export DASHSCOPE_API_KEY="$PRODUCTION_DASHSCOPE_KEY"
   export ANTHROPIC_API_KEY="$PRODUCTION_ANTHROPIC_KEY"
   export PROXY_ENABLED=true
   export PROXY_HOST=production-proxy.company.com
   export PROXY_PORT=8080

Multi-Environment Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import os
   from monollm import UnifiedLLMClient

   # Different environments
   environment = os.getenv("ENVIRONMENT", "development")

   if environment == "production":
       client = UnifiedLLMClient(config_dir="./config/production")
   elif environment == "staging":
       client = UnifiedLLMClient(config_dir="./config/staging")
   else:
       client = UnifiedLLMClient(config_dir="./config/development")

Configuration Priority
----------------------

MonoLLM loads configuration in the following order (later sources override earlier ones):

1. **Default values** - Built-in defaults
2. **Configuration files** - JSON files in config directory
3. **Environment variables** - OS environment variables
4. **Runtime parameters** - Parameters passed to client/config objects

Example:

.. code-block:: python

   # 1. Default timeout: 15 seconds
   # 2. config/providers.json: "timeout": 30
   # 3. Environment: QWEN_TIMEOUT=45
   # 4. Runtime: RequestConfig(timeout=60)
   # Final timeout: 60 seconds

Troubleshooting Configuration
-----------------------------

Common Issues
~~~~~~~~~~~~~

**Missing API Keys:**

.. code-block:: text

   ConfigurationError: No API key found for provider 'qwen'

Solution: Set the ``DASHSCOPE_API_KEY`` environment variable.

**Invalid Configuration File:**

.. code-block:: text

   ConfigurationError: Invalid JSON in config/models.json

Solution: Validate your JSON syntax using a JSON validator.

**Proxy Connection Failed:**

.. code-block:: text

   ConnectionError: Failed to connect through proxy

Solution: Verify proxy settings and network connectivity.

Debugging Configuration
~~~~~~~~~~~~~~~~~~~~~~~

Enable debug logging to see configuration loading:

.. code-block:: python

   import logging
   logging.basicConfig(level=logging.DEBUG)

   from monollm import UnifiedLLMClient

   # Debug logs will show configuration loading process
   client = UnifiedLLMClient()

Configuration Validation
~~~~~~~~~~~~~~~~~~~~~~~~~

Validate your configuration before using:

.. code-block:: python

   from monollm import UnifiedLLMClient

   async def validate_config():
       try:
           async with UnifiedLLMClient() as client:
               providers = client.list_providers()
               print(f"Available providers: {list(providers.keys())}")
               
               models = client.list_models()
               for provider_id, provider_models in models.items():
                   print(f"{provider_id}: {len(provider_models)} models")
                   
       except Exception as e:
           print(f"Configuration error: {e}")

   import asyncio
   asyncio.run(validate_config())

Best Practices
--------------

1. **Use environment variables** for sensitive data like API keys
2. **Version control configuration files** but not API keys
3. **Use different configs** for different environments
4. **Validate configuration** at application startup
5. **Document custom configurations** for your team
6. **Use .env files** for local development
7. **Set reasonable timeouts** based on your use case
8. **Monitor configuration changes** in production

Security Considerations
-----------------------

- **Never commit API keys** to version control
- **Use secure key management** in production
- **Rotate API keys** regularly
- **Limit API key permissions** when possible
- **Use HTTPS proxies** for secure communication
- **Validate configuration inputs** to prevent injection attacks 