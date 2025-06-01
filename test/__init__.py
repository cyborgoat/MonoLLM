"""
MonoLLM Test Suite

This package contains comprehensive testing utilities for the MonoLLM framework.

Test Scripts:
    - test_all_models.py: Comprehensive test suite for all configured models
    - test_single_model.py: Individual model testing with custom configurations
    - test_providers.py: Provider-specific testing utilities
    - test_thinking.py: Specialized tests for reasoning models with thinking capabilities

Usage:
    # Run all model tests
    python test/test_all_models.py
    
    # Test a specific model
    python test/test_single_model.py qwq-32b --reasoning --stream
    
    # Test thinking capabilities
    python test/test_thinking.py
    
    # Test specific providers
    python test/test_providers.py --provider qwen

Author: cyborgoat
License: MIT License
"""

__version__ = "1.0.0"
__author__ = "cyborgoat"

# Test utilities and common functions can be imported here
# from .utils import TestRunner, ModelValidator, etc. 