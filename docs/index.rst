.. MonoLLM documentation master file, created by
   sphinx-quickstart on Sun Jun  1 00:02:09 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MonoLLM Documentation
=====================

MonoLLM is a unified Python framework for accessing multiple Large Language Model providers through a single, consistent interface. It simplifies LLM integration by abstracting away provider-specific differences while maintaining full access to advanced features.

.. note::
   MonoLLM v0.1.2 introduces comprehensive testing utilities, improved reasoning model support, and enhanced provider compatibility.

Key Features
------------

**Unified Interface**
   Access OpenAI, Anthropic, Google, Qwen, DeepSeek, and other providers through one API

**Advanced Capabilities**
   - Streaming responses for real-time interaction
   - Reasoning models with thinking steps (QwQ, o1, DeepSeek R1)
   - Multi-turn conversations with context management
   - Automatic model capability detection

**Developer Experience**
   - Type-safe async/await API
   - Comprehensive error handling
   - Flexible configuration management
   - Built-in retry mechanisms and rate limiting

**Production Ready**
   - Proxy support for enterprise environments
   - Token usage tracking and cost management
   - Extensive logging and monitoring
   - Comprehensive test suite

Quick Start
-----------

Installation
~~~~~~~~~~~~

Install MonoLLM using pip:

.. code-block:: bash

   pip install monollm

Or from source:

.. code-block:: bash

   git clone https://github.com/cyborgoat/MonoLLM.git
   cd MonoLLM
   pip install -e .

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def main():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="gpt-4o", temperature=0.7)
           response = await client.generate("Explain quantum computing", config)
           print(response.content)

   asyncio.run(main())

Configuration
~~~~~~~~~~~~~

Set up your API keys:

.. code-block:: bash

   export OPENAI_API_KEY="your-openai-key"
   export ANTHROPIC_API_KEY="your-anthropic-key"
   export DASHSCOPE_API_KEY="your-qwen-key"
   export DEEPSEEK_API_KEY="your-deepseek-key"

Supported Providers
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 30 25 25

   * - Provider
     - Models
     - Special Features
     - Status
   * - OpenAI
     - GPT-4o, GPT-4o-mini, o1, o1-mini
     - Reasoning models, MCP
     - ✓ Full support
   * - Anthropic
     - Claude 3.5 Sonnet, Claude 3.5 Haiku
     - MCP integration
     - ✓ Full support
   * - Qwen/DashScope
     - QwQ-32B, Qwen3 series
     - Thinking steps, Chinese
     - ✓ Full support
   * - DeepSeek
     - DeepSeek V3, DeepSeek R1
     - Code reasoning
     - ✓ Full support
   * - Google
     - Gemini 2.0 Flash, Gemini 2.5 Pro
     - Multimodal (planned)
     - ✓ Basic support
   * - Volcengine
     - Doubao models
     - Enterprise features
     - ✓ Basic support

Documentation Sections
-----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   quickstart
   configuration
   examples
   testing

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/client
   api/models
   api/exceptions

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Getting Help
------------

- **GitHub Issues**: Report bugs and request features at https://github.com/cyborgoat/MonoLLM/issues
- **Documentation**: Full documentation at https://cyborgoat.github.io/MonoLLM/
- **Examples**: See the ``examples/`` directory for complete usage examples

License
-------

MonoLLM is released under the MIT License. See the LICENSE file for details.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

