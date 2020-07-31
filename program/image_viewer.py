import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel
from PySide2.QtGui import QIcon, QImage, QPixmap, QFont

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle('image-viewer')
		self.setGeometry(200, 200, 800, 600)

		self.show()
