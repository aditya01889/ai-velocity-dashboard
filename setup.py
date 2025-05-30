from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-velocity-dashboard",
    version="0.1.0",
    author="AI Team",
    author_email="ai-team@example.com",
    description="AI Velocity Dashboard - Monitor your AI development team's productivity, test coverage, and infrastructure health.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ai-velocity-dashboard",
    packages=find_packages(include=["app", "app.*"]),
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.md"],
    },
    python_requires=">=3.10",
    install_requires=[
        "streamlit>=1.32.0",
        "python-dotenv>=1.0.1",
        "pydantic>=2.6.1",
        "fastapi>=0.109.2",
        "uvicorn>=0.27.0",
        "PyGithub>=2.1.1",
        "langsmith>=0.0.87",
        "pandas>=2.1.4",
        "numpy>=1.26.3",
        "plotly>=5.18.0",
        "matplotlib>=3.8.2",
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "isort>=5.13.2",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "types-python-dateutil>=2.8.19",
            "types-requests>=2.31.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Monitoring",
    ],
    entry_points={
        "console_scripts": [
            "ai-velocity-dashboard=app.main:main",
        ],
    },
)
