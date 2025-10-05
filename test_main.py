"""
Test Suite for CodeScope Main Entry Point

Tests cover:
    - Argument parsing
    - File validation
    - File loading with different encodings
    - Error handling
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import (
    setup_argument_parser,
    validate_file_path,
    load_file_content,
    __version__
)


class TestArgumentParser(unittest.TestCase):
    """Test command-line argument parsing."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = setup_argument_parser()

    def test_parser_creation(self):
        """Test that parser is created successfully."""
        self.assertIsNotNone(self.parser)
        self.assertEqual(self.parser.prog, 'CodeScope')

    def test_file_argument(self):
        """Test --file argument parsing."""
        args = self.parser.parse_args(['--file', 'test.py'])
        self.assertEqual(args.file, 'test.py')

    def test_file_argument_short_form(self):
        """Test -f short form of file argument."""
        args = self.parser.parse_args(['-f', 'script.py'])
        self.assertEqual(args.file, 'script.py')

    def test_debug_flag(self):
        """Test --debug flag."""
        args = self.parser.parse_args(['--debug'])
        self.assertTrue(args.debug)

    def test_debug_flag_short_form(self):
        """Test -d short form of debug flag."""
        args = self.parser.parse_args(['-d'])
        self.assertTrue(args.debug)

    def test_no_arguments(self):
        """Test parsing with no arguments."""
        args = self.parser.parse_args([])
        self.assertIsNone(args.file)
        self.assertFalse(args.debug)

    def test_version_flag(self):
        """Test --version flag."""
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['--version'])
        self.assertEqual(cm.exception.code, 0)

    def test_combined_arguments(self):
        """Test multiple arguments together."""
        args = self.parser.parse_args(['--file', 'test.py', '--debug'])
        self.assertEqual(args.file, 'test.py')
        self.assertTrue(args.debug)


class TestFileValidation(unittest.TestCase):
    """Test file path validation functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Create temporary test file
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False
        )
        self.temp_file.write("# Test Python file\nprint('Hello')\n")
        self.temp_file.close()

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_valid_file_path(self):
        """Test validation of valid Python file."""
        result = validate_file_path(self.temp_file.name)
        self.assertIsNotNone(result)
        self.assertTrue(os.path.isabs(result))

    def test_nonexistent_file(self):
        """Test validation of nonexistent file."""
        result = validate_file_path('/nonexistent/file.py')
        self.assertIsNone(result)

    def test_none_file_path(self):
        """Test validation with None input."""
        result = validate_file_path(None)
        self.assertIsNone(result)

    def test_empty_string_path(self):
        """Test validation with empty string."""
        result = validate_file_path('')
        self.assertIsNone(result)

    def test_directory_path(self):
        """Test validation with directory path."""
        temp_dir = tempfile.mkdtemp()
        try:
            result = validate_file_path(temp_dir)
            self.assertIsNone(result)
        finally:
            os.rmdir(temp_dir)

    def test_non_python_file(self):
        """Test validation of non-Python file (should still work)."""
        temp_txt = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False
        )
        temp_txt.write("Not Python code")
        temp_txt.close()
        try:
            result = validate_file_path(temp_txt.name)
            # Should return path even for non-.py files (with warning)
            self.assertIsNotNone(result)
        finally:
            os.unlink(temp_txt.name)

    def test_relative_path_conversion(self):
        """Test that relative paths are converted to absolute."""
        # Get just the filename
        filename = os.path.basename(self.temp_file.name)
        dirname = os.path.dirname(self.temp_file.name)

        # Change to directory and test
        original_cwd = os.getcwd()
        try:
            os.chdir(dirname)
            result = validate_file_path(filename)
            self.assertIsNotNone(result)
            self.assertTrue(os.path.isabs(result))
        finally:
            os.chdir(original_cwd)


class TestFileLoading(unittest.TestCase):
    """Test file content loading functionality."""

    def test_load_utf8_file(self):
        """Test loading UTF-8 encoded file."""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            encoding='utf-8',
            delete=False
        ) as f:
            f.write("# UTF-8 file\ndef hello():\n    print('世界')\n")
            temp_path = f.name

        try:
            content = load_file_content(temp_path)
            self.assertIsNotNone(content)
            self.assertIn('hello', content)
            self.assertIn('世界', content)
        finally:
            os.unlink(temp_path)

    def test_load_latin1_file(self):
        """Test loading Latin-1 encoded file (fallback)."""
        with tempfile.NamedTemporaryFile(
            mode='wb',
            suffix='.py',
            delete=False
        ) as f:
            # Write Latin-1 encoded content
            f.write(b"# Latin-1 file\nprint('\xe9\xe8')\n")
            temp_path = f.name

        try:
            content = load_file_content(temp_path)
            # Should succeed with fallback encoding
            self.assertIsNotNone(content)
        finally:
            os.unlink(temp_path)

    def test_load_nonexistent_file(self):
        """Test loading nonexistent file."""
        content = load_file_content('/nonexistent/file.py')
        self.assertIsNone(content)

    def test_load_empty_file(self):
        """Test loading empty file."""
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False
        ) as f:
            temp_path = f.name

        try:
            content = load_file_content(temp_path)
            self.assertIsNotNone(content)
            self.assertEqual(content, '')
        finally:
            os.unlink(temp_path)


class TestMainFunction(unittest.TestCase):
    """Test main function behavior."""

    @patch('main.QApplication')
    @patch('main.CodeVisualizationTool')
    def test_main_without_arguments(self, mock_tool, mock_app):
        """Test main function with no arguments."""
        # Mock sys.argv
        test_args = ['main.py']
        with patch.object(sys, 'argv', test_args):
            with patch('sys.exit') as mock_exit:
                from main import main
                mock_app.return_value.exec.return_value = 0
                main()
                # Verify window was created and shown
                mock_tool.return_value.show.assert_called_once()

    @patch('main.QApplication')
    @patch('main.CodeVisualizationTool')
    def test_main_with_debug_flag(self, mock_tool, mock_app):
        """Test main function with debug flag."""
        test_args = ['main.py', '--debug']
        with patch.object(sys, 'argv', test_args):
            with patch('sys.exit') as mock_exit:
                from main import main
                mock_app.return_value.exec.return_value = 0
                main()
                # Should complete without errors
                mock_tool.return_value.show.assert_called_once()


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestArgumentParser))
    suite.addTests(loader.loadTestsFromTestCase(TestFileValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestFileLoading))
    suite.addTests(loader.loadTestsFromTestCase(TestMainFunction))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
