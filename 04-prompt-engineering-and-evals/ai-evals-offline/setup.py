from setuptools import setup, find_packages
import pathlib

# Read requirements from the root-level requirements.txt
def read_requirements():
    """Read requirements.txt from the project root"""
    root_dir = pathlib.Path(__file__).parent.parent.parent
    requirements_file = root_dir / "requirements.txt"
    
    if not requirements_file.exists():
        return []
    
    with open(requirements_file, 'r') as f:
        requirements = []
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                requirements.append(line)
        return requirements

setup(
    name="ai-evals-offline",
    version="0.1.0",
    description="AI evaluation framework for offline testing",
    packages=find_packages(),
    install_requires=read_requirements(),
    python_requires=">=3.8",
    author="AI Engineering Course",
    author_email="course@example.com",
    url="https://github.com/your-repo/ai-evals-offline",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)