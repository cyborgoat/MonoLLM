Installation
============

This guide will help you install UnifiedLLM and set up your development environment.

Prerequisites
-------------

Before installing UnifiedLLM, ensure you have the following:

* **Python 3.13+**: UnifiedLLM requires Python 3.13 or later
* **Git**: For cloning the repository
* **uv** (recommended) or **pip**: For package management

Installing Python 3.13
~~~~~~~~~~~~~~~~~~~~~~~

If you don't have Python 3.13 installed:

**macOS (using Homebrew):**

.. code-block:: bash

   brew install python@3.13

**Ubuntu/Debian:**

.. code-block:: bash

   sudo apt update
   sudo apt install python3.13 python3.13-pip python3.13-venv

**Windows:**

Download Python 3.13 from the `official Python website <https://python.org/downloads/>`_.

Installing uv (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

uv is a fast Python package installer and resolver:

.. code-block:: bash

   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Or with pip
   pip install uv

Installation Methods
--------------------

Method 1: Using uv (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/cyborgoat/unified-llm.git
   cd unified-llm

   # Create virtual environment and install dependencies
   uv sync

   # Install in development mode
   uv pip install -e .

Method 2: Using pip
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/cyborgoat/unified-llm.git
   cd unified-llm

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -e .

Method 3: Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For contributors and developers:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/cyborgoat/unified-llm.git
   cd unified-llm

   # Install with development dependencies
   uv sync --dev

   # Install pre-commit hooks
   pre-commit install

Verification
------------

Verify your installation by running:

.. code-block:: bash

   # Check CLI is working
   unified-llm --help

   # List available providers
   unified-llm list-providers

   # Test Python import
   python -c "from unified_llm import UnifiedLLMClient; print('Installation successful!')"

Setting Up API Keys
-------------------

UnifiedLLM requires API keys for the providers you want to use. Set them as environment variables:

.. code-block:: bash

   # OpenAI
   export OPENAI_API_KEY="your-openai-api-key"

   # Anthropic
   export ANTHROPIC_API_KEY="your-anthropic-api-key"

   # Google Gemini
   export GOOGLE_API_KEY="your-google-api-key"

   # Qwen (DashScope)
   export DASHSCOPE_API_KEY="your-dashscope-api-key"

   # DeepSeek
   export DEEPSEEK_API_KEY="your-deepseek-api-key"

   # Volcengine
   export VOLCENGINE_API_KEY="your-volcengine-api-key"

.. tip::
   Create a ``.env`` file in your project directory to store API keys:

   .. code-block:: bash

      # .env file
      OPENAI_API_KEY=your-openai-api-key
      ANTHROPIC_API_KEY=your-anthropic-api-key
      DASHSCOPE_API_KEY=your-dashscope-api-key
      # ... other keys

Docker Installation
-------------------

You can also run UnifiedLLM using Docker:

.. code-block:: bash

   # Build the Docker image
   docker build -t unified-llm .

   # Run with environment variables
   docker run -e OPENAI_API_KEY=your-key unified-llm

Troubleshooting
---------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Python Version Error:**

.. code-block:: text

   ERROR: Python 3.13 or higher is required

Solution: Upgrade to Python 3.13+ or use pyenv to manage multiple Python versions.

**Permission Denied:**

.. code-block:: text

   PermissionError: [Errno 13] Permission denied

Solution: Use ``--user`` flag with pip or create a virtual environment.

**Module Not Found:**

.. code-block:: text

   ModuleNotFoundError: No module named 'unified_llm'

Solution: Ensure you've installed the package and activated your virtual environment.

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the `troubleshooting guide <troubleshooting.html>`_
2. Search existing `GitHub issues <https://github.com/cyborgoat/unified-llm/issues>`_
3. Create a new issue with detailed error information
4. Join our `discussions <https://github.com/cyborgoat/unified-llm/discussions>`_

Next Steps
----------

After installation, check out:

* :doc:`quickstart` - Get started with basic usage
* :doc:`configuration` - Configure providers and settings
* :doc:`examples` - See practical examples
* :doc:`cli` - Learn about the command-line interface 