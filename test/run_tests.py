#!/usr/bin/env python3
"""
MonoLLM Test Runner

A convenient script to run different test suites with various options.
"""

import asyncio
import sys
import os
import argparse
import subprocess
from datetime import datetime

def print_header(text: str, char: str = "🚀"):
    """Print a formatted header."""
    print(f"\n{char * 60}")
    print(f" {text}")
    print(f"{char * 60}")

def run_script(script_name: str, args: list = None) -> int:
    """Run a test script with given arguments."""
    cmd = [sys.executable, f"test/{script_name}"]
    if args:
        cmd.extend(args)
    
    print(f"Running: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        # Set PYTHONPATH to include src directory
        env = os.environ.copy()
        src_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
        if 'PYTHONPATH' in env:
            env['PYTHONPATH'] = f"{src_path}:{env['PYTHONPATH']}"
        else:
            env['PYTHONPATH'] = src_path
        
        result = subprocess.run(cmd, cwd=os.path.dirname(os.path.dirname(__file__)), env=env)
        return result.returncode
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return 1

def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(
        description="MonoLLM Test Runner - Run various test suites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tests
  python test/run_tests.py --all
  
  # Quick test with a single model
  python test/run_tests.py --quick
  
  # Test thinking capabilities
  python test/run_tests.py --thinking
  
  # Test specific provider
  python test/run_tests.py --provider qwen
  
  # Test specific model
  python test/run_tests.py --model qwq-32b --reasoning
        """
    )
    
    # Test suite options
    parser.add_argument("--all", action="store_true", 
                       help="Run all test suites (comprehensive)")
    parser.add_argument("--quick", action="store_true", 
                       help="Quick test with a single working model")
    parser.add_argument("--models", action="store_true", 
                       help="Test all models (test_all_models.py)")
    parser.add_argument("--thinking", action="store_true", 
                       help="Test thinking capabilities (test_thinking.py)")
    parser.add_argument("--providers", action="store_true", 
                       help="Test all providers (test_providers.py)")
    
    # Specific tests
    parser.add_argument("--model", help="Test specific model")
    parser.add_argument("--provider", help="Test specific provider")
    
    # Model test options
    parser.add_argument("--stream", action="store_true", help="Enable streaming")
    parser.add_argument("--reasoning", action="store_true", help="Use reasoning prompt")
    parser.add_argument("--creative", action="store_true", help="Use creative prompt")
    parser.add_argument("--code", action="store_true", help="Use code prompt")
    
    # Thinking test options
    parser.add_argument("--thinking-test", help="Specific thinking test to run")
    
    # Provider test options
    parser.add_argument("--provider-test", 
                       choices=["basic", "streaming", "thinking", "edge_cases"],
                       help="Specific provider test to run")
    
    # Utility options
    parser.add_argument("--list", action="store_true", 
                       help="List available models and providers")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    
    args = parser.parse_args()
    
    print_header("🚀 MonoLLM Test Runner")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    exit_code = 0
    
    try:
        if args.list:
            # List available options
            print("\n📋 Listing available models and providers...")
            run_script("test_single_model.py", ["--help"])
            run_script("test_providers.py", ["--list-providers"])
            run_script("test_thinking.py", ["--list-tests"])
            
        elif args.quick:
            # Quick test with a known working model
            print("\n⚡ Running quick test...")
            print("Testing QwQ-32B with reasoning (known to work well)")
            exit_code = run_script("test_single_model.py", 
                                 ["qwq-32b", "--reasoning", "--stream"])
            
        elif args.all:
            # Run all test suites
            print("\n🎯 Running comprehensive test suite...")
            
            print("\n1️⃣ Testing all models...")
            models_result = run_script("test_all_models.py")
            
            print("\n2️⃣ Testing thinking capabilities...")
            thinking_result = run_script("test_thinking.py")
            
            print("\n3️⃣ Testing all providers...")
            providers_result = run_script("test_providers.py")
            
            # Summary
            results = [models_result, thinking_result, providers_result]
            passed = sum(1 for r in results if r == 0)
            total = len(results)
            
            print_header("📊 Comprehensive Test Summary")
            print(f"Test suites passed: {passed}/{total}")
            if passed == total:
                print("🎉 All test suites completed successfully!")
            else:
                print("⚠️  Some test suites had issues. Check output above.")
                exit_code = 1
            
        elif args.models:
            # Test all models
            print("\n🤖 Testing all models...")
            exit_code = run_script("test_all_models.py")
            
        elif args.thinking:
            # Test thinking capabilities
            print("\n🧠 Testing thinking capabilities...")
            script_args = []
            if args.model:
                script_args.extend(["--model", args.model])
            if args.thinking_test:
                script_args.extend(["--test", args.thinking_test])
            exit_code = run_script("test_thinking.py", script_args)
            
        elif args.providers:
            # Test all providers
            print("\n🔧 Testing all providers...")
            exit_code = run_script("test_providers.py")
            
        elif args.model:
            # Test specific model
            print(f"\n🎯 Testing model: {args.model}")
            script_args = [args.model]
            
            if args.stream:
                script_args.append("--stream")
            if args.reasoning:
                script_args.append("--reasoning")
            if args.creative:
                script_args.append("--creative")
            if args.code:
                script_args.append("--code")
                
            exit_code = run_script("test_single_model.py", script_args)
            
        elif args.provider:
            # Test specific provider
            print(f"\n🔧 Testing provider: {args.provider}")
            script_args = ["--provider", args.provider]
            
            if args.provider_test:
                script_args.extend(["--test", args.provider_test])
                
            exit_code = run_script("test_providers.py", script_args)
            
        else:
            # No specific test selected, show help
            parser.print_help()
            print("\n💡 Quick start suggestions:")
            print("  python test/run_tests.py --quick          # Quick test")
            print("  python test/run_tests.py --thinking       # Test reasoning models")
            print("  python test/run_tests.py --model qwq-32b  # Test specific model")
            print("  python test/run_tests.py --all            # Comprehensive tests")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
        exit_code = 1
    except Exception as e:
        print(f"\n\n❌ Test runner failed: {e}")
        exit_code = 1
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return exit_code

if __name__ == "__main__":
    exit(main()) 