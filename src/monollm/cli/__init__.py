"""
MonoLLM CLI Module

This module provides both user-friendly and machine-friendly command-line interfaces
for the MonoLLM framework. It supports interactive usage as well as programmatic
integration with external applications like Tauri sidecars.

Components:
    - user_interface: Human-friendly CLI with rich formatting
    - machine_interface: JSON-based API for programmatic usage
    - config_manager: Configuration and model management utilities
    - output_formatter: Structured output formatting for different modes

Documentation:
    - README.md: Complete CLI documentation with examples
    - README-MACHINE.md: Comprehensive machine interface documentation
    - MACHINE-QUICK-REFERENCE.md: Quick reference for JSON API usage

Usage:
    # User interface (default)
    monollm list-providers
    monollm chat gpt-4o --temperature 0.7
    
    # Machine interface (JSON output)
    monollm list-providers --machine
    monollm generate "Hello" --model gpt-4o --machine
"""

from .main import main
from .user_interface import UserInterface
from .machine_interface import MachineInterface
from .config_manager import ConfigManager
from .output_formatter import OutputFormatter

__all__ = [
    "main",
    "UserInterface", 
    "MachineInterface",
    "ConfigManager",
    "OutputFormatter"
] 