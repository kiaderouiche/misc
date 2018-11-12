#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Version sans SymPy (temporaire)

import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLineEdit, QSpinBox,
                             QStyleFactory, QWidget)


class Window(QWidget):
	def __init__(self, parent=None):
		super(Window, self).__init__(parent)
		self.setWindowTitle("Primer number repartition")

		#Crée le spinbox
		self.spinbox = QSpinBox(self)

		#Init la configuration du spinbox
		self.spinbox.setMinimum(5)
		self.spinbox.setMaximum(90)
		self.spinbox.setValue(55)
		self.spinbox.setStyleSheet("background-color: yellow")

		self.spinbox.valueChanged.connect(self.change)

		self.lineEdit = QLineEdit(self)
		#positionnement
		posit = QGridLayout()
		posit.addWidget(self.spinbox, 0, 1)
		posit.addWidget(self.lineEdit, 1, 0, 1, 3)
		self.setLayout(posit)

	def change(self, nb):
		"""méthode exécutée à chaque changement des radioboutons"""
		if nb % 2 == 0:
			self.lineEdit.setText(u"%d est pair" %(nb))
		if nb % 2 != 0:
			self.lineEdit.setText(u"%d est impair" %(nb))
			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	QApplication.setStyle(QStyleFactory.create('plastique'))
	win = Window()
	win.show()
	sys.exit(app.exec_())