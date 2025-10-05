"""
Unit tests for UnknownProjectHandler

Tests various scenarios including:
- Valid code with different project types
- Malformed code with syntax errors
- Edge cases and error handling
"""

import unittest
from unknown_project_handler import UnknownProjectHandler, ProjectType, analyze_unknown_project


class TestUnknownProjectHandler(unittest.TestCase):
    """Test suite for UnknownProjectHandler class"""

    def test_web_application_detection(self):
        """Test detection of web application projects"""
        code = """
import flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertEqual(result['project_type'], ProjectType.WEB_APPLICATION)
        self.assertTrue(result['success'])
        self.assertGreater(len(result['structure_info']['functions']), 0)

    def test_cli_tool_detection(self):
        """Test detection of CLI tool projects"""
        code = """
import argparse

def main():
    parser = argparse.ArgumentParser(description='Test CLI')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

if __name__ == '__main__':
    main()
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertEqual(result['project_type'], ProjectType.CLI_TOOL)
        self.assertTrue(result['success'])

    def test_data_analysis_detection(self):
        """Test detection of data analysis projects"""
        code = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_data(df):
    return df.describe()

data = pd.DataFrame({'a': [1, 2, 3]})
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertEqual(result['project_type'], ProjectType.DATA_ANALYSIS)
        self.assertTrue(result['success'])

    def test_library_detection(self):
        """Test detection of library projects"""
        code = """
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        return [x * 2 for x in self.data]
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertEqual(result['project_type'], ProjectType.LIBRARY)
        self.assertTrue(result['success'])
        self.assertEqual(len(result['structure_info']['classes']), 2)

    def test_script_detection(self):
        """Test detection of simple script projects"""
        code = """
def calculate_sum(numbers):
    return sum(numbers)

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def main():
    data = [1, 2, 3, 4, 5]
    print(calculate_sum(data))
    print(calculate_average(data))

if __name__ == '__main__':
    main()
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertIn(result['project_type'], [ProjectType.SCRIPT, ProjectType.CLI_TOOL])
        self.assertTrue(result['success'])

    def test_syntax_error_handling(self):
        """Test handling of code with syntax errors"""
        code = """
def broken_function(:
    print('This has a syntax error'
    return None
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertFalse(result['success'])
        self.assertGreater(len(result['structure_info']['errors']), 0)
        self.assertEqual(result['structure_info']['errors'][0]['type'], 'SyntaxError')

    def test_partial_analysis_with_errors(self):
        """Test partial analysis capability when AST parsing fails"""
        code = """
import sys
import os

class MyClass:
    def method1(self):
        pass

def function1(:  # Syntax error here
    pass
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        # Should still detect some structure despite errors
        self.assertGreater(len(result['structure_info']['imports']), 0)
        self.assertFalse(result['success'])

    def test_empty_code(self):
        """Test handling of empty code"""
        code = ""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertEqual(len(result['nodes']), 1)  # Should have at least module node
        self.assertTrue(result['success'])

    def test_class_with_methods_extraction(self):
        """Test extraction of classes with their methods"""
        code = """
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name}"

    def celebrate_birthday(self):
        self.age += 1
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertEqual(len(result['structure_info']['classes']), 1)
        person_class = result['structure_info']['classes'][0]
        self.assertEqual(person_class['name'], 'Person')
        self.assertIn('__init__', person_class['methods'])
        self.assertIn('greet', person_class['methods'])
        self.assertIn('celebrate_birthday', person_class['methods'])

    def test_imports_extraction(self):
        """Test extraction of various import types"""
        code = """
import os
import sys as system
from pathlib import Path
from typing import List, Dict
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        imports = result['structure_info']['imports']
        self.assertGreater(len(imports), 0)

        # Check for specific imports
        import_names = [imp['name'] for imp in imports]
        self.assertIn('os', import_names)
        self.assertIn('sys', import_names)

    def test_decorators_detection(self):
        """Test detection of decorators on functions and classes"""
        code = """
def decorator(func):
    return func

@decorator
def my_function():
    pass

@decorator
class MyClass:
    @staticmethod
    def static_method():
        pass

    @classmethod
    def class_method(cls):
        pass
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        # Should detect decorators
        self.assertGreater(len(result['structure_info']['functions']), 0)
        self.assertGreater(len(result['structure_info']['classes']), 0)

    def test_async_function_detection(self):
        """Test detection of async functions"""
        code = """
async def fetch_data(url):
    return await some_async_call(url)

async def process_data():
    data = await fetch_data('http://example.com')
    return data
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        functions = result['structure_info']['functions']
        async_functions = [f for f in functions if f.get('is_async', False)]
        self.assertGreater(len(async_functions), 0)

    def test_visualization_data_generation(self):
        """Test that visualization data is properly generated"""
        code = """
class MyClass:
    def method(self):
        pass

def my_function():
    pass
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        # Check nodes and edges are generated
        self.assertGreater(len(result['nodes']), 0)
        self.assertGreater(len(result['edges']), 0)

        # Check levels structure
        self.assertIn('module', result['levels'])
        self.assertIn('class', result['levels'])
        self.assertIn('function', result['levels'])

    def test_get_project_info(self):
        """Test project info summary"""
        code = """
import os
import sys

class MyClass:
    def method1(self):
        pass

def function1():
    pass

def function2():
    pass
"""
        handler = UnknownProjectHandler(code)
        handler.analyze()

        info = handler.get_project_info()

        self.assertIn('project_type', info)
        self.assertEqual(info['num_classes'], 1)
        self.assertEqual(info['num_functions'], 2)
        self.assertGreater(info['num_imports'], 0)
        self.assertFalse(info['has_errors'])

    def test_analyze_unknown_project_function(self):
        """Test convenience function"""
        code = """
def test():
    pass
"""
        result = analyze_unknown_project(code, '/tmp/test.py')

        self.assertIn('project_type', result)
        self.assertIn('structure_info', result)
        self.assertIn('nodes', result)
        self.assertTrue(result['success'])

    def test_complex_inheritance(self):
        """Test detection of class inheritance"""
        code = """
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def bark(self):
        print('Woof!')

class Cat(Animal):
    def meow(self):
        print('Meow!')
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        classes = result['structure_info']['classes']
        self.assertEqual(len(classes), 3)

        # Check for base classes
        dog_class = next(c for c in classes if c['name'] == 'Dog')
        self.assertIn('Animal', dog_class['bases'])

    def test_module_level_variables(self):
        """Test detection of module-level variables"""
        code = """
CONSTANT = 42
config = {'debug': True}
data = [1, 2, 3]
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        variables = result['structure_info']['variables']
        self.assertGreater(len(variables), 0)

        var_names = [v['name'] for v in variables]
        self.assertIn('CONSTANT', var_names)

    def test_error_node_visualization(self):
        """Test that errors are included in visualization"""
        code = """
def broken(:
    pass
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        # Should have error nodes
        self.assertIn('error', result['levels'])
        self.assertGreater(len(result['structure_info']['errors']), 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    def test_only_comments(self):
        """Test code with only comments"""
        code = """
# This is a comment
# Another comment
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()
        self.assertTrue(result['success'])

    def test_multiline_strings(self):
        """Test code with multiline strings"""
        code = '''
"""
This is a docstring
"""

def func():
    """Function docstring"""
    pass
'''
        handler = UnknownProjectHandler(code)
        result = handler.analyze()
        self.assertTrue(result['success'])

    def test_very_long_code(self):
        """Test handling of large code files"""
        # Generate a large code sample
        code = "import os\n" * 100
        code += "\n".join([f"def function_{i}(): pass" for i in range(100)])

        handler = UnknownProjectHandler(code)
        result = handler.analyze()

        self.assertTrue(result['success'])
        self.assertGreater(len(result['structure_info']['functions']), 90)

    def test_unicode_in_code(self):
        """Test handling of unicode characters"""
        code = """
def greet(name):
    return f"Hello {name} 你好 👋"

class Café:
    pass
"""
        handler = UnknownProjectHandler(code)
        result = handler.analyze()
        self.assertTrue(result['success'])


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestUnknownProjectHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
