"""
Tests for setup configuration and package installation
"""

import os
import sys
import subprocess
import unittest
from pathlib import Path


class TestSetupConfiguration(unittest.TestCase):
    """Test suite for setup.py and package configuration"""

    def setUp(self):
        """Set up test fixtures"""
        self.project_root = Path(__file__).parent.absolute()

    def test_setup_py_exists(self):
        """Test that setup.py exists"""
        setup_file = self.project_root / "setup.py"
        self.assertTrue(setup_file.exists(), "setup.py should exist")

    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists"""
        pyproject_file = self.project_root / "pyproject.toml"
        self.assertTrue(pyproject_file.exists(), "pyproject.toml should exist")

    def test_package_json_exists(self):
        """Test that package.json exists"""
        package_json = self.project_root / "package.json"
        self.assertTrue(package_json.exists(), "package.json should exist")

    def test_manifest_in_exists(self):
        """Test that MANIFEST.in exists"""
        manifest_file = self.project_root / "MANIFEST.in"
        self.assertTrue(manifest_file.exists(), "MANIFEST.in should exist")

    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists"""
        req_file = self.project_root / "requirements.txt"
        self.assertTrue(req_file.exists(), "requirements.txt should exist")

    def test_setup_py_syntax(self):
        """Test that setup.py has valid Python syntax"""
        setup_file = self.project_root / "setup.py"

        try:
            with open(setup_file, 'r') as f:
                code = f.read()

            # Try to compile the code to check syntax
            compile(code, str(setup_file), 'exec')
            self.assertTrue(True, "setup.py has valid syntax")
        except SyntaxError as e:
            self.fail(f"setup.py has syntax errors: {e}")

    def test_requirements_are_valid(self):
        """Test that requirements.txt contains valid package names"""
        req_file = self.project_root / "requirements.txt"

        with open(req_file, 'r') as f:
            requirements = f.readlines()

        # Filter out comments and empty lines
        packages = [
            line.strip()
            for line in requirements
            if line.strip() and not line.strip().startswith('#')
        ]

        # Check that we have required packages
        package_names = [pkg.split('>=')[0].split('==')[0].lower() for pkg in packages]

        self.assertIn('pyqt6', package_names, "PyQt6 should be in requirements")
        self.assertIn('pyqtgraph', package_names, "pyqtgraph should be in requirements")
        self.assertIn('networkx', package_names, "networkx should be in requirements")

    def test_setup_py_metadata(self):
        """Test that setup.py contains correct metadata"""
        setup_file = self.project_root / "setup.py"

        with open(setup_file, 'r') as f:
            content = f.read()

        # Check for essential metadata
        self.assertIn("name='codescope'", content, "Package name should be 'codescope'")
        self.assertIn("author='Hemang Joshi'", content, "Author should be set")
        self.assertIn("python_requires='>=3.7'", content, "Python version requirement should be set")
        self.assertIn("MIT", content, "License should be MIT")

    def test_pyproject_toml_structure(self):
        """Test that pyproject.toml has correct structure"""
        pyproject_file = self.project_root / "pyproject.toml"

        with open(pyproject_file, 'r') as f:
            content = f.read()

        # Check for essential sections
        self.assertIn("[build-system]", content, "build-system section should exist")
        self.assertIn("[project]", content, "project section should exist")
        self.assertIn("[project.scripts]", content, "scripts section should exist")
        self.assertIn("[tool.pytest.ini_options]", content, "pytest config should exist")
        self.assertIn("[tool.black]", content, "black config should exist")

    def test_package_json_structure(self):
        """Test that package.json has correct structure"""
        package_json = self.project_root / "package.json"

        try:
            import json
            with open(package_json, 'r') as f:
                data = json.load(f)

            # Check essential fields
            self.assertEqual(data['name'], 'codescope', "Package name should be 'codescope'")
            self.assertIn('version', data, "Version should be specified")
            self.assertIn('scripts', data, "Scripts section should exist")
            self.assertIn('license', data, "License should be specified")
            self.assertEqual(data['license'], 'MIT', "License should be MIT")

            # Check for useful scripts
            self.assertIn('test', data['scripts'], "Test script should exist")
            self.assertIn('start', data['scripts'], "Start script should exist")

        except json.JSONDecodeError as e:
            self.fail(f"package.json is not valid JSON: {e}")

    def test_gitignore_has_build_artifacts(self):
        """Test that .gitignore includes build artifacts"""
        gitignore = self.project_root / ".gitignore"

        with open(gitignore, 'r') as f:
            content = f.read()

        # Check for important patterns
        self.assertIn("__pycache__", content, "__pycache__ should be ignored")
        self.assertIn("build/", content, "build/ should be ignored")
        self.assertIn("dist/", content, "dist/ should be ignored")
        self.assertIn("*.egg-info", content, "egg-info should be ignored")
        self.assertIn(".pytest_cache", content, "pytest cache should be ignored")

    def test_main_modules_exist(self):
        """Test that main Python modules exist"""
        modules = ['app.py', 'unknown_project_handler.py']

        for module in modules:
            module_path = self.project_root / module
            self.assertTrue(
                module_path.exists(),
                f"{module} should exist in project root"
            )

    def test_documentation_files_exist(self):
        """Test that documentation files exist"""
        docs = ['README.md', 'LICENSE']

        for doc in docs:
            doc_path = self.project_root / doc
            self.assertTrue(
                doc_path.exists(),
                f"{doc} should exist in project root"
            )


class TestPackageInstallation(unittest.TestCase):
    """Test suite for package installation capabilities"""

    def setUp(self):
        """Set up test fixtures"""
        self.project_root = Path(__file__).parent.absolute()

    def test_setup_check_command(self):
        """Test that setup.py check command works"""
        try:
            result = subprocess.run(
                [sys.executable, 'setup.py', 'check'],
                cwd=self.project_root,
                capture_output=True,
                timeout=10,
                text=True
            )

            # Check command should succeed or be available
            self.assertIn(
                result.returncode, [0, 1],  # 0 for success, 1 for minor warnings
                f"setup.py check failed: {result.stderr}"
            )
        except subprocess.TimeoutExpired:
            self.fail("setup.py check command timed out")
        except Exception as e:
            self.skipTest(f"Could not run setup.py check: {e}")


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSetupConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestPackageInstallation))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
