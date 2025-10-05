import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg

class MinimalVisualizer(pg.GraphicsLayoutWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = self.addViewBox()
        self.view.setAspectLocked(False)
        self.view.enableAutoRange()

class MinimalTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Minimal Example')
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.visualizer = MinimalVisualizer(self)
        layout.addWidget(self.visualizer)

def main():
    app = QApplication(sys.argv)
    ex = MinimalTool()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
