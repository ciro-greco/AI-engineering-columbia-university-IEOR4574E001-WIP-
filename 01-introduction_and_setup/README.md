# Week 1: Environment Setup & Course Workflow

## Overview

This week you'll set up your development environment and learn the submission workflow for assignments and your capstone project.

## Setup Checklist

1. [GitHub Account & Repository Setup](#github-account--repository-setup)
2. [Installing Git](#installing-git)
3. [Installing Python](#installing-python)
4. [Virtual Environments](#virtual-environments)
5. [Installing Required Libraries](#installing-required-libraries)
6. [GPU Setup (Optional)](#gpu-setup-optional)
7. [Assignment Submission Workflow](#assignment-submission-workflow)
8. [Testing Your Setup](#testing-your-setup)

## 1. GitHub Account & Repository Setup

### Creating Your GitHub Account

1. Go to [github.com](https://github.com) and sign up
2. Choose a professional username (pick a reasonable one, you'll use this throughout your career)
3. (Optional) Enable two-factor authentication for security (you will have to at a certain point of your career so you might as well...)

### Creating Your Course Repository

You'll maintain ONE repository for all coursework:

```bash
# Create a new repository on GitHub named: IEOR4574-Assignments-[YourUNI]
# Example: IEOR4574-Assignments-abc123

# Make it PRIVATE (required for academic integrity)
# Initialize with README
# Add .gitignore template: Python
```

### Repository Structure

Your repository should follow this structure:

```
IEOR4574-Assignments-[YourUNI]/
├── README.md
├── .gitignore
├── Assignment-1/
    ├── requirements.txt
    ├── README.md
    └── ...
├── Assignment-2/
    ├── requirements.txt
    ├── README.md
    └── ...
└── capstone-project/
    ├── proposal.md
    ├── src/
    ├── data/
    └── final-report.md
```

### Adding Course Staff as Collaborators

1. Go to Settings → Manage access
2. Click "Add people"
3. Add the following GitHub usernames:
   - `ciro-greco` (Instructor)
   - `[TA-username-1]` (TA)
   - `[TA-username-2]` (TA)

## 2. Installing Git

### Mac Installation

```bash
# Git comes with Xcode Command Line Tools
xcode-select --install

# Or via Homebrew
brew install git
```

### Linux Installation

```bash
# Ubuntu/Debian
sudo apt-get install git

# Fedora
sudo dnf install git
```

### Windows Installation

Download from [git-scm.com](https://git-scm.com/download/win) or use WSL:

```bash
# In WSL
sudo apt-get install git
```

### Configure Git

```bash
# Set your identity (use your real name for submissions)
git config --global user.name "Your Full Name"
git config --global user.email "uni@columbia.edu"

# Set default branch name
git config --global init.defaultBranch main
```

## 3. Installing Python

This course requires Python version 3.8 or higher (latest stable version is 3.11 as of 2024).

### Mac Installation Instructions

We recommend using Homebrew for installation:

```bash
# Install Homebrew if you haven't already
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

#### Apple Silicon (M1/M2/M3) Macs

For Apple Silicon Macs, install additional dependencies:

```bash
# Install required dependencies
brew install cmake libomp openblas hdf5 

# Add to your ~/.zshrc or ~/.bashrc
export OPENBLAS=$(brew --prefix openblas)
export CFLAGS="-falign-functions=8 ${CFLAGS}"
```

### Linux Installation Instructions

Use your distribution's package manager:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Fedora
sudo dnf install python3.11 python3-pip
```

### Windows Installation Instructions

We strongly recommend using [Windows Subsystem for Linux (WSL2)](https://learn.microsoft.com/en-us/windows/wsl/install):

```powershell
# In PowerShell as Administrator
wsl --install
```

Then follow the Linux instructions above. Alternatively, download Python from [python.org](https://www.python.org/downloads/).

### Verifying Installation

```bash
python3 --version  # Should show Python 3.8+ - probably Python 3.11 if you followed the instructions above 
pip3 --version     # Should show your pip version
```

## 3. Virtual Environments

Virtual environments isolate project dependencies. **Always use one for Python projects - I know it's annoying, but it's a best practice that will pay off 100x**

### Creating a Virtual Environment

```bash
# Navigate to your project directory
cd ~/AI-engineering-IEOR4574E001

# Create virtual environment
python3 -m venv .venv

# Activate it (Mac/Linux)
source .venv/bin/activate

# Activate it (Windows)
.venv\Scripts\activate

# Your prompt should now show (venv)
```
**OPTIONAL** You can also use `uv` if you want a more modern package manager (https://docs.astral.sh/uv/). It a very nice and really fast Python package and project manager written in Rust.

### Deactivating and removing

```bash
deactivate
rm -r .venv
```

## 4. Installing Required Libraries

### Core Dependencies

With your virtual environment activated:

```bash
# Create requirements.txt with core dependencies
cat > requirements.txt << EOF
torch>=2.0.0
transformers>=4.30.0
numpy>=1.23.0
pandas>=2.0.0
matplotlib>=3.6.0
jupyter>=1.0.0
ipykernel>=6.20.0
scikit-learn>=1.2.0
sentencepiece>=0.1.99
accelerate>=0.20.0
datasets>=2.12.0
tokenizers>=0.13.0
tqdm>=4.65.0
sentence-transformers>=2.2.0
bitsandbytes>=0.39.0
huggingface-hub>=0.15.0
psutil>=5.9.0
EOF

# Install all requirements
pip install -r requirements.txt
```

### Or install directly:
```bash
pip install torch transformers numpy pandas matplotlib jupyter \
           scikit-learn sentencepiece accelerate datasets tokenizers tqdm \
           sentence-transformers bitsandbytes huggingface-hub psutil
```


## 5. Testing Your Setup

## 6. Assignment Submission Workflow

### Weekly Assignment Process

1. **Clone your repository** (first time only):
```bash
git clone https://github.com/[your-username]/IEOR4574-Assignments-[YourUNI].git
cd IEOR4574-Assignments-[YourUNI]
```

2. **Create week folder and complete assignment**:
```bash
# Create folder for the week
mkdir 02-introduction-to-LLMs
cd 02-introduction-to-LLMs

# Copy assignment template from course repo or create new notebook
# Complete your work in Jupyter
jupyter notebook assignment2.ipynb
```

3. **Commit and push your work**:
```bash
# Check what files changed
git status

# Add your assignment files
git add 02-introduction-to-LLMs/assignment2.ipynb
git add 02-introduction-to-LLMs/README.md  # Include any notes or documentation

# Commit with descriptive message
git commit -m "Week 2: Complete language model assignment"

# Push to GitHub
git push origin main
```

4. **Verify submission**:
- Go to your GitHub repository
- Check that files appear correctly
- Ensure notebook outputs are visible

### Submission Guidelines

#### DO's
- ✅ Commit regularly (don't wait until deadline)
- ✅ Include all outputs in notebooks (run all cells before submitting)
- ✅ Use clear commit messages
- ✅ Include README.md with any special instructions
- ✅ Test your code in a fresh environment

#### DON'Ts
- ❌ Don't upload large files (>100MB) - use .gitignore
- ❌ Don't include API keys or passwords
- ❌ Don't copy other students' code
- ❌ Don't submit incomplete notebooks


## 7. Running Notebooks

### Important: Everything Works on CPU! 

All course notebooks are designed to be **extremely accessible** and run perfectly on any laptop with CPU only. We intentionally chose small models (TinyLlama, GPT-2, BERT-base) so you don't need expensive hardware.

### Starting Jupyter

```bash
# Activate your virtual environment
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows

# Start Jupyter Lab (recommended) or Notebook
jupyter lab
# or
jupyter notebook
```

Your browser will open to the Jupyter interface. Navigate to any `.ipynb` file and start coding!

### If You Want GPU Acceleration (Optional)

**99% of students should skip this section** - CPU is perfectly fine for this course!

If you really want GPU acceleration, you have two options:

1. **Google Colab (STRONGLY RECOMMENDED)** 
   - Free GPU access (more than enough for this course)
   - Zero setup required
   - Just upload your notebook and enable GPU runtime
   - Go to Runtime → Change runtime type → GPU

2. **Local CUDA Setup (Advanced Users Only)**️
   - Much more complex
   - Requires NVIDIA GPU + driver installation
   - See "GPU Setup (Advanced)" section at the bottom of this README
   - **Only attempt if you're comfortable with system administration**

**Bottom line**: Start with CPU. If notebooks feel slow, try Google Colab. Local GPU setup should be your last resort.

## 8. Testing Your Setup

### Complete Setup Test

Create `test_setup.py`:

```python
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
    print("="*50)
    print("AI Engineering Course - Environment Test")
    print("="*50)
    
    test_python_version()
    test_core_libraries()
    test_pytorch()
    test_transformers()
    test_git()
    
    print("="*50)
    print("Setup complete! You're ready for the course.")
```

Run the test:

```bash
python test_setup.py
```

### Expected Output

```
==================================================
AI Engineering Course - Environment Test
==================================================
✓ Python 3.11.5
✓ numpy installed
✓ pandas installed
✓ matplotlib installed
✓ sklearn installed
✓ PyTorch 2.0.1
  └─ CPU only
✓ Transformers working
  └─ Test tokenization: [15496, 11, 2159, 0]
✓ Git installed: git version 2.39.2
  └─ User: Your Full Name
  └─ Email: uni@columbia.edu
==================================================
Setup complete! You're ready for the course.
```

## Troubleshooting

### Common Issues

1. **Git Issues**
   - "Permission denied": Check your SSH keys or use HTTPS
   - "Repository not found": Ensure you've created it and have access
   - Large files: Use `.gitignore` for data files, model weights

2. **Python/Package Issues**
   - "No module named 'torch'": Virtual environment not activated
   - Out of memory: Use Colab or reduce batch sizes
   - SSL errors on Mac: `pip install --upgrade certifi`

3. **Jupyter Issues**
   - Kernel not found: Run `python -m ipykernel install --user`
   - Can't see outputs: Clear and re-run all cells before committing

   
### GPU Setup (Advanced)

**Note**: GPU setup is completely optional. All course materials work perfectly on CPU!

#### Google Colab (Easiest Option)
- No local GPU setup needed
- Free GPU access via [Google Colab](https://colab.research.google.com)
- Just upload your notebooks and enable GPU runtime

#### Local NVIDIA GPU Setup
For those with NVIDIA GPUs who want local acceleration:

```bash
# First, check if your GPU is detected
nvidia-smi  # Should show your GPU info

# Install CUDA-enabled PyTorch (check pytorch.org for latest)
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1  
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Test GPU availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

#### Apple Silicon GPU (MPS)
For M1/M2/M3 Macs, PyTorch supports Metal Performance Shaders:

```python
import torch
print(f"MPS available: {torch.backends.mps.is_available()}")
# If True, models will automatically use Apple's GPU
```

If GPU setup fails, just use CPU. The course is designed to work well without GPUs!
