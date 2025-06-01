.. UnifiedLLM documentation master file, created by
   sphinx-quickstart on Sun Jun  1 00:02:09 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MonoLLM Documentation
========================

.. image:: https://img.shields.io/badge/version-0.1.1-blue.svg
   :target: https://github.com/cyborgoat/MonoLLM
   :alt: Version

.. image:: https://img.shields.io/badge/python-3.12+-blue.svg
   :target: https://python.org
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/cyborgoat/MonoLLM/blob/main/LICENSE
   :alt: License

A powerful framework that provides a unified interface for multiple LLM providers, allowing developers to seamlessly switch between different AI models while maintaining consistent API interactions.

🚀 **Key Features**
-------------------

* **🔄 Unified Interface**: Access multiple LLM providers through a single, consistent API
* **🌐 Proxy Support**: Configure HTTP/SOCKS5 proxies for all LLM calls
* **📺 Streaming**: Real-time streaming responses for better user experience
* **🧠 Reasoning Models**: Special support for reasoning models with thinking steps
* **🌡️ Temperature Control**: Fine-tune creativity and randomness when supported
* **🔢 Token Management**: Control costs with maximum output token limits
* **🔧 MCP Integration**: Model Context Protocol support when available
* **🎯 OpenAI Protocol**: Prefer OpenAI-compatible APIs for consistency
* **⚙️ JSON Configuration**: Easy configuration management through JSON files

📋 **Supported Providers**
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 15 10 15

   * - Provider
     - Status
     - Streaming
     - Reasoning
     - MCP
     - OpenAI Protocol
   * - OpenAI
     - ✅ Ready
     - ✅ Yes
     - ✅ Yes
     - ✅ Yes
     - ✅ Yes
   * - Anthropic
     - ✅ Ready
     - ✅ Yes
     - ❌ No
     - ✅ Yes
     - ❌ No
   * - Google Gemini
     - 🚧 Planned
     - ✅ Yes
     - ❌ No
     - ❌ No
     - ❌ No
   * - Qwen (DashScope)
     - ✅ Ready
     - ✅ Yes
     - ✅ Yes
     - ❌ No
     - ✅ Yes
   * - DeepSeek
     - ✅ Ready
     - ✅ Yes
     - ✅ Yes
     - ❌ No
     - ✅ Yes
   * - Volcengine
     - 🚧 Planned
     - ✅ Yes
     - ❌ No
     - ❌ No
     - ✅ Yes

⚡ **Quick Start**
-----------------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/cyborgoat/MonoLLM.git
   cd MonoLLM

   # Install with uv (recommended)
   uv sync
   uv pip install -e .

   # Or install with pip
   pip install -e .

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from unified_llm import UnifiedLLMClient, RequestConfig

   async def main():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwq-32b",  # Qwen's reasoning model
               temperature=0.7,
               max_tokens=1000,
           )
           
           response = await client.generate(
               "Explain quantum computing in simple terms.",
               config
           )
           
           print(response.content)
           if response.usage:
               print(f"Tokens used: {response.usage.total_tokens}")

   asyncio.run(main())

CLI Usage
~~~~~~~~~

.. code-block:: bash

   # List available providers
   monollm list-providers

   # List available models
   monollm list-models --provider qwen

   # Generate text
   monollm generate "What is AI?" --model qwq-32b --stream

   # Use reasoning model with thinking steps
   monollm generate "Solve: 2x + 5 = 13" --model qwq-32b --thinking

📚 **Documentation Contents**
-----------------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   configuration
   cli
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/client

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources

🔗 **Useful Links**
-------------------

* **GitHub Repository**: https://github.com/cyborgoat/MonoLLM
* **Issue Tracker**: https://github.com/cyborgoat/MonoLLM/issues
* **Discussions**: https://github.com/cyborgoat/MonoLLM/discussions
* **PyPI Package**: https://pypi.org/project/unified-llm/ *(coming soon)*

📄 **License**
--------------

This project is licensed under the MIT License. See the `LICENSE <https://github.com/cyborgoat/MonoLLM/blob/main/LICENSE>`_ file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

