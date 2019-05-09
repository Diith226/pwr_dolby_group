# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\AXDition\Documents\Qt\QtDesignerProjects\GUI_Test2\GUI_Test3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import _thread
import random
import winsound

import librosa
import librosa.display
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import scipy.signal
import numpy


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1141, 507)

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(40, 10, 531, 80))
        self.groupBox.setObjectName("groupBox")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 509, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.loadFile)

        self.horizontalLayout.addWidget(self.toolButton)

        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.playConvButt = QtWidgets.QPushButton(Form)
        self.playConvButt.setGeometry(QtCore.QRect(810, 440, 101, 41))
        self.playConvButt.setObjectName("playConvButt")

        self.convButton = QtWidgets.QPushButton(Form)
        self.convButton.setGeometry(QtCore.QRect(600, 30, 201, 51))
        self.convButton.setObjectName("convButton")
        self.convButton.clicked.connect(self.plot)

        self.playOrgButt = QtWidgets.QPushButton(Form)
        self.playOrgButt.setGeometry(QtCore.QRect(240, 440, 101, 41))
        self.playOrgButt.setObjectName("playOrgButt")
        self.playOrgButt.clicked.connect(self.playOrgNewThread)

        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 100, 531, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.canvas_Org = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.canvas_Org.setContentsMargins(0, 0, 0, 0)
        self.canvas_Org.setObjectName("canvas_Org")

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas_Org.addWidget(self.canvas)
        self.figure.set_facecolor("black")
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_facecolor("black")

        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure2.set_facecolor("black")
        self.ax2 = self.figure2.add_subplot(111)
        self.ax2.clear()
        self.ax2.grid(False)
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_facecolor("black")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(590, 100, 531, 331))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        self.canvas_Conv = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.canvas_Conv.setContentsMargins(0, 0, 0, 0)
        self.canvas_Conv.setObjectName("verticalLayout_3")

        self.canvas_Conv.addWidget(self.canvas2)

        self.convButton_2 = QtWidgets.QPushButton(Form)
        self.convButton_2.setGeometry(QtCore.QRect(860, 30, 201, 51))
        self.convButton_2.setObjectName("convButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "File path"))
        self.toolButton.setText(_translate("Form", "..."))
        self.playConvButt.setText(_translate("Form", "Play Converted"))
        self.convButton.setText(_translate("Form", "Start Dreaming"))
        self.playOrgButt.setText(_translate("Form", "Play Original"))
        self.convButton_2.setText(_translate("Form", "Save Your Dream"))

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        #self.ax2 = self.figure2.add_subplot(111)

        # discards the old graph
        self.ax2.clear()
        self.ax2.grid(False)
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])

        # plot data
        self.ax2.plot(data, '*-')

        # refresh canvas
        self.canvas2.draw()

    def loadFile(self):
        filename, _ = QFileDialog.getOpenFileName(filter="All Files (*);;Wave files (*.wav)",
                                                  initialFilter="Wave files (*.wav)")
        self.lineEdit.setText(filename)
        self.x, self.sr = librosa.load(filename)
        xDecim = scipy.signal.decimate(self.x, 35)
        t = []
        for x in range(len(xDecim)-1):
            t.append(x)
        print(t)
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_facecolor("black")
        try:
            self.ax.hist(xDecim, t)
        except:
            print(sys.exc_info())
        #self.ax.hist(xDecim, bins=1000)
        self.canvas.draw()

    def playOrgNewThread(self):
        try:
            _thread.start_new_thread(self.playOrg, ())
        except:
            print("Error: unable to start thread")

    def playOrg(self):
        winsound.PlaySound(self.lineEdit.text(), winsound.SND_FILENAME)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
