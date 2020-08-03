import sys

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea
from PySide2.QtGui import QIcon, QImage, QPixmap, QFont
from PySide2 import QtCore

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle('image-viewer')
		self.setGeometry(200, 200, 800, 600)
		self.image_path = 'F:\\browser-test\\test-dir\\4.jpg'
		self.cont_zoomed = None

		self.create_layout()
		self.show()

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_BracketLeft:
			self.zoom('in')
			event.accept()
		elif event.key() == QtCore.Qt.Key_BracketRight:
			self.zoom('out')
			event.accept()
		elif event.key() == QtCore.Qt.Key_Q:
			self.close()
		return super().keyPressEvent(event)

	def zoom(self, dire):
		if self.cont_zoomed:
			ratio = self.cont_zoomed
		else:
			ratio = self.content
		if dire == 'in':
			self.cont_zoomed = self.content.scaled(ratio.width() * 0.75, ratio.height() * 0.75, QtCore.Qt.KeepAspectRatio)
		elif dire == 'out':
			self.cont_zoomed = self.content.scaled(ratio.width() * 1.25, ratio.height() * 1.25, QtCore.Qt.KeepAspectRatio)
		self.image.setPixmap(self.cont_zoomed)

	def create_layout(self):
		self.image = QLabel()
		self.content = QPixmap(self.image_path)
		# FIXME: reset on resize
		self.image.setPixmap(self.content)

		self.label = QLabel()
		self.label.setText('image name probably')

		self.image_scroll = QScrollArea()
		self.image_scroll.setWidget(self.image)
		self.image_scroll.setAlignment(QtCore.Qt.AlignCenter)

		vbox = QVBoxLayout()

		vbox.addWidget(self.image_scroll)
		vbox.addWidget(self.label)

		# remove padding & margin
		vbox.setSpacing(0)
		vbox.setContentsMargins(0, 0, 0, 0)
		self.setLayout(vbox)

	def set_image(self, img):
		'''Change displayed image with the input from the main window.
		
		img -- path to image file
		'''
		self.image_path = img
		self.content = QPixmap(self.image_path)
		self.image.setPixmap(self.content)

		self.label.setText(self.image_path)

	def resizeEvent(self, event):
		# increase image width in scroll area to fit into it
		self.image.setFixedWidth(self.width() - self.image_scroll.verticalScrollBar().width() - 2)
		return super().resizeEvent(event)
