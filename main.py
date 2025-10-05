#!/usr/bin/env python3
"""
CodeScope - Python Code Visualization Tool
Main Entry Point

This module serves as the primary entry point for the CodeScope application.
It handles initialization, command-line argument parsing, and application startup.

Usage:
    python main.py [options]

    Options:
        --file <path>       Open a specific Python file on startup
        --debug             Enable debug logging
        --version           Show version information
        --help              Show this help message

Example:
    python main.py
    python main.py --file my_script.py
    python main.py --debug
"""

import sys
import os
import argparse
import logging
from typing import Optional

# Ensure imports work correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Import after path setup
from app import CodeVisualizationTool

__version__ = "1.0.0"
__author__ = "HJLabs"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def setup_argument_parser() -> argparse.ArgumentParser:
    """
    Set up command-line argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog='CodeScope',
        description='Python Code Visualization Tool - Transform complex codebases into intuitive visual representations',
        epilog=f'Version {__version__} | Made by {__author__}'
    )

    parser.add_argument(
        '--file', '-f',
        type=str,
        metavar='PATH',
        help='Path to Python file to open on startup'
    )

    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug logging for troubleshooting'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    return parser


def validate_file_path(file_path: str) -> Optional[str]:
    """
    Validate that the provided file path exists and is a Python file.

    Args:
        file_path: Path to the file to validate

    Returns:
        str: Absolute path to the file if valid, None otherwise
    """
    if not file_path:
        return None

    # Convert to absolute path
    abs_path = os.path.abspath(file_path)

    # Check if file exists
    if not os.path.exists(abs_path):
        logger.error(f"File not found: {file_path}")
        return None

    # Check if it's a file (not directory)
    if not os.path.isfile(abs_path):
        logger.error(f"Path is not a file: {file_path}")
        return None

    # Check if it's a Python file
    if not abs_path.endswith('.py'):
        logger.warning(f"File does not have .py extension: {file_path}")
        # Allow it anyway - user might want to visualize it

    return abs_path


def load_file_content(file_path: str) -> Optional[str]:
    """
    Load content from a Python file.

    Args:
        file_path: Path to the file to load

    Returns:
        str: File content if successful, None otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"Successfully loaded file: {file_path}")
        return content
    except UnicodeDecodeError:
        logger.error(f"Failed to decode file with UTF-8 encoding: {file_path}")
        try:
            # Try alternative encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
            logger.warning(f"Loaded file with latin-1 encoding: {file_path}")
            return content
        except Exception as e:
            logger.error(f"Failed to load file with alternative encoding: {e}")
            return None
    except Exception as e:
        logger.error(f"Failed to load file: {e}")
        return None


def main():
    """
    Main entry point for the CodeScope application.

    Handles:
        - Command-line argument parsing
        - Application initialization
        - File loading (if specified)
        - Error handling and logging
    """
    # Parse command-line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Configure logging level based on debug flag
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    logger.info(f"Starting CodeScope v{__version__}")

    # Validate file path if provided
    initial_code = None
    if args.file:
        logger.info(f"Attempting to load file: {args.file}")
        file_path = validate_file_path(args.file)
        if file_path:
            initial_code = load_file_content(file_path)
            if initial_code is None:
                logger.error("Failed to load file content. Starting with default code.")
        else:
            logger.error("Invalid file path. Starting with default code.")

    try:
        # Initialize Qt Application
        # Enable high DPI scaling for better display on modern screens
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        app = QApplication(sys.argv)
        app.setApplicationName("CodeScope")
        app.setApplicationVersion(__version__)

        logger.debug("Qt Application initialized")

        # Create main window
        window = CodeVisualizationTool()

        # Load initial code if provided
        if initial_code:
            window.code_editor.setPlainText(initial_code)
            logger.info("Initial code loaded into editor")

        # Show the window
        window.show()
        logger.info("Application window displayed")

        # Start the application event loop
        exit_code = app.exec()
        logger.info(f"Application exited with code: {exit_code}")
        sys.exit(exit_code)

    except ImportError as e:
        logger.critical(f"Failed to import required modules: {e}")
        logger.critical("Please ensure all dependencies are installed:")
        logger.critical("  pip install PyQt6 pyqtgraph networkx")
        sys.exit(1)

    except Exception as e:
        logger.critical(f"Unexpected error during application startup: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
