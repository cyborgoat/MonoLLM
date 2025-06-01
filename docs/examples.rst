Examples
========

This page provides comprehensive examples of using MonoLLM for various tasks and scenarios.

Basic Examples
--------------

Simple Text Generation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def simple_generation():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwen-plus")
           
           response = await client.generate(
               "What are the benefits of renewable energy?",
               config
           )
           
           print(response.content)

   asyncio.run(simple_generation())

Streaming Response
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def streaming_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwen-plus",
               stream=True
           )
           
           print("Response: ", end="", flush=True)
           
           streaming_response = await client.generate_stream(
               "Write a short poem about artificial intelligence.",
               config
           )
           
           async for chunk in streaming_response:
               if chunk.content:
                   print(chunk.content, end="", flush=True)
           
           print()  # New line

   asyncio.run(streaming_example())

Advanced Examples
-----------------

Reasoning with QwQ
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def reasoning_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwq-32b",
               show_thinking=True,
               max_tokens=1500
           )
           
           response = await client.generate(
               """
               A farmer has 17 sheep. All but 9 die. How many sheep are left?
               Think through this step by step.
               """,
               config
           )
           
           if response.thinking:
               print("🤔 Thinking process:")
               print(response.thinking)
               print("\n" + "="*50 + "\n")
           
           print("📝 Final answer:")
           print(response.content)

   asyncio.run(reasoning_example())

Multi-turn Conversation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig, Message

   async def conversation_example():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwen-plus")
           
           # Initialize conversation
           messages = [
               Message(role="system", content="You are a helpful coding assistant."),
               Message(role="user", content="How do I create a list in Python?"),
           ]
           
           # First exchange
           response = await client.generate(messages, config)
           print("Assistant:", response.content)
           
           # Continue conversation
           messages.append(Message(role="assistant", content=response.content))
           messages.append(Message(
               role="user", 
               content="Can you show me how to add items to that list?"
           ))
           
           # Second exchange
           response = await client.generate(messages, config)
           print("Assistant:", response.content)
           
           # Third exchange
           messages.append(Message(role="assistant", content=response.content))
           messages.append(Message(
               role="user", 
               content="What about removing items?"
           ))
           
           response = await client.generate(messages, config)
           print("Assistant:", response.content)

   asyncio.run(conversation_example())

Provider Comparison
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def compare_providers():
       async with UnifiedLLMClient() as client:
           prompt = "Explain machine learning in one paragraph."
           
           # Test different models
           models = [
               ("qwen-plus", "Qwen Plus"),
               ("qwq-32b", "QwQ 32B"),
               ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet"),
               ("gpt-4o", "GPT-4o"),
           ]
           
           for model_id, model_name in models:
               try:
                   config = RequestConfig(model=model_id, max_tokens=200)
                   response = await client.generate(prompt, config)
                   
                   print(f"\n{model_name}:")
                   print("-" * len(model_name))
                   print(response.content)
                   
                   if response.usage:
                       print(f"Tokens: {response.usage.total_tokens}")
                       
               except Exception as e:
                   print(f"\n{model_name}: Error - {e}")

   asyncio.run(compare_providers())

Use Case Examples
-----------------

Content Generation
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def content_generation():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwen-plus",
               temperature=0.8,  # Higher creativity
               max_tokens=1000
           )
           
           # Blog post generation
           blog_prompt = """
           Write a blog post about the future of electric vehicles.
           Include:
           - Current market trends
           - Technological advances
           - Environmental impact
           - Challenges and opportunities
           
           Make it engaging and informative for a general audience.
           """
           
           response = await client.generate(blog_prompt, config)
           print("Blog Post:")
           print("=" * 50)
           print(response.content)

   asyncio.run(content_generation())

Code Generation and Review
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def code_assistance():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwq-32b",  # Good for reasoning about code
               temperature=0.2   # Lower temperature for code
           )
           
           # Code generation
           code_prompt = """
           Create a Python function that:
           1. Takes a list of numbers
           2. Removes duplicates
           3. Sorts the list in descending order
           4. Returns the top 3 numbers
           
           Include error handling and docstring.
           """
           
           response = await client.generate(code_prompt, config)
           print("Generated Code:")
           print("-" * 30)
           print(response.content)
           
           # Code review
           review_prompt = """
           Review this Python code and suggest improvements:
           
           def process_data(data):
               result = []
               for item in data:
                   if item not in result:
                       result.append(item)
               result.sort(reverse=True)
               return result[:3]
           """
           
           response = await client.generate(review_prompt, config)
           print("\nCode Review:")
           print("-" * 30)
           print(response.content)

   asyncio.run(code_assistance())

Data Analysis
~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def data_analysis():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwq-32b",
               show_thinking=True,
               max_tokens=1500
           )
           
           analysis_prompt = """
           Analyze this sales data and provide insights:
           
           Q1 2024: $125,000 (15% increase from Q1 2023)
           Q2 2024: $140,000 (8% increase from Q1 2024)
           Q3 2024: $135,000 (3.6% decrease from Q2 2024)
           Q4 2024: $160,000 (18.5% increase from Q3 2024)
           
           Provide:
           1. Trend analysis
           2. Seasonal patterns
           3. Growth rate calculations
           4. Recommendations for Q1 2025
           """
           
           response = await client.generate(analysis_prompt, config)
           
           if response.thinking:
               print("Analysis Process:")
               print(response.thinking)
               print("\n" + "="*50 + "\n")
           
           print("Analysis Results:")
           print(response.content)

   asyncio.run(data_analysis())

Creative Writing
~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def creative_writing():
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwen-plus",
               temperature=1.0,  # Maximum creativity
               max_tokens=2000
           )
           
           story_prompt = """
           Write a short science fiction story (500-800 words) about:
           - A world where AI and humans collaborate seamlessly
           - A discovery that changes everything
           - An unexpected friendship
           
           Make it engaging with vivid descriptions and dialogue.
           """
           
           response = await client.generate(story_prompt, config)
           print("Science Fiction Story:")
           print("=" * 50)
           print(response.content)
           
           if response.usage:
               print(f"\nWord count estimate: ~{response.usage.completion_tokens * 0.75:.0f} words")

   asyncio.run(creative_writing())

Error Handling Examples
-----------------------

Robust Error Handling
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig
   from monollm.core.exceptions import (
       MonoLLMError, 
       ProviderError, 
       ConnectionError,
       ConfigurationError
   )

   async def robust_generation(prompt: str, model: str):
       """Generate text with comprehensive error handling."""
       async with UnifiedLLMClient() as client:
           try:
               config = RequestConfig(
                   model=model,
                   max_tokens=500,
                   temperature=0.7
               )
               
               response = await client.generate(prompt, config)
               return response.content
               
           except ConfigurationError as e:
               print(f"Configuration error: {e}")
               print("Please check your API keys and configuration.")
               return None
               
           except ConnectionError as e:
               print(f"Connection error: {e}")
               print("Please check your internet connection and proxy settings.")
               return None
               
           except ProviderError as e:
               print(f"Provider error: {e}")
               print("The AI provider encountered an error.")
               return None
               
           except MonoLLMError as e:
               print(f"MonoLLM error: {e}")
               return None
               
           except Exception as e:
               print(f"Unexpected error: {e}")
               return None

   async def main():
       # Test with valid model
       result = await robust_generation("Hello, world!", "qwen-plus")
       if result:
           print("Success:", result)
       
       # Test with invalid model
       result = await robust_generation("Hello, world!", "invalid-model")
       if not result:
           print("Handled invalid model gracefully")

   asyncio.run(main())

Retry Logic
~~~~~~~~~~~

.. code-block:: python

   import asyncio
   import time
   from monollm import UnifiedLLMClient, RequestConfig
   from monollm.core.exceptions import ProviderError

   async def generate_with_retry(prompt: str, model: str, max_retries: int = 3):
       """Generate text with retry logic."""
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model=model)
           
           for attempt in range(max_retries):
               try:
                   response = await client.generate(prompt, config)
                   return response.content
                   
               except ProviderError as e:
                   if attempt < max_retries - 1:
                       wait_time = 2 ** attempt  # Exponential backoff
                       print(f"Attempt {attempt + 1} failed: {e}")
                       print(f"Retrying in {wait_time} seconds...")
                       await asyncio.sleep(wait_time)
                   else:
                       print(f"All {max_retries} attempts failed")
                       raise
               
               except Exception as e:
                   # Don't retry for non-provider errors
                   print(f"Non-retryable error: {e}")
                   raise

   async def main():
       try:
           result = await generate_with_retry(
               "What is the capital of France?", 
               "qwen-plus"
           )
           print("Result:", result)
       except Exception as e:
           print("Final error:", e)

   asyncio.run(main())

Performance Examples
--------------------

Concurrent Requests
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def concurrent_generation():
       """Generate multiple responses concurrently."""
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwen-plus", max_tokens=100)
           
           # Define multiple prompts
           prompts = [
               "What is artificial intelligence?",
               "Explain quantum computing.",
               "What are the benefits of renewable energy?",
               "How does machine learning work?",
               "What is blockchain technology?"
           ]
           
           # Create tasks for concurrent execution
           tasks = [
               client.generate(prompt, config) 
               for prompt in prompts
           ]
           
           # Execute all tasks concurrently
           start_time = time.time()
           responses = await asyncio.gather(*tasks)
           end_time = time.time()
           
           # Display results
           for i, (prompt, response) in enumerate(zip(prompts, responses)):
               print(f"\nQuestion {i+1}: {prompt}")
               print(f"Answer: {response.content[:100]}...")
           
           print(f"\nTotal time: {end_time - start_time:.2f} seconds")
           print(f"Average time per request: {(end_time - start_time) / len(prompts):.2f} seconds")

   import time
   asyncio.run(concurrent_generation())

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   async def batch_processing():
       """Process a batch of texts efficiently."""
       async with UnifiedLLMClient() as client:
           config = RequestConfig(
               model="qwen-plus",
               temperature=0.3,
               max_tokens=50
           )
           
           # Sample data to process
           texts = [
               "The weather is beautiful today.",
               "I love programming in Python.",
               "Machine learning is fascinating.",
               "The sunset was absolutely stunning.",
               "Coffee helps me stay productive."
           ]
           
           # Process in batches to avoid overwhelming the API
           batch_size = 3
           results = []
           
           for i in range(0, len(texts), batch_size):
               batch = texts[i:i + batch_size]
               
               # Create tasks for this batch
               tasks = [
                   client.generate(
                       f"Analyze the sentiment of this text: '{text}'",
                       config
                   )
                   for text in batch
               ]
               
               # Process batch
               batch_responses = await asyncio.gather(*tasks)
               results.extend(batch_responses)
               
               # Small delay between batches
               if i + batch_size < len(texts):
                   await asyncio.sleep(0.5)
           
           # Display results
           for text, response in zip(texts, results):
               print(f"Text: {text}")
               print(f"Analysis: {response.content}")
               print("-" * 50)

   asyncio.run(batch_processing())

Integration Examples
--------------------

Web Application Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Example with FastAPI
   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   import asyncio
   from monollm import UnifiedLLMClient, RequestConfig

   app = FastAPI()
   
   # Global client instance
   llm_client = None

   class GenerationRequest(BaseModel):
       prompt: str
       model: str = "qwen-plus"
       temperature: float = 0.7
       max_tokens: int = 500

   class GenerationResponse(BaseModel):
       content: str
       model: str
       provider: str
       tokens_used: int

   @app.on_event("startup")
   async def startup_event():
       global llm_client
       llm_client = UnifiedLLMClient()
       await llm_client.initialize()

   @app.on_event("shutdown")
   async def shutdown_event():
       global llm_client
       if llm_client:
           await llm_client.close()

   @app.post("/generate", response_model=GenerationResponse)
   async def generate_text(request: GenerationRequest):
       try:
           config = RequestConfig(
               model=request.model,
               temperature=request.temperature,
               max_tokens=request.max_tokens
           )
           
           response = await llm_client.generate(request.prompt, config)
           
           return GenerationResponse(
               content=response.content,
               model=response.model,
               provider=response.provider,
               tokens_used=response.usage.total_tokens if response.usage else 0
           )
           
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

   @app.get("/models")
   async def list_models():
       models = llm_client.list_models()
       return models

   # Run with: uvicorn main:app --reload

CLI Application
~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """
   Simple CLI application using MonoLLM
   """
   import asyncio
   import argparse
   from monollm import UnifiedLLMClient, RequestConfig

   async def interactive_chat():
       """Interactive chat session."""
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model="qwen-plus")
           
           print("MonoLLM Interactive Chat")
           print("Type 'quit' to exit")
           print("-" * 30)
           
           while True:
               try:
                   user_input = input("\nYou: ").strip()
                   
                   if user_input.lower() in ['quit', 'exit', 'q']:
                       break
                   
                   if not user_input:
                       continue
                   
                   print("AI: ", end="", flush=True)
                   
                   # Use streaming for better UX
                   config.stream = True
                   streaming_response = await client.generate_stream(user_input, config)
                   
                   async for chunk in streaming_response:
                       if chunk.content:
                           print(chunk.content, end="", flush=True)
                   
                   print()  # New line
                   
               except KeyboardInterrupt:
                   print("\nGoodbye!")
                   break
               except Exception as e:
                   print(f"Error: {e}")

   async def single_generation(prompt: str, model: str):
       """Single text generation."""
       async with UnifiedLLMClient() as client:
           config = RequestConfig(model=model)
           response = await client.generate(prompt, config)
           print(response.content)

   def main():
       parser = argparse.ArgumentParser(description="MonoLLM CLI")
       parser.add_argument("--interactive", "-i", action="store_true", 
                          help="Start interactive chat")
       parser.add_argument("--prompt", "-p", type=str, 
                          help="Single prompt to process")
       parser.add_argument("--model", "-m", type=str, default="qwen-plus",
                          help="Model to use")
       
       args = parser.parse_args()
       
       if args.interactive:
           asyncio.run(interactive_chat())
       elif args.prompt:
           asyncio.run(single_generation(args.prompt, args.model))
       else:
           parser.print_help()

   if __name__ == "__main__":
       main()

Best Practices
--------------

1. **Always use async context managers** for proper resource management
2. **Handle errors gracefully** with appropriate exception handling
3. **Use appropriate models** for different tasks (reasoning vs. general)
4. **Set reasonable token limits** to control costs
5. **Implement retry logic** for production applications
6. **Use streaming** for better user experience with long responses
7. **Cache responses** when appropriate to reduce API calls
8. **Monitor usage** and implement rate limiting if needed

These examples demonstrate the flexibility and power of MonoLLM across various use cases. Adapt them to your specific needs and requirements. 