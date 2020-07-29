import sys
import os

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide2.QtGui import QIcon, QImage, QPixmap, QFont

from icon import get_icon

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle('file-browser')
		self.setGeometry(200, 200, 640, 480)

		self.create_layout()
		vbox = QVBoxLayout()
		vbox.addWidget(self.group)
		self.setLayout(vbox)
		# self.group.setTitle('test')

		self.show()


	def create_layout(self):
		'''Draw a frame* with current directory on top and 2* lists inside.'''
		path = 'F:\\_patreon\\browser-test'

		self.group = QGroupBox(path)
		self.group.setFont(QFont('Sanserif', 14))

		hbox = QHBoxLayout()

		try:
			left_list = self.create_file_list(os.path.abspath(os.path.join(path, '..')), os.path.basename(path))
		except Exception as e:
			left_list = self.create_file_list('')
			print(e)
		left_list.setMinimumSize(100, 100)
		hbox.addWidget(left_list)

		try:
			mid_list = self.create_file_list(path)
		except Exception as e:
			print(e)
		mid_list.setMinimumSize(100, 100)
		hbox.addWidget(mid_list)

		self.group.setLayout(hbox)

	def create_file_list(self, path, selected = None):
		'''Return a file list with objects populated from files/dirs in given path.

		path -- path of directory to create list elements
		selected -- name of the cwd to select in parent list
		'''
		file_list = QListWidget(self)
		if not path: # if empty
			return file_list

		files, dirs, dirpath = get_files(path)

		dir_icons = []
		file_icons = []

		selected_index = -1
		if len(files) > 0:
			for i in range(len(files)):
				files[i] = QListWidgetItem(QIcon(convert_to_icon(os.path.join(dirpath, files[i]))), files[i])
		if len(dirs) > 0:
			for i in range(len(dirs)):
				if dirs[i] == selected:
					selected_index = i
				dirs[i] = QListWidgetItem(QIcon(convert_to_icon(os.path.join(dirpath, dirs[i]))), dirs[i])

		if len(dirs) > 0:
			for d in dirs:
				file_list.addItem(d)
		if len(files) > 0:
			for f in files:
				file_list.addItem(f)
		
		if selected_index >= 0:
			file_list.item(selected_index).setSelected(True)

		return file_list


	# TODO: double click or right arrow action to go into that dir
	# TODO: add a left list for parent, right list for child, check if those positions exist first

	# TODO: keep a cache of contents of 5-10 directories in path: content dictionary arrays and check in maybe get_files() to see if they exist before reading again.
	# is this a good structure for one array element? {'path+dir': [dirs], 'path+files': [files], 'path+dp': 'dirpath'}

def convert_to_icon(path):
	'''Convert Image to QPixmap, which could be used in QIcon().
	
	path -- file/dir path to get the icon image of
	'''
	im = get_icon(path, 'large')
	im = im.convert('RGBA')
	data = im.tobytes('raw', 'RGBA')
	qim = QImage(data, 32, 32, QImage.Format_RGBA8888)
	return QPixmap.fromImage(qim)

def get_files(path):
	'''Return a list of filenames, dirnames and path information to those.
	
	path -- path to the directory of files/directories that gets returned
	'''
	f = []
	d = []
	dp = ''
	for (dirpath, dirnames, filenames) in os.walk(path):
		f.extend(filenames)
		d.extend(dirnames)
		dp = dirpath # FIXME: this is useless because path arg is already dirpath?
		break
	return f, d, dp


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	app.exec_()
	sys.exit()
