from neoscore.core import neoscore
from neoscore.core.path import Path
from neoscore.core.point import ORIGIN
from neoscore.core.units import Mm

from PySide6.QtWidgets import QApplication, QMainWindow, QTextBrowser
import sys    

def main():
    # Create the Qt Application
    app = QApplication(sys.argv)
    
    # Create the main window
    window = QMainWindow()
    window.setWindowTitle("Neoscore Blank Page Renderer")
    
    # Create a QTextBrowser widget to display the rendered content
    text_browser = QTextBrowser()
    window.setCentralWidget(text_browser)
    
    # Render the blank Neoscore page content
    # Initialize Neoscore
    neoscore.setup(text_browser)

    # Display the blank page
    neoscore.show()
    
    # Show the main window
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
