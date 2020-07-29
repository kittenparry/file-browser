import sys
from PySide2.QtWidgets import QApplication, QLabel

def main():
	app = QApplication(sys.argv)
	label = QLabel('<font color="blue" size="50">Test Label</font>')
	label.show()
	app.exec_()

if __name__ == '__main__':
	main()
