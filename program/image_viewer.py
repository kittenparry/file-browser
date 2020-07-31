import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea
from PySide2.QtGui import QIcon, QImage, QPixmap, QFont

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle('image-viewer')
		self.setGeometry(200, 200, 800, 600)
		self.image_path = 'F:\\_patreon\\browser-test\\4.jpg'

		self.create_layout()
		self.show()


	def create_layout(self):
		self.image = QLabel()
		self.content = QPixmap(self.image_path)
		# FIXME: reset on resize
		self.image.setPixmap(self.content)

		self.label = QLabel()
		self.label.setText('image name probably')

		self.image_scroll = QScrollArea()
		self.image_scroll.setWidget(self.image)

		vbox = QVBoxLayout()

		vbox.addWidget(self.image_scroll)
		vbox.addWidget(self.label)

		# remove padding & margin
		vbox.setSpacing(0)
		vbox.setContentsMargins(0, 0, 0, 0)
		self.setLayout(vbox)
