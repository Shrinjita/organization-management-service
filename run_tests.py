"""
Test runner script for Organization Management Service
"""

import subprocess
import sys
import os
from colorama import init, Fore, Style

init(autoreset=True)

def run_command(command, description):
    """Run a shell command and handle output"""
    print(f"\n{Fore.CYAN}▶ {description}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Command: {command}{Style.RESET_ALL}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}✓ Success{Style.RESET_ALL}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"{Fore.RED}✗ Failed with exit code {result.returncode}{Style.RESET_ALL}")
            if result.stderr:
                print(f"{Fore.RED}Error: {result.stderr}{Style.RESET_ALL}")
            return False
        
        return True
    
    except Exception as e:
        print(f"{Fore.RED}✗ Exception: {e}{Style.RESET_ALL}")
        return False

def main():
    """Main test runner function"""
    print(f"{Fore.BLUE}🏁 Starting Organization Management Service Test Suite{Style.RESET_ALL}")
    print(f"{Fore.BLUE}=" * 60 + Style.RESET_ALL)
    
    # Check if virtual environment is activated
    if not os.path.exists("venv") and not os.environ.get("VIRTUAL_ENV"):
        print(f"{Fore.YELLOW}⚠ Warning: Virtual environment not detected{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Consider activating it with: source venv/bin/activate{Style.RESET_ALL}")
    
    # Run tests in sequence
    tests = [
        ("pytest tests/ -v --tb=short", "Running unit tests"),
        ("pytest tests/ --cov=src --cov-report=term-missing", "Running coverage tests"),
        ("flake8 src/ tests/ --max-line-length=88", "Running code linting"),
        ("mypy src/", "Running type checking"),
    ]
    
    all_passed = True
    for command, description in tests:
        if not run_command(command, description):
            all_passed = False
    
    # Run API tests if basic tests pass
    if all_passed:
        print(f"\n{Fore.CYAN}▶ Starting API server for integration tests{Style.RESET_ALL}")
        
        # Start server in background
        server_process = subprocess.Popen(
            ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        try:
            # Wait for server to start
            import time
            time.sleep(3)
            
            # Run integration tests
            run_command(
                "pytest tests/test_integration.py -v",
                "Running integration tests"
            )
        
        finally:
            # Stop server
            server_process.terminate()
            server_process.wait()
    
    # Print summary
    print(f"\n{Fore.BLUE}=" * 60 + Style.RESET_ALL)
    if all_passed:
        print(f"{Fore.GREEN}🎉 All tests passed!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Some tests failed{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
