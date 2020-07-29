import sys
import os
from PySide2.QtWidgets import QApplication, QLabel, QListWidget, QListWidgetItem
from PySide2.QtGui import QIcon
from icon import get_icon

def main():
	app = QApplication(sys.argv)

	file_list = QListWidget()
	files, dirs, dirpath = get_files()
	print(dirs)
	print(files)
	print(dirpath)

	# get_icon("C:\Program Files (x86)", 'large').save('test2.png')
	if len(files) > 0:
		for f in files:
			f = QListWidgetItem(f)
			# f.setIcon(get_icon('C:\Program Files (x86)', 'large'))
	if len(dirs) > 0:
		for i in range(len(dirs)):
			dirs[i] = QListWidgetItem(QIcon('test2.png'), dirs[i])
		# for d in dirs:
		# 	d = QListWidgetItem(QIcon('test2.png'), d)
		# 	d = 'tddd'
			# test = QIcon('C:\\test2.png')
			# d.setIcon(test)

	print(dirs)

	if len(files) > 0:
		file_list.insertItems(0, files)
	if len(dirs) > 0:
		# file_list.insertItems(0, dirs)
		for d in dirs:
			file_list.addItem(d)
	
	# TODO: double click or right arrow action to go into that dir

	file_list.show()

	app.exec_()

def get_files():
	f = []
	d = []
	dp = ''
	for (dirpath, dirnames, filenames) in os.walk('F:/_patreon/browser-test'):
		f.extend(filenames)
		d.extend(dirnames)
		dp = dirpath
		break
	return f, d, dp


if __name__ == '__main__':
	main()
