# Contributing to AI Velocity Dashboard

Thank you for your interest in contributing to the AI Velocity Dashboard! We welcome contributions from the community to help improve this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [Code Style and Guidelines](#code-style-and-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [License](#license)

## Code of Conduct

This project adheres to the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/your-username/ai-velocity-dashboard.git
   cd ai-velocity-dashboard
   ```
3. **Set up the development environment** (see below).

## Development Setup

### Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) (optional)

### Installation

1. **Install Python dependencies** with Poetry:
   ```bash
   poetry install
   ```

2. **Set up pre-commit hooks** (optional but recommended):
   ```bash
   pre-commit install
   ```

3. **Set up environment variables** by copying the example file:
   ```bash
   cp .env.example .env
   ```
   Then, update the `.env` file with your configuration.

### Running the Application

#### Local Development

```bash
# Start the development server
make run

# Or run with hot-reloading
uvicorn app.main:app --reload
```

#### Docker

```bash
# Build and start the application
make docker-run

# View logs
make docker-logs

# Stop the application
make docker-down
```

## Making Changes

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number-description
   ```

2. **Make your changes** following the [code style guidelines](#code-style-and-guidelines).

3. **Run tests** to ensure nothing is broken:
   ```bash
   make test
   ```

4. **Format and lint** your code:
   ```bash
   make format lint
   ```

5. **Commit your changes** with a descriptive commit message:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

## Submitting a Pull Request

1. Go to the [repository](https://github.com/your-org/ai-velocity-dashboard) on GitHub.
2. Click on the "Compare & pull request" button.
3. Fill in the PR template with details about your changes.
4. Submit the pull request.

## Reporting Issues

If you find a bug or have a feature request, please [open an issue](https://github.com/your-org/ai-velocity-dashboard/issues/new/choose) with the following information:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Screenshots or logs (if applicable)
- Your environment (OS, Python version, etc.)

## Code Style and Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use type hints for all function signatures and variables.
- Write docstrings for all public functions, classes, and modules following the [Google style guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
- Keep functions small and focused on a single responsibility.
- Write meaningful commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Testing

- Write unit tests for all new features and bug fixes.
- Ensure all tests pass before submitting a pull request.
- Aim for good test coverage (80%+).

To run tests:

```bash
# Run all tests
make test

# Run tests with coverage
make test-cov

# Run a specific test file
pytest tests/test_module.py

# Run a specific test function
pytest tests/test_module.py::test_function_name
```

## Documentation

- Update the README.md with any changes to the setup or usage instructions.
- Add docstrings to all new functions, classes, and modules.
- Update the CHANGELOG.md with a summary of your changes.

## License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).
