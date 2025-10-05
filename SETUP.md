# CodeScope Setup and Configuration Guide

This document provides comprehensive information about installing, configuring, and distributing CodeScope.

## Table of Contents

- [Installation Methods](#installation-methods)
- [Development Setup](#development-setup)
- [Package Configuration](#package-configuration)
- [Build and Distribution](#build-and-distribution)
- [Testing Setup](#testing-setup)
- [Troubleshooting](#troubleshooting)

## Installation Methods

### Method 1: Standard Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/hemangjoshi37a/CodeScope.git
cd CodeScope

# Install with pip
pip install .
```

### Method 2: Development Installation

For active development, use editable installation:

```bash
# Install in editable mode with development dependencies
pip install -e .[dev]
```

This allows you to modify the code and see changes immediately without reinstalling.

### Method 3: Installation from Source

```bash
# Build distribution packages
python setup.py sdist bdist_wheel

# Install from the built wheel
pip install dist/codescope-1.0.0-py3-none-any.whl
```

### Method 4: Direct Dependency Installation

If you just want to run the application without installing the package:

```bash
pip install -r requirements.txt
python app.py
```

## Development Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- virtualenv (recommended)

### Setting Up Development Environment

1. **Create a virtual environment:**

```bash
python -m venv venv
```

2. **Activate the virtual environment:**

```bash
# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install development dependencies:**

```bash
pip install -e .[dev]
```

This installs:
- pytest (testing framework)
- pytest-cov (coverage reporting)
- black (code formatter)
- flake8 (linter)
- mypy (type checker)
- isort (import sorter)

### Running the Application

After installation, you can run CodeScope in several ways:

```bash
# Method 1: Using the installed command
codescope

# Method 2: Using Python module
python -m app

# Method 3: Direct execution
python app.py
```

## Package Configuration

### setup.py

Traditional Python packaging configuration. Key features:

- **Package Discovery**: Automatically finds all Python packages
- **Dependencies**: Reads from requirements.txt
- **Entry Points**: Provides `codescope` command-line tool
- **Metadata**: Author, license, keywords, classifiers

### pyproject.toml

Modern Python packaging standard (PEP 518). Includes:

- **Build System**: Specifies setuptools as the build backend
- **Project Metadata**: Name, version, description, dependencies
- **Tool Configuration**: Settings for black, pytest, coverage, mypy, isort
- **Scripts**: Command-line entry points

### package.json

Optional Node.js-style configuration for development scripts:

```bash
# Available npm-style scripts
npm run start        # Launch the application
npm run demo         # Run demo script
npm run test         # Run tests with coverage
npm run lint         # Run flake8 linter
npm run format       # Format code with black
npm run clean        # Clean build artifacts
npm run build        # Build distribution packages
```

### MANIFEST.in

Controls which files are included in the source distribution:

- **Included**: README, LICENSE, requirements.txt, documentation
- **Excluded**: Cache files, build artifacts, IDE settings

## Build and Distribution

### Building Distribution Packages

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build source distribution and wheel
python setup.py sdist bdist_wheel
```

This creates:
- `dist/codescope-1.0.0.tar.gz` (source distribution)
- `dist/codescope-1.0.0-py3-none-any.whl` (wheel distribution)

### Verifying the Build

```bash
# Check the distribution
twine check dist/*

# Test installation in a clean environment
pip install dist/codescope-1.0.0-py3-none-any.whl
```

### Publishing to PyPI (Maintainers Only)

```bash
# Install twine if not already installed
pip install twine

# Upload to PyPI
twine upload dist/*

# Or upload to Test PyPI first
twine upload --repository testpypi dist/*
```

## Testing Setup

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html --cov-report=term

# Run specific test file
pytest test_setup.py

# Run tests matching a pattern
pytest -k "test_setup"
```

### Test Configuration

Tests are configured in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
```

### Coverage Reports

After running tests with coverage:

```bash
# View HTML coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## Code Quality Tools

### Black (Code Formatter)

```bash
# Format all Python files
black *.py

# Check formatting without making changes
black --check *.py

# Format specific file
black app.py
```

### Flake8 (Linter)

```bash
# Lint all Python files
flake8 *.py

# Lint with specific configuration
flake8 --max-line-length=100 *.py
```

### MyPy (Type Checker)

```bash
# Type check all files
mypy *.py --ignore-missing-imports

# Type check specific file
mypy app.py
```

### isort (Import Sorter)

```bash
# Sort imports in all files
isort *.py

# Check import sorting
isort --check-only *.py
```

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'PyQt6'"

**Solution:**
```bash
pip install PyQt6
```

#### Issue: "setup.py not found" when running setup commands

**Solution:** Make sure you're in the project root directory:
```bash
cd /path/to/CodeScope
python setup.py [command]
```

#### Issue: Permission denied when installing

**Solution:** Use `--user` flag or virtual environment:
```bash
pip install --user .
```

#### Issue: Tests failing due to missing dependencies

**Solution:** Install test dependencies:
```bash
pip install -e .[test]
```

#### Issue: Import errors after installation

**Solution:** Ensure you're not in the source directory when testing installation:
```bash
cd ~
python -c "import app; app.main()"
```

### Verifying Installation

```bash
# Check if package is installed
pip show codescope

# Verify command is available
which codescope  # Linux/macOS
where codescope  # Windows

# Test import
python -c "import app; print('Import successful')"
```

## Environment Variables

CodeScope doesn't require environment variables, but you can configure:

```bash
# Set Python path (if needed)
export PYTHONPATH=/path/to/CodeScope:$PYTHONPATH

# Set log level
export CODESCOPE_LOG_LEVEL=DEBUG
```

## Dependency Management

### Core Dependencies

- **PyQt6** (>=6.0.0): GUI framework
- **pyqtgraph** (>=0.12.0): Graph visualization
- **networkx** (>=2.5): Graph algorithms

### Development Dependencies

- **pytest** (>=6.0): Testing framework
- **pytest-cov** (>=2.0): Coverage plugin
- **black** (>=22.0): Code formatter
- **flake8** (>=4.0): Linter
- **mypy** (>=0.950): Type checker

### Updating Dependencies

```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade PyQt6
```

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [setuptools Documentation](https://setuptools.pypa.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)

## Contributing

When contributing to CodeScope setup configuration:

1. Test your changes with `pytest test_setup.py`
2. Ensure all tests pass
3. Update this documentation if needed
4. Follow PEP 8 style guidelines
5. Add comments for complex setup logic

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Last Updated:** 2025-10-05
**Version:** 1.0.0
