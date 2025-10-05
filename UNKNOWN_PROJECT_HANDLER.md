# Unknown Project Structure Handler

## Overview

The Unknown Project Structure Handler is a powerful feature in CodeScope that enables the analysis and visualization of Python projects with non-standard or unknown structures. It provides robust error handling, project type detection, and graceful degradation when parsing fails.

## Features

### 1. Automatic Project Type Detection

The handler uses heuristic analysis to automatically detect the type of Python project:

- **Web Application**: Detects frameworks like Flask, Django, FastAPI, etc.
- **CLI Tool**: Identifies command-line tools using argparse, click, typer
- **Data Analysis**: Recognizes data science projects with pandas, numpy, matplotlib
- **Library**: Identifies reusable code libraries with classes but no main execution
- **Script**: Simple Python scripts with functions and main execution
- **Unknown**: Fallback category for unrecognized patterns

### 2. Comprehensive Code Analysis

The handler extracts detailed information from Python code:

- **Classes**: Names, inheritance, decorators, methods
- **Functions**: Top-level functions, arguments, decorators, async detection
- **Imports**: Both `import` and `from...import` statements
- **Variables**: Module-level variable assignments
- **Decorators**: Function and class decorators
- **Errors**: Syntax errors and other parsing issues

### 3. Graceful Error Handling

When code contains syntax errors or cannot be fully parsed:

- **Partial Analysis**: Attempts text-based parsing to extract basic structure
- **Error Visualization**: Displays errors as special nodes in the visualization
- **Detailed Logging**: Provides comprehensive error information for debugging
- **No Crashes**: Never crashes the application, always returns usable results

### 4. Enhanced Visualization

Supports additional node types for better visual representation:

- **Import Nodes** (Purple): Shows external dependencies
- **Error Nodes** (Bright Red): Highlights syntax errors and issues
- **Module Node** (Blue): Root node representing the file
- **Class Nodes** (Green): Class definitions
- **Function Nodes** (Red): Functions and methods
- **Variable Nodes** (Orange): Module-level variables

## Usage

### Basic Usage

```python
from unknown_project_handler import UnknownProjectHandler

# Create handler with code
code = """
import flask
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'
"""

handler = UnknownProjectHandler(code)
result = handler.analyze()

# Access results
print(f"Project Type: {result['project_type']}")
print(f"Classes: {len(result['structure_info']['classes'])}")
print(f"Functions: {len(result['structure_info']['functions'])}")
print(f"Imports: {len(result['structure_info']['imports'])}")
```

### Convenience Function

```python
from unknown_project_handler import analyze_unknown_project

# Quick analysis
result = analyze_unknown_project(code, file_path='/path/to/file.py')

# Get visualization data
nodes = result['nodes']
edges = result['edges']
levels = result['levels']
```

### Integration with CodeScope

The Unknown Project Handler is automatically integrated into CodeScope's main application:

```python
# In app.py, it's used automatically
parser = CodeParser(code)
nodes, edges, levels = parser.analyze()

# The parser now uses UnknownProjectHandler for better analysis
```

### Getting Project Information

```python
handler = UnknownProjectHandler(code)
handler.analyze()

# Get summary info
info = handler.get_project_info()
print(f"Project Type: {info['project_type']}")
print(f"Number of Classes: {info['num_classes']}")
print(f"Number of Functions: {info['num_functions']}")
print(f"Number of Imports: {info['num_imports']}")
print(f"Has Errors: {info['has_errors']}")
```

## Project Type Detection Heuristics

### Web Application
Detected when imports include:
- `flask`, `django`, `fastapi`, `bottle`, `tornado`, `aiohttp`, `starlette`
- `tkinter`, `pyqt`, `pyside`, `kivy`, `wxpython` (GUI frameworks)

### CLI Tool
Detected when imports include:
- `argparse`, `click`, `typer`
- References to `sys.argv`

### Data Analysis
Detected when imports include:
- `pandas`, `numpy`, `matplotlib`, `seaborn`, `sklearn`, `scipy`

### Library
Detected when:
- Has multiple classes
- No `main()` function
- No direct execution code

### Script
Detected when:
- Has `main()` function
- Multiple functions (3+)
- Direct execution code

## API Reference

### UnknownProjectHandler Class

#### Constructor

```python
UnknownProjectHandler(code: str, file_path: Optional[str] = None)
```

**Parameters:**
- `code`: Python source code to analyze
- `file_path`: Optional file path for additional context

#### Methods

##### analyze()

```python
def analyze(self) -> Dict
```

Performs comprehensive analysis of the code structure.

**Returns:**
Dictionary containing:
- `project_type`: Detected ProjectType enum
- `structure_info`: Detailed structure breakdown
- `nodes`: List of visualization nodes (name, type)
- `edges`: List of edges between nodes (parent, child)
- `levels`: Hierarchical organization dict
- `success`: Boolean indicating if analysis succeeded without errors

##### get_project_info()

```python
def get_project_info(self) -> Dict
```

Returns summary of project statistics.

**Returns:**
Dictionary containing:
- `project_type`: Project type as string
- `num_classes`: Number of classes found
- `num_functions`: Number of functions found
- `num_imports`: Number of imports found
- `num_errors`: Number of errors encountered
- `has_errors`: Boolean indicating errors present
- `file_path`: Original file path if provided

### ProjectType Enum

Available project types:
- `ProjectType.WEB_APPLICATION`
- `ProjectType.CLI_TOOL`
- `ProjectType.LIBRARY`
- `ProjectType.SCRIPT`
- `ProjectType.DATA_ANALYSIS`
- `ProjectType.UNKNOWN`

## Examples

### Example 1: Analyzing a Flask Application

```python
code = """
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    conn = sqlite3.connect('data.db')
    # ... query data
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(debug=True)
"""

handler = UnknownProjectHandler(code)
result = handler.analyze()

print(f"Type: {result['project_type']}")  # WEB_APPLICATION
print(f"Functions: {[f['name'] for f in result['structure_info']['functions']]}")
# Output: ['index', 'get_data']
```

### Example 2: Handling Syntax Errors

```python
code = """
def broken_function(:
    print('Missing parameter name'
    return None

class ValidClass:
    def method(self):
        pass
"""

handler = UnknownProjectHandler(code)
result = handler.analyze()

print(f"Success: {result['success']}")  # False
print(f"Errors: {len(result['structure_info']['errors'])}")  # > 0
print(f"Classes found: {len(result['structure_info']['classes'])}")  # 1 (partial analysis)

# Errors are included in visualization
error_nodes = [n for n in result['nodes'] if n[1] == 'error']
print(f"Error nodes: {error_nodes}")
```

### Example 3: Data Analysis Project

```python
code = """
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filename):
    return pd.read_csv(filename)

def plot_distribution(data, column):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column])
    plt.show()

def analyze_correlations(data):
    return data.corr()
"""

handler = UnknownProjectHandler(code, file_path='analysis.py')
result = handler.analyze()

print(f"Type: {result['project_type']}")  # DATA_ANALYSIS
print(f"Imports: {[imp['name'] for imp in result['structure_info']['imports']]}")
```

### Example 4: Using in CodeScope GUI

The handler is automatically used by CodeScope's GUI application:

```python
# User types or pastes code in the editor
# CodeScope automatically:
# 1. Creates CodeParser with the code
# 2. CodeParser uses UnknownProjectHandler
# 3. Analysis results are visualized
# 4. Project type is logged

# Check console output for:
# INFO:app:Project type detected: web_application
```

## Advanced Features

### Custom Node Colors

The visualizer supports custom colors for each node type:

```python
# In app.py
color_map = {
    'module': (100, 100, 255, 255),      # Blue
    'class': (100, 255, 100, 255),       # Green
    'function': (255, 100, 100, 255),    # Red
    'variable': (255, 200, 0, 255),      # Orange
    'import': (200, 100, 255, 255),      # Purple
    'error': (255, 50, 50, 255)          # Bright Red
}
```

### Filtering by Level

Results include hierarchical levels for easy filtering:

```python
result = handler.analyze()

# Get only classes
class_nodes = result['levels']['class']

# Get only functions
function_nodes = result['levels']['function']

# Get imports
import_nodes = result['levels']['import']

# Get errors
error_nodes = result['levels']['error']
```

### Async Function Detection

The handler properly detects async functions:

```python
code = """
async def fetch_data(url):
    response = await http_client.get(url)
    return response.json()

async def process_multiple(urls):
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
"""

handler = UnknownProjectHandler(code)
result = handler.analyze()

# Check for async functions
for func in result['structure_info']['functions']:
    if func['is_async']:
        print(f"Async function: {func['name']}")
```

## Testing

Comprehensive unit tests are provided in `test_unknown_project_handler.py`:

```bash
# Run all tests
python test_unknown_project_handler.py

# Tests cover:
# - Project type detection (web, CLI, data analysis, library, script)
# - Syntax error handling
# - Partial analysis with errors
# - Class and method extraction
# - Import detection
# - Decorator detection
# - Async function detection
# - Visualization data generation
# - Edge cases (empty code, unicode, large files)
```

## Performance Considerations

### Large Files

For very large files (>1000 lines), the handler:
- Uses efficient AST traversal
- Limits import visualization to first 10 imports
- Provides fast partial analysis fallback

### Memory Usage

The handler is memory-efficient:
- Stores minimal structure information
- Generates visualization data on-demand
- Cleans up temporary data after analysis

### Speed

Typical analysis times:
- Small files (<100 lines): <10ms
- Medium files (100-1000 lines): 10-50ms
- Large files (>1000 lines): 50-200ms

## Troubleshooting

### Issue: No nodes appear in visualization

**Solution**: Check that your code contains recognizable structures (classes, functions, imports).

```python
# This will show only a module node
code = ""

# This will show multiple nodes
code = "def test(): pass"
```

### Issue: Project type is always UNKNOWN

**Solution**: Add recognizable imports or follow standard patterns:

```python
# Add imports for detection
import flask  # Detected as WEB_APPLICATION

# Or add main function for scripts
def main():
    pass
```

### Issue: Syntax errors prevent visualization

**Solution**: The handler automatically performs partial analysis. Check the error nodes:

```python
result = handler.analyze()
errors = result['structure_info']['errors']
for error in errors:
    print(f"{error['type']}: {error['message']}")
```

## Best Practices

1. **Always check result['success']** to know if full parsing succeeded
2. **Review errors** in result['structure_info']['errors'] for debugging
3. **Use file_path parameter** for better context in multi-file projects
4. **Check project_type** to understand what kind of code you're analyzing
5. **Limit visualization** to relevant levels for large projects

## Future Enhancements

Planned features:
- [ ] Multi-file project analysis
- [ ] Call graph generation
- [ ] Import dependency visualization
- [ ] Code complexity metrics
- [ ] Support for more project types (testing frameworks, API clients, etc.)
- [ ] Custom heuristic rules configuration
- [ ] Export analysis results to JSON

## Contributing

To extend the project type detection:

1. Add new keywords to detection heuristics in `_detect_project_type()`
2. Create new ProjectType enum values
3. Add corresponding tests
4. Update documentation

Example:

```python
# In unknown_project_handler.py
class ProjectType(Enum):
    # ... existing types ...
    TESTING = "testing"  # New type

# In _detect_project_type method
testing_keywords = ['pytest', 'unittest', 'nose', 'tox']
if any(keyword in imports_str for keyword in testing_keywords):
    self.project_type = ProjectType.TESTING
    return
```

## License

This feature is part of CodeScope and is released under the MIT License.

## Support

For issues, questions, or contributions, please visit the main CodeScope repository.
