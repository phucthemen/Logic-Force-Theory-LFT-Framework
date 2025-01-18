from setuptools import setup, find_packages

setup(
    name="lft-framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "qiskit>=0.34.2",
        "torch>=1.9.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "sphinx>=4.0.2",
            "flake8>=3.9.0",
            "black>=21.5b2",
            "mypy>=0.910",
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A framework for measuring and applying logical forces in quantum-enhanced AI systems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lft-framework",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
)
