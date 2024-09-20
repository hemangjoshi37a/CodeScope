import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import networkx as nx

from code_parser import CodeParser
from graph_generator import GraphGenerator
from visualizer import Visualizer
from data_flow_analyzer import DataFlowAnalyzer
from code_editor import CodeEditor

class CodeVisualizationTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Advanced Python Code Visualization Tool')
        self.setGeometry(100, 100, 1600, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.visualizer = Visualizer(self)
        self.code_editor = CodeEditor(self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.visualizer)
        splitter.addWidget(self.code_editor)
        splitter.setSizes([2, 1])  # Set initial sizes (2:1 ratio)

        layout.addWidget(splitter)

    def load_project(self, directory):
        parser = CodeParser(directory)
        ast_data = parser.parse()

        graph_gen = GraphGenerator(ast_data)
        graph = graph_gen.generate_graph()

        flow_analyzer = DataFlowAnalyzer(ast_data)
        data_flow = flow_analyzer.analyze()

        self.visualizer.set_data(graph, data_flow)
        self.visualizer.update()

class Visualizer(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graph = None
        self.data_flow = None
        self.view = self.addViewBox()
        self.view.setAspectLocked(False)
        self.view.enableAutoRange()

    def set_data(self, graph, data_flow):
        self.graph = graph
        self.data_flow = data_flow

    def update(self):
        if not self.graph:
            return

        self.view.clear()
        pos = nx.spring_layout(self.graph)
        
        for node, (x, y) in pos.items():
            item = pg.EllipseROI([x, y], [0.1, 0.1], pen=pg.mkPen('r', width=2))
            self.view.addItem(item)
            
            text = pg.TextItem(node, anchor=(0.5, 0.5))
            self.view.addItem(text)
            text.setPos(x, y)

        for edge in self.graph.edges():
            line = pg.PlotDataItem(pos[edge[0]], pos[edge[1]], pen=pg.mkPen('b', width=1))
            self.view.addItem(line)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CodeVisualizationTool()
    ex.show()
    
    if len(sys.argv) > 1:
        ex.load_project(sys.argv[1])
    
    sys.exit(app.exec_())
