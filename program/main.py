import sys
import os
import mimetypes

from PySide2.QtWidgets import QApplication, QLabel, QListWidget, QListWidgetItem
from PySide2.QtGui import QIcon, QImage, QPixmap
from PIL import ImageQt

from icon import get_icon

def main():
	app = QApplication(sys.argv)

	file_list = QListWidget()
	files, dirs, dirpath = get_files()
	print(dirs)
	print(files)
	print(dirpath)

	# if not os.path.isdir('temp'):
	# 	os.makedirs('temp')
	# TODO: possibly name icon files after mimetypes stripping /
	# and assign icons accordingly
	# icon_paths = []
	# test_mimetype = []

	# if len(files) > 0:
	# 	temp_files = []
	# 	for i in range(len(files)):
	# 		temp_files.append(os.path.join(dirpath, files[i]))
	# 	# for f in temp_files:
	# 	# 	get_icon = (f, 'large')
	# 		# test_mimetype.append(mimetypes.guess_type(f))
	
	# print(test_mimetype)

	# if len(dirs) > 0:
	# 	for i in range(len(dirs)):
	# 		temp_dirs[i] = os.path.join(dirpath, dirs[i])

	dir_icons = []
	file_icons = []

	if len(files) > 0:
		for i in range(len(files)):
			files[i] = QListWidgetItem(QIcon(convert_to_icon(os.path.join(dirpath, files[i]))), files[i])
	if len(dirs) > 0:
		for i in range(len(dirs)):
			dirs[i] = QListWidgetItem(QIcon(convert_to_icon(os.path.join(dirpath, dirs[i]))), dirs[i])

	print(dirs)

	if len(dirs) > 0:
		for d in dirs:
			file_list.addItem(d)
	if len(files) > 0:
		for f in files:
			file_list.addItem(f)
	
	# TODO: double click or right arrow action to go into that dir
	# TODO: add a left list for parent, right list for child, check if those positions exist first

	file_list.show()

	app.exec_()

def convert_to_icon(path):
	'''Convert Image to QPixmap, which could be used in QIcon()
	
	path -- file/dir path to get the icon image of
	'''
	im = get_icon(path, 'large')
	im = im.convert('RGBA')
	data = im.tobytes('raw', 'RGBA')
	qim = QImage(data, 32, 32, QImage.Format_RGBA8888)
	return QPixmap.fromImage(qim)

def get_files():
	f = []
	d = []
	dp = ''
	for (dirpath, dirnames, filenames) in os.walk('F:\\_patreon\\browser-test'):
		f.extend(filenames)
		d.extend(dirnames)
		dp = dirpath
		break
	return f, d, dp


if __name__ == '__main__':
	main()
