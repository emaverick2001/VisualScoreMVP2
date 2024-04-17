import sys
import multiprocessing
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout
from neoscore.common import *
from neoscore.core.neoscore import render_pdf  # Import the render_pdf function

def run_neoscore():
    neoscore.setup()
    Text(ORIGIN, None, "Hello, neoscore!")
    neoscore.show()
    print("Neoscore window opened")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisualScore")
        self.setGeometry(100, 100, 400, 200)
        self.button_open_neoscore = QPushButton("Open Neoscore Window")
        self.button_open_neoscore.clicked.connect(self.open_neoscore_window)

        layout = QVBoxLayout()
        layout.addWidget(self.button_open_neoscore)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_neoscore_window(self):
        neoscore_process = multiprocessing.Process(target=run_neoscore)
        neoscore_process.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
