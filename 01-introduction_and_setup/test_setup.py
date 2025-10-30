#!/usr/bin/env python3
"""Test script to verify environment setup."""

import sys
import warnings

warnings.filterwarnings('ignore')


def test_python_version():
    """Check Python version."""
    version = sys.version_info
    assert version.major == 3 and version.minor >= 8, f"Python 3.8+ required, got {version.major}.{version.minor}"
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")


def test_core_libraries():
    """Test core library imports."""
    libraries = {
        'numpy': 'np',
        'pandas': 'pd',
        'matplotlib.pyplot': 'plt',
        'sklearn': 'sklearn',
    }

    for lib, alias in libraries.items():
        try:
            exec(f"import {lib} as {alias}")
            print(f"✓ {lib.split('.')[0]} installed")
        except ImportError:
            print(f"✗ {lib} not found")


def test_pytorch():
    """Test PyTorch installation."""
    try:
        import torch
        print(f"✓ PyTorch {torch.__version__}")

        # Check for GPU
        if torch.cuda.is_available():
            print(f"  └─ CUDA available: {torch.cuda.get_device_name(0)}")
        elif torch.backends.mps.is_available():
            print("  └─ Apple Silicon GPU available")
        else:
            print("  └─ CPU only")

    except ImportError:
        print("✗ PyTorch not found")


def test_transformers():
    """Test Hugging Face Transformers."""
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        tokens = tokenizer.encode("Hello, World!")
        print(f"✓ Transformers working")
        print(f"  └─ Test tokenization: {tokens}")
    except Exception as e:
        print(f"✗ Transformers error: {e}")


def test_git():
    """Test Git installation and configuration."""
    import subprocess
    try:
        # Check Git installation
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Git installed: {result.stdout.strip()}")

        # Check Git configuration
        user = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
        email = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)

        if user.stdout.strip():
            print(f"  └─ User: {user.stdout.strip()}")
        else:
            print("  └─ ⚠ Git user.name not set")

        if email.stdout.strip():
            print(f"  └─ Email: {email.stdout.strip()}")
        else:
            print("  └─ ⚠ Git user.email not set")

    except FileNotFoundError:
        print("✗ Git not found - please install Git")


if __name__ == "__main__":
    print("=" * 50)
    print("AI Engineering Course - Environment Test")
    print("=" * 50)

    test_python_version()
    test_core_libraries()
    test_git()  # Test Git before transformers to avoid fork issue
    test_pytorch()
    test_transformers()

    print("=" * 50)
    print("Setup complete! You're ready for the course.")