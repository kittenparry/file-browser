import sys
import os
import mimetypes
import re
import string
import platform
import traceback

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide2.QtGui import QIcon, QImage, QPixmap, QFont
from PySide2 import QtCore

from icon import get_icon

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.cached_dirs = []
		self.path = 'F:\\_patreon\\browser-test'
		if platform.system() == 'Windows':
			self.drives = ['%s:\\' % d for d in string.ascii_uppercase if os.path.exists('%s:\\' % d)]
		else:
			self.drives = []

		self.setWindowTitle('file-browser')
		self.setGeometry(200, 200, 800, 600)

		self.create_layout()
		vbox = QVBoxLayout()
		vbox.addWidget(self.group)
		self.setLayout(vbox)
		self.mid_list.setFocus()

		self.show()


	def create_layout(self):
		'''Draw a frame* with current directory on top and 2* lists inside.'''
		self.group = QGroupBox(self.cut_string(self.path))
		self.group.setFont(QFont('Sanserif', 14))

		hbox = QHBoxLayout()

		try:
			self.left_list = self.create_file_list(os.path.abspath(os.path.join(self.path, '..')), os.path.basename(self.path), True)
		except Exception as e:
			self.left_list = self.create_file_list('')
			print(e)
			traceback.print_tb(e.__traceback__)
		self.left_list.setMinimumSize(self.width() / 3, 300)
		hbox.addWidget(self.left_list)

		try:
			self.mid_list = self.create_file_list(self.path)
		except Exception as e:
			print(e)
			traceback.print_tb(e.__traceback__)
		self.mid_list.setMinimumSize(self.width() / 3, 300)
		hbox.addWidget(self.mid_list)

		# FIXME: label's place gets filled by others when in a different window size
		self.right_panel = QLabel()
		self.right_panel.setMinimumSize(self.width() / 3, 300)
		picture = QPixmap('F:\\_patreon\\browser-test\\4.jpg')
		# FIXME: reset on resize
		picture = picture.scaled(int(self.width() / 3), int(self.height() / 3), QtCore.Qt.KeepAspectRatio)
		self.right_panel.setPixmap(picture)
		hbox.addWidget(self.right_panel)


		self.left_list.itemDoubleClicked.connect(self.item_click)
		self.mid_list.itemDoubleClicked.connect(self.item_click)

		self.group.setLayout(hbox)

	def keyPressEvent(self, event):
		if event.key() == QtCore.Qt.Key_Left:
			print('left key')
			# FIXME: requires double left click for whatever reason
			self.item_click(self.left_list.item(0))
		elif event.key() == QtCore.Qt.Key_Right or event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			print('right key or enter')
		return super().keyPressEvent(event)

	def item_click(self, item):
		'''Navigate to a new directory when clicked on a list.
		
		item -- clicked QListWidgetItem
		'''
		print(item, str(item.text()), str(mimetypes.guess_type(item.text())))
		print(mimetypes.guess_type(item.text())[0])
		# TODO: probably use a better method
		if str(item.text()) == '((empty))' or str(item.text()) == '((root))':
			return
		
		# TODO: possibly display preview on one click and open the image in preferred image software on double.
		# TODO: maybe only proceed to a directory if mimetype guess is None? though suppose it could also display None for no extension files
		# and inversely may read directories with extension-like names as those type
		guess = mimetypes.guess_type(item.text())[0]
		if guess: # if not None, e.g. directory
			if 'image' in mimetypes.guess_type(item.text())[0]:
				if item.listWidget() == self.mid_list:
					path = self.path
				elif item.listWidget() == self.left_list:
					# TODO: likely navigate one level above if it's on the left list
					path = os.path.abspath(os.path.join(self.path, '..'))
				picture = QPixmap(os.path.join(path, str(item.text())))
				picture = picture.scaledToWidth(int(self.width() / 3))
				self.right_panel.setPixmap(picture)
				return

		self.right_panel.setPixmap(QPixmap())

		path = self.path
		if item.listWidget() == self.mid_list:
			path = os.path.join(path, str(item.text()))
		elif item.listWidget() == self.left_list:
			if item.text() == '..':
				add = ''
			else:
				add = str(item.text())
			path = os.path.abspath(os.path.join(path, '..', add))
		self.path = path
		self.group.setTitle(self.cut_string(path))
		self.update_file_lists(path)

	def update_file_lists(self, path):
		'''Re-populate file lists with given new path.
		
		path -- new path to get items of the lists
		'''
		left_path = os.path.abspath(os.path.join(path, '..'))
		up_check = False if left_path == path else True
		try:
			if up_check:
				self.create_file_list(left_path, os.path.basename(path), up_check, self.left_list)
			else:
				self.create_file_list('', update_list = self.left_list)
		except Exception as e:
			print(e)
			traceback.print_tb(e.__traceback__)
		self.create_file_list(path, update_list = self.mid_list)

	def create_file_list(self, path, selected = None, up = False, update_list = None):
		'''Return a file list with objects populated from files/dirs in given path.

		path -- path of directory to create list elements
		selected -- name of the cwd to select in parent list
		up -- create a link to one level up
		update_list -- (QListWidget) update the given list with new path elements rather than returning a new list
		'''
		if not update_list:
			file_list = QListWidget(self)
		else:
			update_list.clear()
			file_list = update_list

		if not path and not update_list: # if empty
			return file_list
		elif not path and update_list:
			if len(self.drives) > 0:
				for letter in self.drives:
					try:
						icon = QIcon(convert_to_icon(letter))
					except Exception as e:
						print(e)
						traceback.print_tb(e.__traceback__)
					update_list.addItem(QListWidgetItem(icon, letter))
			else:
				update_list.addItem(QListWidgetItem('((root))'))
			return

		# cache read contents of path to save some time and processing power?
		# TODO: could maybe also save actual QListWIdgetItems? to save on Icon creation time
		# could also copy QIcons to cached_dirs = {... 'dir_icons': [], 'file_icons': []}
		if not any(c['path'] == path for c in self.cached_dirs):
			files, dirs, dirpath = get_files(path)
			cache = {'path': dirpath, 'dirs': dirs.copy(), 'files': files.copy()}
			self.cached_dirs.append(cache)
			# dirs cache limit
			if len(self.cached_dirs) > 15:
				del self.cached_dirs[0]
		else:
			for c in self.cached_dirs:
				if c['path'] == path:
					files, dirs, dirpath = c['files'].copy(), c['dirs'].copy(), c['path']

		if up:
			dirs.insert(0, os.path.abspath(os.path.join(path)))

		selected_index = -1
		if len(files) > 0:
			for i in range(len(files)):
				try:
					icon = QIcon(convert_to_icon(os.path.join(dirpath, files[i])))
				except Exception as e:
					print(e)
					traceback.print_tb(e.__traceback__)
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
					traceback.print_tb(e.__traceback__)
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
		else:
			file_list.item(0).setSelected(True)

		if update_list:
			return
		return file_list

	def cut_string(self, s):
		'''Cut frame* title string so it fits the window.
		
		s -- path string that gets cut and added leading ellipsis'''
		limit = int(self.width() / 10)
		if len(s) > limit:
			s = '...' + s[len(s) - limit:]
		return s


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
	f = sorted(f, key = natural_sort_key)
	d = sorted(d, key = natural_sort_key)
	return f, d, dp

# src: https://stackoverflow.com/a/16090640/4085881
def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
	return [int(text) if text.isdigit() else text.lower() for text in _nsre.split(s)]


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	app.exec_()
	sys.exit()
