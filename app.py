import sys
import ast
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QTextEdit
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QColor
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from difflib import SequenceMatcher
import threading

class CodeNode(pg.GraphicsObject):
    def __init__(self, name, node_type, content=""):
        super().__init__()
        self.name = name
        self.node_type = node_type
        self.content = content
        self.connections = []
        self.rect = QRectF(0, 0, 150, 100)
        self.picture = QtGui.QPicture()
        self._generate_picture()

    def _generate_picture(self):
        painter = QPainter(self.picture)
        painter.setPen(pg.mkPen(color=(50, 50, 50)))
        painter.setBrush(pg.mkBrush(color=(200, 200, 255)))
        painter.drawRect(self.rect)
        painter.setPen(pg.mkPen(color=(0, 0, 0)))
        painter.drawText(self.rect, Qt.AlignCenter, f"{self.node_type}\n{self.name}")
        painter.end()

    def paint(self, painter, option, widget=None):
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return self.rect

    def add_connection(self, other_node):
        self.connections.append(other_node)

class CodeVisualizer(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = self.addViewBox()
        self.view.setAspectLocked(False)
        self.view.enableAutoRange()
        self.nodes = {}
        self.edges = []

    def add_node(self, name, node_type, content=""):
        node = CodeNode(name, node_type, content)
        self.nodes[name] = node
        self.view.addItem(node)
        return node

    def add_edge(self, source, target):
        edge = pg.GraphItem()
        self.view.addItem(edge)
        self.edges.append((source, target, edge))

    def update_layout(self):
        pos = nx.spring_layout(nx.Graph([(s.name, t.name) for s, t, _ in self.edges]))
        for name, node in self.nodes.items():
            x, y = pos[name]
            node.setPos(x * 1000, y * 1000)

        for source, target, edge in self.edges:
            edge.setData(pos={
                'x': [pos[source.name][0], pos[target.name][0]],
                'y': [pos[source.name][1], pos[target.name][1]]
            }, adj=np.array([[0, 1]]), pen=pg.mkPen('r', width=2))

class CodeParser:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)

    def analyze(self):
        nodes = []
        edges = []
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                nodes.append((node.name, type(node).__name__, ast.get_source_segment(self.code, node)))
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.Name):
                        edges.append((node.name, child.id))
        return nodes, edges

class DataFlowAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)

    def analyze(self):
        flow = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        flow.append((ast.get_source_segment(self.code, node.value), target.id))
        return flow

class AIAssistant:
    def suggest_improvements(self, code):
        # This is a placeholder for more advanced AI-based code analysis
        suggestions = []
        if len(code.splitlines()) > 20:
            suggestions.append("Consider breaking this code into smaller functions for better readability.")
        if 'global' in code:
            suggestions.append("Try to avoid using global variables to improve code maintainability.")
        return suggestions

class CollaborationServer:
    def __init__(self):
        self.clients = []
        self.code = ""

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)

    def update_code(self, new_code, sender):
        self.code = new_code
        for client in self.clients:
            if client != sender:
                client.receive_update(new_code)

class CodeVisualizationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.code_parser = None
        self.data_flow_analyzer = None
        self.ai_assistant = AIAssistant()
        self.collaboration_server = CollaborationServer()
        self.collaboration_server.add_client(self)

    def initUI(self):
        self.setWindowTitle('Advanced Python Code Visualization Tool')
        self.setGeometry(100, 100, 1600, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.visualizer = CodeVisualizer(self)
        self.code_editor = QTextEdit(self)
        self.code_editor.textChanged.connect(self.on_code_changed)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.visualizer)
        splitter.addWidget(self.code_editor)
        splitter.setSizes([2, 1])  # Set initial sizes (2:1 ratio)

        layout.addWidget(splitter)

    def load_code(self, code):
        self.code_editor.setText(code)
        self.code_parser = CodeParser(code)
        self.data_flow_analyzer = DataFlowAnalyzer(code)
        self.update_visualization()

    def update_visualization(self):
        self.visualizer.view.clear()
        self.visualizer.nodes.clear()
        self.visualizer.edges.clear()

        nodes, edges = self.code_parser.analyze()
        data_flow = self.data_flow_analyzer.analyze()

        for name, node_type, content in nodes:
            self.visualizer.add_node(name, node_type, content)

        for source, target in edges:
            if source in self.visualizer.nodes and target in self.visualizer.nodes:
                self.visualizer.add_edge(self.visualizer.nodes[source], self.visualizer.nodes[target])

        for source, target in data_flow:
            if source in self.visualizer.nodes and target in self.visualizer.nodes:
                self.visualizer.add_edge(self.visualizer.nodes[source], self.visualizer.nodes[target])

        self.visualizer.update_layout()

    def on_code_changed(self):
        code = self.code_editor.toPlainText()
        self.collaboration_server.update_code(code, self)
        self.load_code(code)
        suggestions = self.ai_assistant.suggest_improvements(code)
        if suggestions:
            print("AI Suggestions:")
            for suggestion in suggestions:
                print(f"- {suggestion}")

    def receive_update(self, new_code):
        if new_code != self.code_editor.toPlainText():
            cursor = self.code_editor.textCursor()
            self.code_editor.setText(new_code)
            self.code_editor.setTextCursor(cursor)

def main():
    app = QApplication(sys.argv)
    ex = CodeVisualizationTool()
    ex.show()

    # Load sample code
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

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
