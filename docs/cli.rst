Command Line Interface
======================

MonoLLM provides a powerful command-line interface (CLI) for interacting with multiple LLM providers without writing code.

Installation
------------

The CLI is automatically available after installing MonoLLM:

.. code-block:: bash

   # Verify installation
   monollm --help

Basic Usage
-----------

The CLI follows this general pattern:

.. code-block:: bash

   monollm <command> [arguments] [options]

Available Commands
------------------

list-providers
~~~~~~~~~~~~~~

List all available LLM providers:

.. code-block:: bash

   monollm list-providers

Example output:

.. code-block:: text

   Available Providers:
   ┌─────────────┬──────────────────────┬───────────┬──────────────┐
   │ Provider ID │ Name                 │ Streaming │ Reasoning    │
   ├─────────────┼──────────────────────┼───────────┼──────────────┤
   │ qwen        │ Qwen (DashScope)     │ ✅        │ ✅           │
   │ anthropic   │ Anthropic Claude     │ ✅        │ ❌           │
   │ openai      │ OpenAI               │ ✅        │ ✅           │
   │ deepseek    │ DeepSeek             │ ✅        │ ✅           │
   └─────────────┴──────────────────────┴───────────┴──────────────┘

list-models
~~~~~~~~~~~

List available models:

.. code-block:: bash

   # List all models
   monollm list-models

   # List models for specific provider
   monollm list-models --provider qwen

Example output:

.. code-block:: text

   Qwen Models:
   ┌─────────────┬─────────────┬───────────┬──────────────┬─────────────┐
   │ Model ID    │ Name        │ Max Tokens│ Reasoning    │ Streaming   │
   ├─────────────┼─────────────┼───────────┼──────────────┼─────────────┤
   │ qwq-32b     │ QwQ 32B     │ 8192      │ ✅           │ ✅          │
   │ qwen-plus   │ Qwen Plus   │ 4096      │ ❌           │ ✅          │
   └─────────────┴─────────────┴───────────┴──────────────┴─────────────┘

generate
~~~~~~~~

Generate text using a specified model:

.. code-block:: bash

   monollm generate "Your prompt here" --model MODEL_NAME [options]

**Required Arguments:**

- ``prompt``: The text prompt to send to the model
- ``--model``: The model to use for generation

**Optional Arguments:**

- ``--temperature FLOAT``: Creativity level (0.0-2.0, default: 0.7)
- ``--max-tokens INT``: Maximum output tokens (default: 1000)
- ``--stream``: Enable streaming output
- ``--thinking``: Show reasoning process (for reasoning models)
- ``--system TEXT``: System message to set context

Examples
--------

Basic Text Generation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Simple generation
   monollm generate "What is artificial intelligence?" --model qwen-plus

   # With custom parameters
   monollm generate "Write a creative story" --model qwen-plus --temperature 0.9 --max-tokens 500

Streaming Output
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Stream the response in real-time
   monollm generate "Tell me a long story about space exploration" --model qwen-plus --stream

Reasoning Models
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Use reasoning model with thinking steps
   monollm generate "Solve: If a train travels 60 miles in 45 minutes, what is its speed in mph?" --model qwq-32b --thinking

   # Complex reasoning problem
   monollm generate "A farmer has 17 sheep. All but 9 die. How many are left?" --model qwq-32b --thinking

System Messages
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Set context with system message
   monollm generate "What is 15 × 23?" --model qwen-plus --system "You are a helpful math tutor. Show your work step by step."

   # Creative writing with context
   monollm generate "Write a poem about coding" --model qwen-plus --system "You are a poet who loves technology"

Provider-Specific Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Qwen (DashScope):**

.. code-block:: bash

   # Regular model
   monollm generate "Explain quantum computing" --model qwen-plus

   # Reasoning model
   monollm generate "Solve this logic puzzle step by step" --model qwq-32b --thinking

**Anthropic Claude:**

.. code-block:: bash

   # Claude 3.5 Sonnet
   monollm generate "Write a technical blog post about APIs" --model claude-3-5-sonnet-20241022

**OpenAI:**

.. code-block:: bash

   # GPT-4o
   monollm generate "Explain machine learning concepts" --model gpt-4o

   # O1 reasoning model
   monollm generate "Solve this complex math problem" --model o1-preview --thinking

**DeepSeek:**

.. code-block:: bash

   # DeepSeek V3
   monollm generate "Code review this Python function" --model deepseek-chat

   # DeepSeek R1 (reasoning)
   monollm generate "Analyze this algorithm's complexity" --model deepseek-reasoner --thinking

Advanced Usage
--------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set default values using environment variables:

.. code-block:: bash

   # Set default model
   export MONOLLM_DEFAULT_MODEL=qwen-plus

   # Set default temperature
   export MONOLLM_DEFAULT_TEMPERATURE=0.7

   # Set default max tokens
   export MONOLLM_DEFAULT_MAX_TOKENS=1000

Configuration Files
~~~~~~~~~~~~~~~~~~~

Create a configuration file at ``~/.monollm/config.json``:

.. code-block:: json

   {
     "default_model": "qwen-plus",
     "default_temperature": 0.7,
     "default_max_tokens": 1000,
     "preferred_providers": ["qwen", "anthropic", "openai"]
   }

Batch Processing
~~~~~~~~~~~~~~~~

Process multiple prompts from a file:

.. code-block:: bash

   # Create a file with prompts (one per line)
   echo "What is AI?" > prompts.txt
   echo "Explain quantum computing" >> prompts.txt
   echo "Benefits of renewable energy" >> prompts.txt

   # Process each prompt
   while IFS= read -r prompt; do
       echo "Prompt: $prompt"
       monollm generate "$prompt" --model qwen-plus
       echo "---"
   done < prompts.txt

Output Formatting
~~~~~~~~~~~~~~~~~

Control output format:

.. code-block:: bash

   # JSON output
   monollm generate "Hello world" --model qwen-plus --format json

   # Markdown output
   monollm generate "Write a README" --model qwen-plus --format markdown

   # Plain text (default)
   monollm generate "Simple response" --model qwen-plus --format text

Error Handling
--------------

The CLI provides helpful error messages:

**Missing API Key:**

.. code-block:: text

   Error: No API key found for provider 'qwen'
   Please set the DASHSCOPE_API_KEY environment variable.

**Invalid Model:**

.. code-block:: text

   Error: Model 'invalid-model' not found
   Available models: qwen-plus, qwq-32b, claude-3-5-sonnet-20241022

**Network Issues:**

.. code-block:: text

   Error: Failed to connect to provider
   Please check your internet connection and proxy settings.

Debugging
~~~~~~~~~

Enable verbose output for debugging:

.. code-block:: bash

   # Verbose mode
   monollm generate "Hello" --model qwen-plus --verbose

   # Debug mode
   monollm generate "Hello" --model qwen-plus --debug

Performance Tips
----------------

1. **Use streaming** for long responses to see output immediately
2. **Set appropriate token limits** to control response length and cost
3. **Choose the right model** for your task (reasoning vs. general)
4. **Use lower temperatures** for factual content, higher for creative content
5. **Cache responses** when possible to avoid repeated API calls

Integration with Other Tools
----------------------------

Pipe Output
~~~~~~~~~~~

.. code-block:: bash

   # Save to file
   monollm generate "Write a Python script" --model qwq-32b > script.py

   # Pipe to other commands
   monollm generate "List of programming languages" --model qwen-plus | grep -i python

Shell Scripts
~~~~~~~~~~~~~

.. code-block:: bash

   #!/bin/bash
   # ai-helper.sh

   MODEL="qwen-plus"
   PROMPT="$1"

   if [ -z "$PROMPT" ]; then
       echo "Usage: $0 'your prompt here'"
       exit 1
   fi

   monollm generate "$PROMPT" --model "$MODEL" --stream

   # Usage: ./ai-helper.sh "Explain Docker containers"

Aliases
~~~~~~~

Create convenient aliases:

.. code-block:: bash

   # Add to ~/.bashrc or ~/.zshrc
   alias ai='monollm generate'
   alias ai-reason='monollm generate --model qwq-32b --thinking'
   alias ai-stream='monollm generate --stream'
   alias ai-creative='monollm generate --temperature 0.9'

   # Usage:
   # ai "What is machine learning?" --model qwen-plus
   # ai-reason "Solve this math problem"
   # ai-stream "Tell me a story" --model qwen-plus

Configuration Reference
-----------------------

Command Line Options
~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

   Global Options:
     --help, -h          Show help message
     --version, -v       Show version information
     --config PATH       Custom configuration file path
     --verbose           Enable verbose output
     --debug             Enable debug output

   Generate Command Options:
     --model, -m TEXT    Model to use (required)
     --temperature FLOAT Temperature (0.0-2.0)
     --max-tokens INT    Maximum output tokens
     --stream            Enable streaming
     --thinking          Show reasoning (reasoning models only)
     --system TEXT       System message
     --format TEXT       Output format (text|json|markdown)

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # API Keys
   OPENAI_API_KEY          # OpenAI API key
   ANTHROPIC_API_KEY       # Anthropic API key
   GOOGLE_API_KEY          # Google Gemini API key
   DASHSCOPE_API_KEY       # Qwen/DashScope API key
   DEEPSEEK_API_KEY        # DeepSeek API key
   VOLCENGINE_API_KEY      # Volcengine API key

   # Proxy Settings
   PROXY_ENABLED           # Enable proxy (true/false)
   PROXY_TYPE              # Proxy type (http/socks5)
   PROXY_HOST              # Proxy host
   PROXY_PORT              # Proxy port
   PROXY_USERNAME          # Proxy username (optional)
   PROXY_PASSWORD          # Proxy password (optional)

   # CLI Defaults
   MONOLLM_DEFAULT_MODEL       # Default model
   MONOLLM_DEFAULT_TEMPERATURE # Default temperature
   MONOLLM_DEFAULT_MAX_TOKENS  # Default max tokens

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Command not found:**

.. code-block:: bash

   # Ensure MonoLLM is installed
   pip install -e .

   # Check if it's in PATH
   which monollm

**Permission denied:**

.. code-block:: bash

   # On Unix systems, ensure execute permissions
   chmod +x $(which monollm)

**Slow responses:**

.. code-block:: bash

   # Use streaming for immediate feedback
   monollm generate "long prompt" --model qwen-plus --stream

   # Reduce max tokens for faster responses
   monollm generate "prompt" --model qwen-plus --max-tokens 100

Getting Help
~~~~~~~~~~~~

.. code-block:: bash

   # General help
   monollm --help

   # Command-specific help
   monollm generate --help
   monollm list-models --help

   # Version information
   monollm --version

The CLI provides a convenient way to access MonoLLM's capabilities without writing code, making it perfect for quick tasks, scripting, and experimentation. 