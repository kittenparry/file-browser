import sys
import os
from PySide2.QtWidgets import QApplication, QLabel, QListWidget, QListWidgetItem
from PySide2 import QtGui

def main():
	app = QApplication(sys.argv)

	file_list = QListWidget()
	# files = ['test1', 'test2', 'test3']
	files, dirs = get_files()
	print(dirs)
	print(files)
	

	# QListWidgetItem('test1', file_list)
	if len(files) > 0:
		file_list.insertItems(0, files)
	if len(dirs) > 0:
		file_list.insertItems(0, dirs)
	
	# TODO: double click or right arrow action to go into that dir

	file_list.show()

	app.exec_()

def get_files():
	f = []
	d = []
	for (dirpath, dirnames, filenames) in os.walk('F:/_patreon/browser-test'):
		f.extend(filenames)
		d.extend(dirnames)
		break
	return f, d


if __name__ == '__main__':
	main()
