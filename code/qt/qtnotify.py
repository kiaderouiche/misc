#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = "K.I.A.Derouiche"
__author_email__ = "kamel.derouiche@gmail.com"

#inspired by https://stackoverflow.com/questions/46389496/pyqt5-notification-from-qwidget

import datetime
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QGridLayout, QLabel,
                             QLineEdit, QMessageBox, QPushButton, QVBoxLayout,
                             QWidget)


class Message(QWidget):
    def __init__(self, title, message, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QGridLayout())
        self.titleLabel = QLabel(title, self)
        self.titleLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 14px; font-weight: bold; padding: 0;")
        self.messageLabel = QLabel(message, self)
        self.messageLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 12px; font-weight: normal; padding: 0;")
        self.buttonClose = QPushButton(self)
        self.buttonClose.setIcon(QIcon("res/close1.png"))
        self.buttonClose.setFixedSize(14, 14)
        self.layout().addWidget(self.titleLabel, 0, 0)
        self.layout().addWidget(self.messageLabel, 1, 0)
        self.layout().addWidget(self.buttonClose, 0, 1, 2, 1)

class Notification(QWidget):
    signNotifyClose = pyqtSignal(str)
    def __init__(self, parent = None):
        time = datetime.datetime.now()
        currentTime = str(time.hour) + ":" + str(time.minute) + "_"
        self.LOG_TAG = currentTime + self.__class__.__name__ + ": "
        super(QWidget, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        resolution = QDesktopWidget().screenGeometry(-1)
        screenWidth = resolution.width()
        screenHeight = resolution.height()
        print(self.LOG_TAG + "width: " + str(resolution.width()) + " height: " + str(resolution.height()))
        self.nMessages = 0
        self.mainLayout = QVBoxLayout(self)
        self.move(screenWidth, 0)

    def setNotify(self, title, message):
        m = Message(title, message, self)
        self.mainLayout.addWidget(m)
        m.buttonClose.clicked.connect(self.onClicked)
        self.nMessages += 1
        self.show()

    def onClicked(self):
        self.mainLayout.removeWidget(self.sender().parent())
        self.sender().parent().deleteLater()
        self.nMessages -= 1
        self.adjustSize()
        if self.nMessages == 0:
            self.close()

    def delete(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i)
            widget = item.widget()
            if widget is not None:
                pass # widget.deleteLater()
            elif item.layout() is not None:
                print("")
                self.delete(item.layout())

class PkgExample(QWidget):
    counter = 0

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout())
        self.btn = QPushButton("Send Notify", self)
        self.layout().addWidget(self.btn)
        self.qline = QLineEdit(self)
        self.layout().addWidget(self.qline)
        self.qbtn = QPushButton("Quit", self)
        self.layout().addWidget(self.qbtn)

        self.notification = Notification()
        self.btn.clicked.connect(self.notify)
        self.qbtn.clicked.connect(self.closeEvent)
    
    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit? Any unsaved work will be lost.",
            QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            app.quit()
        else:
            pass

    def notify(self):
        self.counter += 1
        textValue = self.qline.text()
        
        if textValue == '':
            QMessageBox.warning(self, "Message", "Please writing text.")
        else:
            self.notification.setNotify("Title: {}".format(self.counter),
                                    "{}{}".format(textValue, self.counter))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PkgExample()
    w.show()
    sys.exit(app.exec_())
