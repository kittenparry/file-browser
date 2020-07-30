import sys
import os

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide2.QtGui import QIcon, QImage, QPixmap, QFont

from icon import get_icon

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.cached_dirs = []
		# temp test already read directory
		self.cached_dirs.append({'path': 'F:\\_patreon\\browser-test', 'dirs': ['albums', 'videos'], 'files': ['4.jpg']})

		self.setWindowTitle('file-browser')
		self.setGeometry(200, 200, 640, 480)

		self.create_layout()
		vbox = QVBoxLayout()
		vbox.addWidget(self.group)
		self.setLayout(vbox)

		self.show()


	def create_layout(self):
		'''Draw a frame* with current directory on top and 2* lists inside.'''
		path = 'F:\\_patreon\\browser-test'

		# FIXME: set a max character limit for group text and crop it from left
		# otherwise it changes the size of the window
		self.group = QGroupBox(path)
		self.group.setFont(QFont('Sanserif', 14))

		hbox = QHBoxLayout()

		try:
			self.left_list = self.create_file_list(os.path.abspath(os.path.join(path, '..')), os.path.basename(path), True)
		except Exception as e:
			self.left_list = self.create_file_list('')
			print(e)
		self.left_list.setMinimumSize(200, 300)
		hbox.addWidget(self.left_list)

		try:
			self.mid_list = self.create_file_list(path)
		except Exception as e:
			print(e)
		self.mid_list.setMinimumSize(200, 300)
		hbox.addWidget(self.mid_list)

		self.left_list.itemDoubleClicked.connect(self.left_list_click)
		self.mid_list.itemDoubleClicked.connect(self.mid_list_click)

		self.group.setLayout(hbox)

	def left_list_click(self, item):
		self.item_click(item, 'left')

	def mid_list_click(self, item):
		self.item_click(item, 'mid')

	def item_click(self, item, side):
		print(item, str(item.text()))
		# TODO: probably use a better method
		if str(item.text()) == '((empty))' or str(item.text()) == '((root))':
			return
		path = self.group.title()
		if side == 'mid':
			path = os.path.join(path, str(item.text()))
		elif side == 'left':
			if item.text() == '..':
				add = ''
			else:
				add = str(item.text())
			path = os.path.abspath(os.path.join(path, '..', add))
		self.group.setTitle(path)
		self.update_file_lists(path)

	def update_file_lists(self, path):
		left_path = os.path.abspath(os.path.join(path, '..'))
		up_check = False if left_path == path else True
		try:
			if up_check:
				self.create_file_list(left_path, os.path.basename(path), up_check, self.left_list)
			else:
				self.create_file_list('', update_list = self.left_list)
		except Exception as e:
			print(e)
		self.create_file_list(path, update_list = self.mid_list)

	def create_file_list(self, path, selected = None, up = False, update_list = None):
		'''Return a file list with objects populated from files/dirs in given path.

		path -- path of directory to create list elements
		selected -- name of the cwd to select in parent list
		up -- create a link to one level up
		update_list -- update the given list with new path elements rather than returning a new list
		'''
		if not update_list:
			file_list = QListWidget(self)
		else:
			update_list.clear()
			file_list = update_list

		if not path and not update_list: # if empty
			return file_list
		elif not path and update_list:
			update_list.addItem(QListWidgetItem('((root))'))
			return # TODO: maybe some sort of indication this is root or something?

		# cache read contents of path to save some time?
		if not any(c['path'] == path for c in self.cached_dirs):
			files, dirs, dirpath = get_files(path)
			cache = {'path': dirpath, 'dirs': dirs.copy(), 'files': files.copy()}
			self.cached_dirs.append(cache)
			# dirs cache limit
			if len(self.cached_dirs) > 15:
				del self.cached_dirs[0]
			print('---')
			for c in self.cached_dirs:
				print(c['path'])
			print('---')
			print('new')
		else:
			for c in self.cached_dirs:
				if c['path'] == path:
					files, dirs, dirpath = c['files'].copy(), c['dirs'].copy(), c['path']
					print('cached')
		
		print(files, dirs, dirpath)
		if up:
			dirs.insert(0, os.path.abspath(os.path.join(path)))
			# dirs.insert(0, '..')

		selected_index = -1
		if len(files) > 0:
			for i in range(len(files)):
				try:
					icon = QIcon(convert_to_icon(os.path.join(dirpath, files[i])))
				except Exception as e:
					print(e)
					icon = QIcon()
				files[i] = QListWidgetItem(icon, files[i])
		if len(dirs) > 0:
			for i in range(len(dirs)):
				if dirs[i] == selected:
					selected_index = i
				try:
					icon = QIcon(convert_to_icon(os.path.abspath(os.path.join(dirpath, dirs[i]))))
				except Exception as e:
					print(e)
					icon = QIcon()
				dirs[i] = QListWidgetItem(icon, dirs[i])

		if up:
			dirs[0].setText('..')

		if len(dirs) > 0:
			for d in dirs:
				file_list.addItem(d)
		if len(files) > 0:
			for f in files:
				file_list.addItem(f)
		
		if len(dirs) == 0 and len(files) == 0:
			file_list.addItem(QListWidgetItem('((empty))'))
		
		if selected_index >= 0:
			file_list.item(selected_index).setSelected(True)
			file_list.scrollToItem(file_list.item(selected_index))

		if update_list:
			return
		return file_list


	# TODO: double click or right arrow action to go into that dir
	# TODO: add a left list for parent, right list for child, check if those positions exist first
	# TODO: either no child directory panel or use 4th panel for preview of text files' contents and image/video previews


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
