"""
Unknown Project Structure Handler

This module provides functionality to analyze and handle Python projects
with unknown or non-standard structures. It uses heuristics to detect
project types and creates appropriate visualizations.
"""

import ast
import os
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ProjectType(Enum):
    """Enumeration of detected project types"""
    WEB_APPLICATION = "web_application"
    CLI_TOOL = "cli_tool"
    LIBRARY = "library"
    SCRIPT = "script"
    DATA_ANALYSIS = "data_analysis"
    UNKNOWN = "unknown"


class UnknownProjectHandler:
    """
    Handles analysis of Python code with unknown or non-standard structures.

    This class analyzes code to:
    - Detect project type using heuristics
    - Extract structure information even from malformed code
    - Provide fallback visualization data
    """

    def __init__(self, code: str, file_path: Optional[str] = None):
        """
        Initialize the handler with code to analyze.

        Args:
            code: Python source code to analyze
            file_path: Optional file path for additional context
        """
        self.code = code
        self.file_path = file_path
        self.tree = None
        self.project_type = ProjectType.UNKNOWN
        self.imports = []
        self.structure_info = {
            'classes': [],
            'functions': [],
            'variables': [],
            'imports': [],
            'decorators': [],
            'errors': []
        }

    def analyze(self) -> Dict:
        """
        Perform comprehensive analysis of the code structure.

        Returns:
            Dictionary containing analysis results including:
            - project_type: Detected ProjectType
            - structure_info: Detailed structure breakdown
            - nodes: Visualization nodes
            - edges: Visualization edges
            - levels: Hierarchical organization
        """
        try:
            # Try to parse the code
            self.tree = ast.parse(self.code)
            self._extract_structure()
            self._detect_project_type()

        except SyntaxError as e:
            # Handle syntax errors gracefully
            logger.warning(f"Syntax error in code: {e}")
            self.structure_info['errors'].append({
                'type': 'SyntaxError',
                'message': str(e),
                'line': e.lineno if hasattr(e, 'lineno') else None
            })
            # Try to do partial analysis
            self._partial_analysis()

        except Exception as e:
            logger.error(f"Unexpected error during analysis: {e}")
            self.structure_info['errors'].append({
                'type': type(e).__name__,
                'message': str(e)
            })

        # Generate visualization data
        nodes, edges, levels = self._generate_visualization_data()

        return {
            'project_type': self.project_type,
            'structure_info': self.structure_info,
            'nodes': nodes,
            'edges': edges,
            'levels': levels,
            'success': len(self.structure_info['errors']) == 0
        }

    def _extract_structure(self):
        """Extract detailed structure information from the AST"""
        if not self.tree:
            return

        for node in ast.walk(self.tree):
            try:
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.structure_info['imports'].append({
                            'name': alias.name,
                            'asname': alias.asname,
                            'type': 'import'
                        })

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        self.structure_info['imports'].append({
                            'name': f"{module}.{alias.name}",
                            'asname': alias.asname,
                            'type': 'from_import'
                        })

                elif isinstance(node, ast.ClassDef):
                    self.structure_info['classes'].append({
                        'name': node.name,
                        'bases': [self._get_name(base) for base in node.bases],
                        'decorators': [self._get_name(dec) for dec in node.decorator_list],
                        'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        'lineno': node.lineno
                    })

                elif isinstance(node, ast.FunctionDef):
                    # Check if it's a top-level function (not a method)
                    parent = self._find_parent_class(node)
                    if not parent:
                        self.structure_info['functions'].append({
                            'name': node.name,
                            'args': [arg.arg for arg in node.args.args],
                            'decorators': [self._get_name(dec) for dec in node.decorator_list],
                            'lineno': node.lineno,
                            'is_async': isinstance(node, ast.AsyncFunctionDef)
                        })

                elif isinstance(node, ast.Assign):
                    # Track module-level variables
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            self.structure_info['variables'].append({
                                'name': target.id,
                                'lineno': node.lineno
                            })

            except Exception as e:
                logger.warning(f"Error extracting node {type(node).__name__}: {e}")

    def _detect_project_type(self):
        """
        Use heuristics to detect the project type based on imports and structure.
        """
        imports_str = ' '.join([imp['name'].lower() for imp in self.structure_info['imports']])

        # Web framework detection
        web_keywords = ['flask', 'django', 'fastapi', 'bottle', 'tornado', 'aiohttp', 'starlette']
        if any(keyword in imports_str for keyword in web_keywords):
            self.project_type = ProjectType.WEB_APPLICATION
            return

        # CLI tool detection
        cli_keywords = ['argparse', 'click', 'typer', 'sys.argv']
        if any(keyword in imports_str for keyword in cli_keywords):
            self.project_type = ProjectType.CLI_TOOL
            return

        # Data analysis detection
        data_keywords = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'sklearn', 'scipy']
        if any(keyword in imports_str for keyword in data_keywords):
            self.project_type = ProjectType.DATA_ANALYSIS
            return

        # GUI detection
        gui_keywords = ['tkinter', 'pyqt', 'pyside', 'kivy', 'wxpython']
        if any(keyword in imports_str for keyword in gui_keywords):
            self.project_type = ProjectType.WEB_APPLICATION  # Treat GUI as application
            return

        # Library detection (has classes but no main execution)
        has_main = any(func['name'] == 'main' for func in self.structure_info['functions'])
        has_classes = len(self.structure_info['classes']) > 0

        if has_classes and not has_main:
            self.project_type = ProjectType.LIBRARY
        elif has_main or len(self.structure_info['functions']) > 3:
            self.project_type = ProjectType.SCRIPT
        else:
            self.project_type = ProjectType.UNKNOWN

    def _partial_analysis(self):
        """
        Attempt partial analysis when full AST parsing fails.
        Uses regex and simple text parsing to extract basic structure.
        """
        lines = self.code.split('\n')

        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Detect imports
            if line.startswith('import ') or line.startswith('from '):
                parts = line.split()
                if len(parts) >= 2:
                    self.structure_info['imports'].append({
                        'name': parts[1],
                        'asname': None,
                        'type': 'import',
                        'lineno': i
                    })

            # Detect class definitions
            elif line.startswith('class '):
                class_name = line.split('(')[0].replace('class ', '').strip(':')
                self.structure_info['classes'].append({
                    'name': class_name,
                    'bases': [],
                    'decorators': [],
                    'methods': [],
                    'lineno': i
                })

            # Detect function definitions
            elif line.startswith('def ') or line.startswith('async def '):
                func_name = line.split('(')[0].replace('def ', '').replace('async ', '').strip()
                self.structure_info['functions'].append({
                    'name': func_name,
                    'args': [],
                    'decorators': [],
                    'lineno': i,
                    'is_async': 'async' in line
                })

    def _generate_visualization_data(self) -> Tuple[List, List, Dict]:
        """
        Generate nodes, edges, and levels for visualization.

        Returns:
            Tuple of (nodes, edges, levels) for graph visualization
        """
        nodes = []
        edges = []
        levels = {'module': [], 'class': [], 'function': [], 'import': [], 'error': []}

        # Add module node
        module_name = os.path.basename(self.file_path) if self.file_path else 'Module'
        nodes.append((module_name, 'module'))
        levels['module'].append(module_name)

        # Add import nodes
        for imp in self.structure_info['imports'][:10]:  # Limit to first 10 imports
            import_name = imp['name'].split('.')[0]
            nodes.append((import_name, 'import'))
            levels['import'].append(import_name)
            edges.append((module_name, import_name))

        # Add class nodes
        for cls in self.structure_info['classes']:
            class_name = cls['name']
            nodes.append((class_name, 'class'))
            levels['class'].append(class_name)
            edges.append((module_name, class_name))

            # Add methods as function nodes
            for method in cls['methods']:
                method_full = f"{class_name}.{method}"
                nodes.append((method_full, 'function'))
                levels['function'].append(method_full)
                edges.append((class_name, method_full))

        # Add top-level function nodes
        for func in self.structure_info['functions']:
            func_name = func['name']
            nodes.append((func_name, 'function'))
            levels['function'].append(func_name)
            edges.append((module_name, func_name))

        # Add error nodes if present
        for idx, error in enumerate(self.structure_info['errors']):
            error_name = f"Error_{idx}: {error['type']}"
            nodes.append((error_name, 'error'))
            levels['error'].append(error_name)
            edges.append((module_name, error_name))

        return nodes, edges, levels

    def _get_name(self, node) -> str:
        """Extract name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return str(node)

    def _find_parent_class(self, func_node) -> Optional[str]:
        """Find if a function is a method of a class"""
        if not self.tree:
            return None

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                if func_node in ast.walk(node):
                    return node.name
        return None

    def get_project_info(self) -> Dict:
        """
        Get a summary of the project information.

        Returns:
            Dictionary with project statistics and metadata
        """
        return {
            'project_type': self.project_type.value,
            'num_classes': len(self.structure_info['classes']),
            'num_functions': len(self.structure_info['functions']),
            'num_imports': len(self.structure_info['imports']),
            'num_errors': len(self.structure_info['errors']),
            'has_errors': len(self.structure_info['errors']) > 0,
            'file_path': self.file_path
        }


def analyze_unknown_project(code: str, file_path: Optional[str] = None) -> Dict:
    """
    Convenience function to analyze unknown project structure.

    Args:
        code: Python source code to analyze
        file_path: Optional file path for context

    Returns:
        Dictionary containing analysis results

    Example:
        >>> code = "class MyClass:\\n    pass"
        >>> result = analyze_unknown_project(code)
        >>> print(result['project_type'])
        ProjectType.LIBRARY
    """
    handler = UnknownProjectHandler(code, file_path)
    return handler.analyze()
