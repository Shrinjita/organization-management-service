#!/usr/bin/env python3
"""
Final verification script for Organization Management Service setup.
Checks if everything is properly configured and ready to run.
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)

def check_python_version():
    """Check Python version"""
    print(f"{Fore.CYAN}Checking Python version...{Style.RESET_ALL}")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"{Fore.GREEN}✓ Python {version.major}.{version.minor}.{version.micro}{Style.RESET_ALL}")
        return True
    else:
        print(f"{Fore.RED}✗ Python 3.9+ required (found {version.major}.{version.minor}.{version.micro}){Style.RESET_ALL}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print(f"\n{Fore.CYAN}Checking dependencies...{Style.RESET_ALL}")
    
    dependencies = [
        "fastapi",
        "uvicorn",
        "pymongo",
        "pydantic",
        "jose",
        "passlib",
        "dotenv"
    ]
    
    all_installed = True
    for dep in dependencies:
        spec = importlib.util.find_spec(dep)
        if spec is not None:
            print(f"{Fore.GREEN}✓ {dep}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {dep}{Style.RESET_ALL}")
            all_installed = False
    
    return all_installed

def check_files():
    """Check if required files exist"""
    print(f"\n{Fore.CYAN}Checking required files...{Style.RESET_ALL}")
    
    required_files = [
        "requirements.txt",
        ".env.example",
        "main.py",
        "src/__init__.py",
        "src/config/settings.py",
        "src/db/mongo.py",
        "src/models/organization.py",
        "src/models/admin_user.py",
        "src/routes/auth.py",
        "src/routes/organization.py",
        "src/services/organization_service.py",
        "src/services/admin_service.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"{Fore.GREEN}✓ {file_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {file_path}{Style.RESET_ALL}")
            all_exist = False
    
    return all_exist

def check_directory_structure():
    """Check directory structure"""
    print(f"\n{Fore.CYAN}Checking directory structure...{Style.RESET_ALL}")
    
    required_dirs = [
        "src",
        "src/config",
        "src/db",
        "src/models",
        "src/schemas",
        "src/services",
        "src/routes",
        "src/utils",
        "tests",
        "logs"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"{Fore.GREEN}✓ {dir_path}/{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}✗ {dir_path}/{Style.RESET_ALL}")
            all_exist = False
    
    return all_exist

def check_environment():
    """Check environment setup"""
    print(f"\n{Fore.CYAN}Checking environment...{Style.RESET_ALL}")
    
    # Check if .env exists
    if Path(".env").exists():
        print(f"{Fore.GREEN}✓ .env file exists{Style.RESET_ALL}")
        
        # Read .env and check for required variables
        try:
            with open(".env", "r") as f:
                content = f.read()
            
            required_vars = ["MONGODB_URI", "MASTER_DB_NAME", "JWT_SECRET_KEY"]
            missing_vars = []
            
            for var in required_vars:
                if f"{var}=" in content:
                    print(f"{Fore.GREEN}  ✓ {var}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}  ⚠ {var} (missing or commented){Style.RESET_ALL}")
                    missing_vars.append(var)
            
            if missing_vars:
                print(f"{Fore.YELLOW}Warning: Some environment variables may be missing{Style.RESET_ALL}")
                return False
            else:
                return True
                
        except Exception as e:
            print(f"{Fore.RED}✗ Error reading .env: {e}{Style.RESET_ALL}")
            return False
    else:
        print(f"{Fore.YELLOW}⚠ .env file not found (copy .env.example to .env){Style.RESET_ALL}")
        return False

def run_syntax_check():
    """Run syntax check on Python files"""
    print(f"\n{Fore.CYAN}Running syntax check...{Style.RESET_ALL}")
    
    python_files = []
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    python_files.append("main.py")
    
    all_valid = True
    for file in python_files:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"{Fore.GREEN}✓ {file}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ {file}{Style.RESET_ALL}")
                if result.stderr:
                    print(f"  Error: {result.stderr[:100]}...")
                all_valid = False
        except Exception as e:
            print(f"{Fore.RED}✗ Error checking {file}: {e}{Style.RESET_ALL}")
            all_valid = False
    
    return all_valid

def main():
    """Main verification function"""
    print(f"{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Organization Management Service - Setup Verification{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Required Files", check_files),
        ("Environment Setup", check_environment),
        ("Syntax Check", run_syntax_check)
    ]
    
    results = []
    for check_name, check_function in checks:
        print(f"\n{Fore.CYAN}[{check_name}]{Style.RESET_ALL}")
        try:
            result = check_function()
            results.append((check_name, result))
        except Exception as e:
            print(f"{Fore.RED}Error during {check_name}: {e}{Style.RESET_ALL}")
            results.append((check_name, False))
    
    # Summary
    print(f"\n{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Verification Summary{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        if result:
            print(f"{Fore.GREEN}✓ {check_name}: PASSED{Style.RESET_ALL}")
            passed += 1
        else:
            print(f"{Fore.RED}✗ {check_name}: FAILED{Style.RESET_ALL}")
    
    print(f"\n{Fore.BLUE}{'=' * 60}{Style.RESET_ALL}")
    print(f"Total: {passed}/{total} checks passed")
    
    if passed == total:
        print(f"\n{Fore.GREEN}✅ All checks passed! Setup is complete.{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Next steps:{Style.RESET_ALL}")
        print("1. Make sure MongoDB is running")
        print("2. Initialize database: python src/scripts/init_db.py")
        print("3. Start the service: uvicorn main:app --reload")
        print("4. Access API docs at http://localhost:8000/docs")
        return 0
    else:
        print(f"\n{Fore.YELLOW}⚠ Some checks failed. Please fix the issues above.{Style.RESET_ALL}")
        return 1

if __name__ == "__main__":
    sys.exit(main())