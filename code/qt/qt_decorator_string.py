#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class MyWindow(QDialog):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle("Decorator Chaine")
		self.setGeometry(10, 10, 640, 480)

		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	_win = MyWindow()
	sys.exit(app.exec_())