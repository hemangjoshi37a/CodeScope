
import sys
import traceback
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QTextEdit, QLabel, QLineEdit, QPlainTextEdit
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QColor
import pyqtgraph as pg
import networkx as nx
import ast
from unknown_project_handler import UnknownProjectHandler, ProjectType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)




class CodeParserWorker(QObject):
    finished = pyqtSignal(object, object, object)
    error = pyqtSignal(str)
    log = pyqtSignal(str)

    def __init__(self, code):
        super().__init__()
        self.code = code

    def run(self):
        try:
            parser = CodeParser(self.code)
            nodes, edges, levels = parser.analyze()
            self.finished.emit(nodes, edges, levels)
        except Exception as e:
            self.error.emit(str(e))
            self.log.emit(traceback.format_exc())

class CodeParser:
    def __init__(self, code):
        self.code = code
        self.tree = None
        self.use_unknown_handler = True  # Enable unknown project handling



    def analyze(self):
        """
        Analyze code using both standard parser and unknown project handler.
        Falls back to UnknownProjectHandler for better error handling and analysis.
        """
        try:
            # First attempt: Use UnknownProjectHandler for comprehensive analysis
            if self.use_unknown_handler:
                handler = UnknownProjectHandler(self.code)
                result = handler.analyze()

                if result['success'] or result['nodes']:
                    # Return the enhanced analysis results
                    logger.info(f"Project type detected: {result['project_type'].value}")
                    return result['nodes'], result['edges'], result['levels']

            # Fallback: Use original simple parser
            self.tree = ast.parse(self.code)
            nodes = []
            edges = []
            levels = {'module': [], 'class': [], 'function': []}

            for node in ast.walk(self.tree):
                node_info = self.process_node(node)
                if node_info:
                    nodes.append(node_info)
                    if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                        parent = self.find_parent(node)
                        if parent:
                            edges.append((parent, node_info[0]))

            return nodes, edges, levels
        except SyntaxError as e:
            logger.error(f"Syntax error in code: {e}")
            # Use UnknownProjectHandler for partial analysis even with errors
            if self.use_unknown_handler:
                handler = UnknownProjectHandler(self.code)
                result = handler.analyze()
                return result['nodes'], result['edges'], result['levels']
            return [("SyntaxError", str(e))], [], {'module': [], 'class': [], 'function': []}

    def process_node(self, node):
        try:
            if isinstance(node, ast.Module):
                return (node.__class__.__name__, 'module')
            elif isinstance(node, ast.ClassDef):
                return (node.name, 'class')
            elif isinstance(node, ast.FunctionDef):
                return (node.name, 'function')
            elif isinstance(node, ast.Name):
                return (node.id, 'variable')
            # Add more node types as needed
            else:
                return None
        except Exception as e:
            logger.error(f"Error processing node {type(node)}: {e}")
            return None


    def find_parent(self, node):
        for potential_parent in ast.walk(self.tree):
            for child in ast.iter_child_nodes(potential_parent):
                if child == node:
                    if isinstance(potential_parent, ast.ClassDef):
                        return potential_parent.name
                    elif isinstance(potential_parent, ast.Module):
                        return potential_parent.__class__.__name__
        return None

class CodeNode(pg.GraphItem):
    def __init__(self):
        self.scatter = pg.ScatterPlotItem()
        self.textItems = []
        self.node_data = [[], [], []]  # Initialize node_data before calling super().__init__()
        super().__init__()
        self.setData([], [], [])

    def setData(self, pos=None, text=None, color=None, **kwds):
        logger.debug(f"Setting data for CodeNode: pos={pos}, text={text}, color={color}")
        self.node_data = [
            pos if pos is not None else self.node_data[0],
            text if text is not None else self.node_data[1],
            color if color is not None else self.node_data[2]
        ]
        self.updateGraph()

    def updateGraph(self):
        logger.debug("Updating CodeNode graph")
        pos, text, color = self.node_data
        try:
            if len(pos) > 0:
                self.scatter.setData(pos=pos, size=20, brush=color, hoverable=True, hoverSymbol='s', hoverSize=30)

                # Update existing text items and create new ones if needed
                for i, (p, t) in enumerate(zip(pos, text)):
                    if i < len(self.textItems):
                        self.textItems[i].setPos(p[0], p[1])
                        self.textItems[i].setText(t)
                        self.textItems[i].show()
                    else:
                        item = pg.TextItem(t)
                        self.textItems.append(item)
                        item.setParentItem(self)
                        item.setPos(p[0], p[1])

                # Hide excess text items
                for item in self.textItems[len(pos):]:
                    item.hide()

                logger.debug(f"Updated graph with {len(pos)} nodes")
            else:
                logger.warning("No data to display in CodeNode")
                self.scatter.clear()
                for item in self.textItems:
                    item.hide()
        except Exception as e:
            logger.error(f"Error updating CodeNode graph: {e}")
            logger.error(traceback.format_exc())

    def paint(self, p, *args):
        self.scatter.paint(p, *args)

    def boundingRect(self):
        return self.scatter.boundingRect()



class CodeVisualizer(pg.GraphicsLayoutWidget):
    error = pyqtSignal(str)
    status = pyqtSignal(str)


    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = self.addViewBox()
        self.view.setAspectLocked(False)
        self.view.enableAutoRange()
        self.graph = nx.Graph()
        self.node_item = CodeNode()
        self.view.addItem(self.node_item)

        self.view.setMouseMode(self.view.RectMode)
        self.view.enableAutoRange(False)
        self.view.setLimits(xMin=-1000, xMax=1000, yMin=-1000, yMax=1000)

    def update_graph(self, nodes, edges, levels):
        logger.debug(f"Updating graph with {len(nodes)} nodes and {len(edges)} edges")
        try:
            self.graph.clear()
            for node, node_type in nodes:
                self.graph.add_node(node, type=node_type)
            self.graph.add_edges_from(edges)
            self.levels = levels
            self.update_layout()
        except Exception as e:
            logger.error(f"Error updating graph: {e}")
            logger.error(traceback.format_exc())
            self.error.emit(f"Error updating graph: {str(e)}")


    def update_layout(self):
        logger.debug("Updating layout")
        self.status.emit("Updating layout")
        if len(self.graph.nodes) == 0:
            logger.warning("No nodes to display")
            self.node_item.setData([], [], [])
            return

        try:
            pos = nx.spring_layout(self.graph, k=2, iterations=50)
            node_pos = []
            node_colors = []
            node_labels = []
            for node, coords in pos.items():
                node_pos.append(coords * 1000)  # Scale up the positions
                node_type = self.graph.nodes[node]['type']
                color = self.get_node_color(node_type)
                node_colors.append(color)
                node_labels.append(node)
            logger.debug(f"Setting data for {len(node_pos)} nodes")
            self.node_item.setData(pos=node_pos, text=node_labels, color=node_colors)
            self.view.autoRange()  # Ensure all nodes are visible
            self.status.emit(f"Visualization updated with {len(node_pos)} nodes")
        except Exception as e:
            logger.error(f"Error in update_layout: {e}")
            logger.error(traceback.format_exc())
            self.error.emit(f"Error updating layout: {str(e)}")


    def get_node_color(self, node_type):
        """Get color for each node type"""
        color_map = {
            'module': (100, 100, 255, 255),      # Blue
            'class': (100, 255, 100, 255),       # Green
            'function': (255, 100, 100, 255),    # Red
            'variable': (255, 200, 0, 255),      # Orange
            'import': (200, 100, 255, 255),      # Purple
            'error': (255, 50, 50, 255)          # Bright Red
        }
        return color_map.get(node_type, (200, 200, 200, 255))


    def set_level(self, level):
        logger.debug(f"Setting visualization level to: {level}")
        if level in self.levels and self.levels[level]:
            nodes_to_show = self.levels[level]
            subgraph = self.graph.subgraph(nodes_to_show)
            self.update_layout_for_subgraph(subgraph)
        else:
            logger.warning(f"Invalid or empty level: {level}")
            self.error.emit(f"Invalid or empty level: {level}")

    def update_layout_for_subgraph(self, subgraph):
        logger.debug(f"Updating layout for subgraph with {len(subgraph.nodes)} nodes")
        if len(subgraph.nodes) == 0:
            logger.warning("Subgraph is empty")
            self.node_item.setData([], [], [])
            return

        try:
            pos = nx.spring_layout(subgraph, k=2, iterations=50)
            node_pos = []
            node_colors = []
            node_labels = []
            for node, coords in pos.items():
                node_pos.append(coords * 1000)
                node_type = subgraph.nodes[node]['type']
                color = self.get_node_color(node_type)
                node_colors.append(color)
                node_labels.append(node)
            self.node_item.setData(pos=node_pos, text=node_labels, color=node_colors)
            self.view.autoRange()  # Ensure all nodes are visible
            self.status.emit(f"Subgraph visualization updated with {len(node_pos)} nodes")
        except Exception as e:
            logger.error(f"Error in update_layout_for_subgraph: {e}")
            logger.error(traceback.format_exc())
            self.error.emit(f"Error updating subgraph layout: {str(e)}")

class CodeVisualizationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CodeScope: Advanced Python Code Visualization Tool')
        self.setGeometry(100, 100, 1600, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)


        self.visualizer = CodeVisualizer(self)
        self.visualizer.error.connect(self.show_error)
        self.code_editor = QTextEdit(self)
        self.code_editor.textChanged.connect(self.on_code_changed)

        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("color: red;")

        self.log_viewer = QPlainTextEdit(self)
        self.log_viewer.setReadOnly(True)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for nodes...")
        self.search_bar.textChanged.connect(self.search_nodes)

        self.level_selector = QLineEdit(self)
        self.level_selector.setPlaceholderText("Enter level (module/class/function)")
        self.level_selector.returnPressed.connect(self.change_level)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.addWidget(self.search_bar)
        right_layout.addWidget(self.level_selector)
        right_layout.addWidget(self.code_editor)
        right_layout.addWidget(self.error_label)
        right_layout.addWidget(self.log_viewer)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.visualizer)
        splitter.addWidget(right_widget)
        splitter.setSizes([2, 1])

        layout.addWidget(splitter)

        self.parser_thread = QThread()
        self.parser_worker = None

    def load_code(self, code):
        self.code_editor.setText(code)
        self.update_visualization(code)

    def update_visualization(self, code):
        if self.parser_thread.isRunning():
            self.parser_thread.quit()
            self.parser_thread.wait()

        self.parser_worker = CodeParserWorker(code)
        self.parser_worker.moveToThread(self.parser_thread)
        self.parser_thread.started.connect(self.parser_worker.run)
        self.parser_worker.finished.connect(self.on_parsing_finished)
        self.parser_worker.error.connect(self.show_error)
        self.parser_worker.log.connect(self.show_log)
        self.parser_worker.finished.connect(self.parser_thread.quit)
        self.parser_worker.finished.connect(self.parser_worker.deleteLater)
        self.parser_thread.finished.connect(self.parser_thread.deleteLater)
        self.parser_thread.start()

    @pyqtSlot(object, object, object)
    def on_parsing_finished(self, nodes, edges, levels):
        try:
            logger.debug("Parsing finished, updating visualization")
            self.visualizer.update_graph(nodes, edges, levels)
            self.error_label.setText("")
        except Exception as e:
            logger.error(f"Error updating visualization: {e}")
            logger.error(traceback.format_exc())
            self.show_error(f"Error updating visualization: {str(e)}")


    @pyqtSlot(str)
    def show_error(self, error_message):
        self.error_label.setText(error_message)
        logger.error(error_message)

    @pyqtSlot(str)
    def show_log(self, log_message):
        self.log_viewer.appendPlainText(log_message)
        logger.debug(log_message)

    def on_code_changed(self):
        code = self.code_editor.toPlainText()
        self.update_visualization(code)

    def search_nodes(self, query):
        # TODO: Implement node search functionality
        pass

    def change_level(self):
        level = self.level_selector.text().lower()
        self.visualizer.set_level(level)

    def closeEvent(self, event):
        logger.debug("Closing application")
        if hasattr(self, 'parser_thread') and self.parser_thread.isRunning():
            logger.debug("Stopping parser thread")
            self.parser_thread.quit()
            self.parser_thread.wait()
        super().closeEvent(event)

def main():
    app = QApplication(sys.argv)
    ex = CodeVisualizationTool()
    ex.show()

    sample_code = """
def greet(name):
    print(f"Hello, {name}!")

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        greet(self.name)
        print(f"I am {self.age} years old.")

person = Person("Alice", 30)
person.introduce()
"""
    ex.load_code(sample_code)

    sys.exit(app.exec())

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        logger.critical(traceback.format_exc())







































