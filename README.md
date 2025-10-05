# CodeScope: Python Code Visualization Tool

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Transform complex Python codebases into intuitive, interactive visual representations for faster comprehension and more efficient development.

## 🚀 Key Features

- **Dynamic Graph Visualization**: Powered by PyQt6 and pyqtgraph for smooth, responsive displays
- **Intelligent Code Parsing**: Utilizes Abstract Syntax Tree (AST) for accurate code analysis
- **Unknown Project Structure Handler**: Automatically detects and visualizes projects of any type (NEW!)
- **Project Type Detection**: Identifies web apps, CLI tools, data analysis, libraries, and scripts
- **Robust Error Handling**: Gracefully handles syntax errors with partial analysis fallback
- **Multi-level Visualization**: Navigate between module, class, function, import, and error views
- **Interactive Code Editing**: Real-time code modifications with instant visual updates
- **Enhanced Node Types**: Import nodes (purple) and error nodes (bright red) for better insights
- **Zoom and Pan Capabilities**: Explore large, complex codebases with ease
- **Search Functionality**: Quickly locate specific code elements (search bar included)
- **Asynchronous Parsing**: Non-blocking code analysis using Qt threading

## 🛠️ Installation

```bash
git clone https://github.com/hemangjoshi37a/CodeScope.git
cd CodeScope
pip install -r requirements.txt
```

### Dependencies

- Python 3.7+
- PyQt6
- pyqtgraph
- networkx
- ast (built-in)

### Install Dependencies Manually

If `requirements.txt` is not available, install dependencies manually:

```bash
pip install PyQt6 pyqtgraph networkx
```

## 🖥️ Getting Started

### Quick Start

1. Launch the application:
   ```bash
   python main.py
   ```

2. The application opens with a sample code snippet demonstrating:
   - Function definitions
   - Class definitions with methods
   - Variable assignments and usage

3. Start exploring the visualization immediately or paste your own Python code in the editor.

### Advanced Usage

Launch with a specific file:
```bash
python main.py --file your_script.py
```

Enable debug logging:
```bash
python main.py --debug
```

View all options:
```bash
python main.py --help
```

**Note:** You can also run `python app.py` directly for backward compatibility.

## 📊 Usage

### Basic Navigation

- **Zoom**: Use the mouse wheel or trackpad gestures on the visualization
- **Pan**: Right-click and drag on the visualization area (rect mode enabled)
- **View Limits**: Visualization is bounded to prevent excessive panning
- **Auto-Range**: Automatic adjustment to fit all nodes in view

### Visual Elements

- **Node Colors**:
  - **Blue** (100, 100, 255): Modules
  - **Green** (100, 255, 100): Classes
  - **Red** (255, 100, 100): Functions
  - **Yellow-Orange** (255, 200, 0): Variables
  - **Purple** (200, 100, 255): Imports (NEW!)
  - **Bright Red** (255, 50, 50): Errors (NEW!)

- **Node Connections**:
  - Lines show relationships between classes, functions, and their containing scopes
  - Import nodes connect to the module to show dependencies
  - Error nodes highlight problematic code sections

### Real-time Editing

1. Type or paste Python code in the right-side editor
2. Visualization updates automatically on each text change
3. Parse errors are displayed in the red error label below the editor
4. Detailed logs appear in the log viewer at the bottom

### Level Filtering

1. Enter a level type in the level selector: `module`, `class`, `function`, `import`, or `error`
2. Press Enter to filter the visualization to show only nodes of that type
3. Clear the field and press Enter to show all nodes again

### Project Type Detection

CodeScope automatically detects your project type and logs it:
- **Web Application**: Flask, Django, FastAPI, etc.
- **CLI Tool**: argparse, click, typer
- **Data Analysis**: pandas, numpy, matplotlib
- **Library**: Reusable code with classes
- **Script**: Simple scripts with main execution

Check the console output for: `INFO:app:Project type detected: <type>`

### Search Feature

- Search bar is available (implementation placeholder in app.py:356)
- Future enhancement will allow searching and highlighting specific nodes

## 🧰 Technologies Used

- **Python 3.7+**: Core language
- **PyQt6**: Modern Qt bindings for GUI framework
- **pyqtgraph**: High-performance graphics and GUI library for scientific applications
- **networkx**: Graph algorithms and network analysis
- **ast**: Python's built-in Abstract Syntax Tree module

## 🔍 Features in Detail

### Abstract Syntax Tree (AST) Parsing

CodeScope uses Python's `ast` module to parse code into an Abstract Syntax Tree, enabling detailed structural analysis:

- **Module detection**: Top-level code organization
- **Class definitions** (ast.ClassDef): Class structures and inheritance
- **Function definitions** (ast.FunctionDef): Methods and standalone functions
- **Variable assignments** (ast.Name): Variable references and usage
- **Syntax error handling**: Graceful failure with error messages

The parser is implemented in `CodeParser` class (app.py:36-90) and runs asynchronously to prevent UI blocking.

### Asynchronous Code Analysis

- **CodeParserWorker** (app.py:18-34): Qt QObject worker running in separate thread
- **Signals**: `finished`, `error`, and `log` signals for communication with UI
- **Thread Management**: Proper cleanup on application close (app.py:363-369)

### Graph Visualization

- **Spring Layout Algorithm**: Uses networkx spring_layout for natural node positioning
- **Configurable Parameters**: k=2 (optimal spring distance), iterations=50 (layout convergence)
- **Position Scaling**: Coordinates multiplied by 1000 for better visibility
- **Custom GraphItem**: CodeNode class (app.py:92-146) extends pyqtgraph.GraphItem

### Interactive UI Components

- **Code Editor** (QTextEdit): Multi-line text editor with syntax support
- **Visualizer** (CodeVisualizer): Custom pyqtgraph widget
- **Error Label** (QLabel): Red-styled error display
- **Log Viewer** (QPlainTextEdit): Read-only scrolling log output
- **Search Bar** (QLineEdit): Node search input (ready for implementation)
- **Level Selector** (QLineEdit): Filter by node type
- **Splitter Layout**: Resizable 2:1 ratio between visualizer and controls

## 🛠️ Troubleshooting

- **Visualization not updating**: Check the log viewer for parsing errors
- **Syntax errors**: Ensure your Python code is syntactically correct
- **Performance issues with large files**:
  - Consider limiting the code to specific modules or functions
  - The spring layout algorithm may take time with 100+ nodes
- **Blank visualization**: Verify that your code contains classes, functions, or assignments
- **Thread warnings on close**: Normal cleanup messages; threads are properly terminated

## 🗺️ Roadmap

### Phase 1: Enhanced Visualization Framework ✅ (Partially Complete)
- [x] Node-based visualization system
- [x] Custom rendering with pyqtgraph
- [x] Zoomable interface with pan support
- [ ] Google Maps-like multi-level detail system

### Phase 2: Advanced Code Analysis (In Progress)
- [x] Basic AST parsing for classes, functions, variables
- [ ] Enhanced data flow analysis tracking variable propagation
- [ ] Call graph analysis for function dependencies
- [ ] Import and module dependency visualization

### Phase 3: Interactive Node Manipulation
- [x] Visual node representation with colors
- [x] Automatic connection generation
- [ ] Drag-and-drop node rearrangement
- [ ] Manual edge creation and editing
- [ ] Node grouping and clustering

### Phase 4: Multi-Level Detail Visualization
- [x] Basic level filtering (module/class/function)
- [ ] Smooth zoom-based detail transitions
- [ ] Hierarchical code summarization
- [ ] Collapsible node groups

### Phase 5: Real-Time Code Editing ✅
- [x] Integrated code editor
- [x] Instant visual updates on code change
- [x] Error handling and display
- [ ] Bidirectional editing (click node to edit definition)

### Phase 6: Search and Navigation
- [ ] Implement search functionality (placeholder exists)
- [ ] Node highlighting on search
- [ ] Jump to definition in code editor
- [ ] Breadcrumb navigation

### Phase 7: Advanced Features
- [ ] Export visualizations as images
- [ ] Save/load custom layouts
- [ ] Multiple file support
- [ ] Project-wide visualization

### Phase 8: Collaboration Features (Future)
- [ ] Multi-user support
- [ ] Comments and annotations
- [ ] Change tracking visualization

### Phase 9: AI-Assisted Analysis (Future)
- [ ] Code improvement suggestions
- [ ] Automated refactoring recommendations
- [ ] Pattern recognition

### Phase 10: Version Control Integration (Future)
- [ ] Git integration
- [ ] Visual diff tools
- [ ] Change history animation

## 🤝 Contributing

We welcome contributions to CodeScope! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions and classes
- Test with various Python code samples
- Check the log output for errors
- Update README for significant changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support the Project

If you find CodeScope useful, please consider:
- Starring the repository ⭐
- Sharing it with your network 📢
- Contributing to its development 💻
- Reporting bugs and suggesting features 🐛

## 📫 Contact the Developer

[<img height="36" src="https://cdn.simpleicons.org/similarweb"/>](https://hjlabs.in/) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/WhatsApp"/>](https://wa.me/917016525813) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/telegram"/>](https://t.me/hjlabs) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/Gmail"/>](mailto:hemangjoshi37a@gmail.com) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/LinkedIn"/>](https://www.linkedin.com/in/hemang-joshi-046746aa) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/facebook"/>](https://www.facebook.com/hemangjoshi37) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/Twitter"/>](https://twitter.com/HemangJ81509525) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/tumblr"/>](https://www.tumblr.com/blog/hemangjoshi37a-blog) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/StackOverflow"/>](https://stackoverflow.com/users/8090050/hemang-joshi) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/Instagram"/>](https://www.instagram.com/hemangjoshi37) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/Pinterest"/>](https://in.pinterest.com/hemangjoshi37a) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/Blogger"/>](http://hemangjoshi.blogspot.com) &nbsp;
[<img height="36" src="https://cdn.simpleicons.org/gitlab"/>](https://gitlab.com/hemangjoshi37a) &nbsp;

## ❓ Frequently Asked Questions

**Q: Can CodeScope handle very large Python projects?**
A: CodeScope works best with individual files or modules. For large projects, visualize key modules separately. Performance depends on node count and complexity.

**Q: Why does the visualization look cluttered?**
A: Try using the level selector to filter by `class` or `function`. The spring layout algorithm works best with 10-50 nodes.

**Q: Can I export the visualization?**
A: Export functionality is planned for future releases. Currently, you can take screenshots of the visualization window.

**Q: Does CodeScope modify my code?**
A: No, CodeScope only reads and analyzes your code. Changes in the editor don't save to disk automatically.

**Q: What Python syntax is supported?**
A: CodeScope supports standard Python syntax parsed by the `ast` module (Python 3.7+). Even code with syntax errors is analyzed using the Unknown Project Handler for partial visualization.

**Q: What happens if my code has syntax errors?**
A: CodeScope gracefully handles syntax errors! The Unknown Project Handler performs partial analysis and displays error nodes (bright red) in the visualization to highlight issues.

**Q: Can I use CodeScope with other languages?**
A: Currently, CodeScope is Python-only. The AST parser is Python-specific, but the visualization framework could be adapted for other languages.

**Q: How do I report bugs?**
A: Open an issue on GitHub with:
  - Steps to reproduce
  - Error messages from the log viewer
  - Sample code causing the issue (if possible)

## 💡 Use Cases

CodeScope is perfect for:

- **Code Reviews**: Quickly understand structure and relationships
- **Refactoring**: Identify tightly coupled components
- **Learning**: Visualize how classes and functions interact
- **Documentation**: Generate visual code maps
- **Debugging**: Trace function calls and data flow
- **Onboarding**: Help new developers understand codebase structure

## 🔬 Technical Details

### Code Structure

```
CodeScope/
├── main.py                         # Main entry point (NEW!)
├── app.py                           # Core application file
├── unknown_project_handler.py      # Unknown project structure handler
├── test_main.py                    # Test suite for main entry point (NEW!)
├── test_unknown_project_handler.py # Test suite for project handler
├── demo_main.py                    # Demo script for main.py usage (NEW!)
├── demo_unknown_project.py         # Demo for unknown project handler
├── CodeScope.ipynb                 # Jupyter notebook experiments
├── minimal_example.py              # Simplified example
├── requirements.txt                # Project dependencies
├── UNKNOWN_PROJECT_HANDLER.md      # Feature documentation
├── LICENSE                         # MIT License
└── README.md                       # This file
```

### Key Classes

- **CodeVisualizationTool** (app.py:258-369): Main QMainWindow application
- **CodeVisualizer** (app.py:150-256): Custom pyqtgraph widget for graph rendering
- **CodeParser** (app.py:37-110): Enhanced AST-based code analyzer with unknown project support
- **CodeParserWorker** (app.py:18-34): Threaded parser wrapper
- **CodeNode** (app.py:92-146): Custom GraphItem for node rendering
- **UnknownProjectHandler** (unknown_project_handler.py): Handles unknown project structures (NEW!)
- **ProjectType** (unknown_project_handler.py): Enum for project type classification (NEW!)

### Logging

CodeScope uses Python's logging module with DEBUG level:
- Logger output appears in console and the in-app log viewer
- Useful for debugging visualization issues and parser errors

---

<p align="center">
  Made with ❤️ by <a href="https://hjlabs.in/">HJLabs</a>
</p>
