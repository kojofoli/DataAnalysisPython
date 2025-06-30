#!/usr/bin/env python3
"""
Setup script for development environment.
This script helps set up the development environment with all necessary tools.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("Setting up Temperature Toolkit development environment...")
    print("=" * 60)

    # Check if we're in a virtual environment
    if not hasattr(sys, "real_prefix") and not (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("⚠️  Warning: You're not in a virtual environment.")
        print("   Consider creating one with: python -m venv venv")
        print("   Then activate it and run this script again.")
        print()

    # Install development dependencies
    print("Installing development dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("Failed to install requirements. Please check your Python environment.")
        return False

    # Install pre-commit hooks
    print("\nSetting up pre-commit hooks...")
    if not run_command("pre-commit install", "Installing pre-commit hooks"):
        print("Failed to install pre-commit hooks. Continuing without them.")

    # Run initial checks
    print("\nRunning initial code quality checks...")

    # Format code with black
    if not run_command("black .", "Formatting code with Black"):
        print("Black formatting failed. Please check your code.")

    # Run flake8
    if not run_command("flake8 .", "Running Flake8 linting"):
        print("Flake8 found issues. Please fix them.")

    # Run mypy type checking
    if not run_command("mypy temperature_toolkit/", "Running MyPy type checking"):
        print("MyPy found type issues. Please fix them.")

    # Run tests
    print("\nRunning tests...")
    if not run_command(
        "python -m pytest test_temperature_toolkit.py -v", "Running test suite"
    ):
        print("Tests failed. Please fix the issues.")

    print("\n" + "=" * 60)
    print("✓ Development environment setup complete!")
    print("\nNext steps:")
    print("1. Run 'python main.py' to see the demo")
    print("2. Run 'python test_temperature_toolkit.py' to run tests")
    print("3. Use 'black .' to format code")
    print("4. Use 'flake8 .' to check code style")
    print("5. Use 'mypy temperature_toolkit/' to check types")
    print("\nHappy coding! 🚀")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
