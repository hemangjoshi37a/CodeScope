# Main Entry Point Implementation

## Overview

This document describes the implementation of the main entry point (`main.py`) for the CodeScope Python Code Visualization Tool. The main entry point provides a clean, professional interface for launching the application with various command-line options.

## Features

### Command-Line Interface

The main entry point supports the following command-line arguments:

- `--file`, `-f PATH`: Open a specific Python file on startup
- `--debug`, `-d`: Enable debug logging for troubleshooting
- `--version`, `-v`: Display version information
- `--help`, `-h`: Show help message with usage instructions

### File Loading

- **UTF-8 Support**: Primary encoding for loading Python files
- **Fallback Encoding**: Automatically falls back to Latin-1 encoding if UTF-8 fails
- **File Validation**: Validates file paths before attempting to load
- **Error Handling**: Graceful error handling with informative error messages

### Logging

- **Configurable Logging**: Support for INFO and DEBUG log levels
- **Structured Output**: Timestamp, logger name, log level, and message
- **Console Output**: Logs written to stdout for easy debugging

### High DPI Support

- **Modern Display Compatibility**: Automatic high DPI scaling configuration
- **Qt6 Integration**: Uses Qt6's HighDpiScaleFactorRoundingPolicy

## File Structure

### main.py (242 lines)

The main entry point file contains:

1. **Documentation**: Module docstring with usage examples
2. **Imports**: All necessary imports with proper error handling
3. **Configuration**: Version, author, and logging setup
4. **Argument Parser**: Command-line argument parsing setup
5. **File Validation**: File path validation logic
6. **File Loading**: File content loading with encoding fallback
7. **Main Function**: Application initialization and startup

### test_main.py (281 lines)

Comprehensive test suite covering:

1. **Argument Parsing Tests** (8 tests):
   - Parser creation
   - File argument (long and short form)
   - Debug flag (long and short form)
   - Version flag
   - Combined arguments
   - No arguments

2. **File Validation Tests** (7 tests):
   - Valid file path
   - Nonexistent file
   - None input
   - Empty string
   - Directory path
   - Non-Python file
   - Relative path conversion

3. **File Loading Tests** (4 tests):
   - UTF-8 encoded files
   - Latin-1 encoded files (fallback)
   - Nonexistent files
   - Empty files

4. **Main Function Tests** (2 tests):
   - Main without arguments
   - Main with debug flag

**Total: 21 tests, all passing ✓**

### demo_main.py (234 lines)

Interactive demonstration script that showcases:

1. Basic usage without arguments
2. Opening specific files
3. Debug mode
4. Help command
5. Version information

The demo creates a sample Python file and provides example commands for different use cases.

## Usage Examples

### Basic Usage

```bash
# Launch with default code
python main.py

# Launch with a specific file
python main.py --file my_script.py
python main.py -f my_script.py

# Enable debug logging
python main.py --debug
python main.py -d

# Combined options
python main.py --file my_script.py --debug

# View help
python main.py --help

# Check version
python main.py --version
```

### Programmatic Usage

```python
from main import validate_file_path, load_file_content

# Validate a file path
file_path = validate_file_path('script.py')
if file_path:
    # Load file content
    content = load_file_content(file_path)
    if content:
        print(f"Loaded {len(content)} characters")
```

## Error Handling

### File Not Found

```
ERROR:main:File not found: /path/to/nonexistent.py
```

### Invalid File Path

```
ERROR:main:Path is not a file: /path/to/directory
```

### Encoding Issues

```
ERROR:main:Failed to decode file with UTF-8 encoding: file.py
WARNING:main:Loaded file with latin-1 encoding: file.py
```

### Import Errors

```
CRITICAL:main:Failed to import required modules: <error>
CRITICAL:main:Please ensure all dependencies are installed:
CRITICAL:main:  pip install PyQt6 pyqtgraph networkx
```

## Implementation Details

### Architecture

```
main.py
├── setup_argument_parser()  # Configure argparse
├── validate_file_path()     # Validate file existence
├── load_file_content()      # Load file with encoding fallback
└── main()                   # Application entry point
    ├── Parse arguments
    ├── Configure logging
    ├── Validate file (if provided)
    ├── Initialize Qt Application
    ├── Create main window
    ├── Load initial code (if provided)
    ├── Show window
    └── Start event loop
```

### Key Design Decisions

1. **Separate Entry Point**: Keep `app.py` focused on application logic, `main.py` handles CLI
2. **Encoding Fallback**: Support both UTF-8 and Latin-1 to handle various file encodings
3. **Path Validation**: Convert relative paths to absolute and validate before loading
4. **Graceful Errors**: Provide helpful error messages and fallback to default behavior
5. **Non-Python Files**: Allow loading non-.py files with a warning (user choice)
6. **Executable Bit**: File is marked executable for Unix-like systems (`chmod +x`)

### Dependencies

- **PyQt6**: GUI framework
- **argparse**: Command-line argument parsing (built-in)
- **logging**: Logging functionality (built-in)
- **os**: File system operations (built-in)
- **sys**: System-specific parameters (built-in)

## Testing

### Running Tests

```bash
# Run all tests
python test_main.py

# Run with verbose output (default)
python test_main.py -v
```

### Test Coverage

- ✅ Argument parsing: 8/8 tests passing
- ✅ File validation: 7/7 tests passing
- ✅ File loading: 4/4 tests passing
- ✅ Main function: 2/2 tests passing

**Overall: 21/21 tests passing (100%)**

### Running the Demo

```bash
# Interactive demonstration
python demo_main.py
```

Follow the prompts to see examples of different usage patterns.

## Integration with Existing Code

### Backward Compatibility

The existing `app.py` can still be run directly:

```bash
python app.py  # Still works
```

### Migration Path

Users can migrate from `python app.py` to `python main.py` gradually. Both work identically when run without arguments.

### Future Enhancements

The main entry point is designed to support future features:

1. **Configuration Files**: Could load settings from `~/.codescope/config.json`
2. **Multiple Files**: Could support loading multiple files at once
3. **Output Options**: Could add `--output` for exporting visualizations
4. **Theme Selection**: Could add `--theme dark` or `--theme light`
5. **Plugin System**: Could add `--plugin <name>` for extensions

## Version Information

- **Version**: 1.0.0
- **Author**: HJLabs
- **License**: MIT
- **Python**: 3.7+
- **Status**: Production Ready

## Summary

The main entry point implementation provides:

✅ Clean, professional CLI interface
✅ Comprehensive error handling
✅ Full test coverage (21 tests)
✅ Unicode and encoding support
✅ Detailed logging and debugging
✅ Backward compatibility
✅ Extensible architecture
✅ Complete documentation

The implementation follows Python best practices and integrates seamlessly with the existing CodeScope application.
