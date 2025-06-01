Testing Guide
=============

MonoLLM includes a comprehensive test suite to validate functionality across all supported providers and models. This guide covers how to use the testing utilities to verify your setup and ensure everything works correctly.

Overview
--------

The test suite is located in the ``test/`` directory and includes:

- **Model Testing**: Validate all configured models
- **Provider Testing**: Test provider-specific functionality
- **Reasoning Testing**: Specialized tests for thinking-capable models
- **Integration Testing**: End-to-end functionality validation

Test Scripts
------------

Quick Test Runner
~~~~~~~~~~~~~~~~~

The unified test runner provides a convenient entry point for all testing:

.. code-block:: bash

   # Quick test with a known working model
   python test/run_tests.py --quick
   
   # Run comprehensive test suite
   python test/run_tests.py --all
   
   # Test specific provider
   python test/run_tests.py --provider qwen
   
   # Test specific model
   python test/run_tests.py --model qwq-32b --reasoning

Individual Test Scripts
~~~~~~~~~~~~~~~~~~~~~~~

**test_all_models.py** - Comprehensive model testing:

.. code-block:: bash

   # Test all configured models
   python test/test_all_models.py

**test_single_model.py** - Individual model testing:

.. code-block:: bash

   # Basic test
   python test/test_single_model.py gpt-4o-mini
   
   # Test with streaming
   python test/test_single_model.py claude-3-5-sonnet-20241022 --stream
   
   # Test reasoning model
   python test/test_single_model.py qwq-32b --reasoning --stream

**test_thinking.py** - Reasoning model testing:

.. code-block:: bash

   # Test all thinking models
   python test/test_thinking.py
   
   # Test specific model
   python test/test_thinking.py --model qwq-32b
   
   # Test specific reasoning scenario
   python test/test_thinking.py --test logic_puzzle

**test_providers.py** - Provider-specific testing:

.. code-block:: bash

   # Test all providers
   python test/test_providers.py
   
   # Test specific provider
   python test/test_providers.py --provider anthropic
   
   # Test specific functionality
   python test/test_providers.py --provider qwen --test thinking

Setting Up Tests
----------------

Prerequisites
~~~~~~~~~~~~~

1. **API Keys**: Configure API keys for the providers you want to test
2. **Environment**: Set up your ``.env`` file or environment variables
3. **Dependencies**: Ensure all dependencies are installed

Environment Setup
~~~~~~~~~~~~~~~~~

Create a ``.env`` file in your project root:

.. code-block:: bash

   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   DASHSCOPE_API_KEY=your-dashscope-api-key
   DEEPSEEK_API_KEY=your-deepseek-api-key

Running Your First Test
~~~~~~~~~~~~~~~~~~~~~~~

Start with a quick test to verify your setup:

.. code-block:: bash

   python test/run_tests.py --quick

This will test a known working model (QwQ-32B) with reasoning capabilities.

Test Categories
---------------

Basic Functionality Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~

These tests verify core functionality:

- **Text Generation**: Basic prompt-response functionality
- **Configuration**: Model parameter handling
- **Error Handling**: Graceful failure scenarios
- **Token Usage**: Usage tracking and reporting

**Example Output:**

.. code-block:: text

   Testing Model: gpt-4o-mini
   ✓ Basic generation: Success (1.2s, 45 tokens)
   ✓ Configuration: Temperature and max_tokens applied
   ✓ Usage tracking: 45 total tokens

Streaming Tests
~~~~~~~~~~~~~~~

Validate real-time streaming capabilities:

- **Stream Chunks**: Proper chunk delivery
- **Completion Detection**: Stream termination handling
- **Content Assembly**: Correct content reconstruction

**Example Output:**

.. code-block:: text

   Testing Streaming: claude-3-5-sonnet-20241022
   ✓ Stream initialization: Success
   ✓ Chunk delivery: 23 chunks received
   ✓ Stream completion: Properly terminated
   ✓ Content assembly: 156 characters total

Reasoning Tests
~~~~~~~~~~~~~~~

Specialized tests for thinking-capable models:

- **Thinking Steps**: Reasoning process validation
- **Quality Analysis**: Thinking content evaluation
- **Step Coverage**: Expected reasoning step detection

**Test Scenarios:**

- **basic_math**: Simple arithmetic with step-by-step solving
- **logic_puzzle**: Constraint satisfaction problems
- **multi_step_problem**: Complex multi-step calculations
- **complex_reasoning**: Advanced problem-solving strategies
- **code_reasoning**: Code debugging and analysis

**Example Output:**

.. code-block:: text

   Testing QwQ-32B Reasoning:
   ✓ basic_math: Quality score 0.95 (4/4 steps covered)
   ✓ logic_puzzle: Quality score 0.88 (3/3 steps covered)
   ✓ Thinking length: 1,247 characters
   ✓ Final answer: Correct and complete

Provider-Specific Tests
~~~~~~~~~~~~~~~~~~~~~~~

Test provider-unique features and edge cases:

**OpenAI Provider:**
- Temperature control
- Special character handling
- Long prompt processing

**Anthropic Provider:**
- System message support
- Multi-turn conversations
- MCP integration

**Qwen Provider:**
- Chinese language support
- Code generation
- Thinking mode capabilities

**DeepSeek Provider:**
- Code analysis
- Algorithm design
- Reasoning capabilities

Understanding Test Results
--------------------------

Success Indicators
~~~~~~~~~~~~~~~~~~

- **✓ PASS**: Test completed successfully
- **Quality Score**: 0.8+ indicates high-quality reasoning
- **Response Time**: Typical response latencies
- **Token Usage**: Accurate usage tracking

Partial Success
~~~~~~~~~~~~~~~

- **⚠ PARTIAL (2/3)**: Some tests failed
- **⏭ SKIP**: Test not applicable (e.g., thinking test on non-reasoning model)
- **Stream Only**: Model requires streaming mode

Failure Indicators
~~~~~~~~~~~~~~~~~~

- **✗ FAIL**: Test failed with error
- **Provider Error**: API-related issues
- **Timeout**: Request exceeded time limit
- **Configuration Error**: Setup issues

Common Test Scenarios
---------------------

Validating New Setup
~~~~~~~~~~~~~~~~~~~~

When setting up MonoLLM for the first time:

.. code-block:: bash

   # 1. Quick validation
   python test/run_tests.py --quick
   
   # 2. Test your primary provider
   python test/run_tests.py --provider openai
   
   # 3. Validate reasoning models if needed
   python test/run_tests.py --thinking

Testing After Configuration Changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After modifying ``config/models.json`` or adding new API keys:

.. code-block:: bash

   # Test specific model
   python test/test_single_model.py new-model-id
   
   # Test provider functionality
   python test/test_providers.py --provider new-provider

Continuous Integration
~~~~~~~~~~~~~~~~~~~~~~

For CI/CD pipelines:

.. code-block:: bash

   # Run all tests with timeout
   timeout 300 python test/run_tests.py --all
   
   # Test critical models only
   python test/test_single_model.py gpt-4o-mini
   python test/test_single_model.py qwq-32b --reasoning

Troubleshooting Tests
---------------------

Common Issues
~~~~~~~~~~~~~

**API Key Missing**

.. code-block:: text

   Warning: No API key found for provider 'openai'

*Solution*: Add the API key to your ``.env`` file or environment variables.

**Model Not Found**

.. code-block:: text

   Model 'gpt-5' not found in any provider

*Solution*: Check ``config/models.json`` for available models.

**Rate Limiting**

.. code-block:: text

   Error code: 429 - Rate limit exceeded

*Solution*: Wait and retry, or implement additional backoff strategies.

**Quota Exceeded**

.. code-block:: text

   Error code: 429 - You exceeded your current quota

*Solution*: Check your API billing or use a different provider.

Debug Mode
~~~~~~~~~~

For detailed error information, check the console output during test runs. The test scripts provide comprehensive error messages and suggestions.

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

The test suite includes timing information to help monitor:

- **Response Latency**: Time to first response
- **Streaming Performance**: Chunk delivery rate
- **Thinking Generation**: Reasoning process speed

Custom Testing
--------------

Creating Custom Tests
~~~~~~~~~~~~~~~~~~~~~

You can extend the test scripts for your specific needs:

.. code-block:: python

   # Add to test_thinking.py
   CUSTOM_PROMPTS = {
       "domain_specific": {
           "prompt": "Your domain-specific test prompt",
           "expected_steps": ["step1", "step2", "step3"],
           "difficulty": "medium"
       }
   }

Batch Testing
~~~~~~~~~~~~~

Test multiple models sequentially:

.. code-block:: bash

   # Test multiple models
   for model in qwq-32b claude-3-5-sonnet-20241022 deepseek-chat; do
       echo "Testing $model..."
       python test/test_single_model.py $model --stream
   done

Integration with Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integrate testing into your development workflow:

.. code-block:: bash

   # Pre-commit testing
   python test/run_tests.py --quick
   
   # Feature testing
   python test/test_single_model.py your-model --custom-prompt "Your test"
   
   # Performance testing
   python test/test_providers.py --provider your-provider

Best Practices
--------------

1. **Start Small**: Begin with quick tests before running comprehensive suites
2. **Test Incrementally**: Test new configurations immediately
3. **Monitor Usage**: Be aware of API costs during extensive testing
4. **Document Results**: Keep track of which models work best for your use cases
5. **Regular Validation**: Run tests periodically to catch configuration drift

The testing suite provides a robust foundation for validating your MonoLLM setup and ensuring reliable operation across all supported providers and models. 