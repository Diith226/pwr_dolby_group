# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\AXDition\Documents\Qt\QtDesignerProjects\GUI_Test2\GUI_Test2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("DeepDreamSound")
        Form.resize(1020, 450)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(70, 25, 530, 80))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 509, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.myCanvas_Conv = QtWidgets.QWidget(Form)
        self.myCanvas_Conv.setGeometry(QtCore.QRect(510, 140, 441, 231))
        self.myCanvas_Conv.setObjectName("myCanvas_Conv")
        self.playConvButt = QtWidgets.QPushButton(Form)
        self.playConvButt.setGeometry(QtCore.QRect(690, 390, 101, 41))
        self.playConvButt.setObjectName("playConvButt")
        self.convButton = QtWidgets.QPushButton(Form)
        self.convButton.setGeometry(QtCore.QRect(640, 40, 120, 51))
        self.convButton.setObjectName("convButton")
        self.saveButton = QtWidgets.QPushButton(Form)
        self.saveButton.setGeometry(QtCore.QRect(800, 40, 120, 51))
        self.saveButton.setObjectName("saveButton")
        self.playOrgButt = QtWidgets.QPushButton(Form)
        self.playOrgButt.setGeometry(QtCore.QRect(230, 390, 101, 41))
        self.playOrgButt.setObjectName("playOrgButt")
        self.myCanvas_Org = QtWidgets.QWidget(Form)
        self.myCanvas_Org.setGeometry(QtCore.QRect(50, 140, 441, 231))
        self.myCanvas_Org.setObjectName("myCanvas_Org")


        myPlot1 = PlotCanvas(self.myCanvas_Org, plotNumber=1)
        myPlot2 = PlotCanvas(self.myCanvas_Conv, plotNumber=2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DeepDreamSound"))
        self.groupBox.setTitle(_translate("Form", "Lokalizacja pliku do przetworzenia"))
        self.toolButton.setText(_translate("Form", "..."))
        self.playConvButt.setText(_translate("Form", "Play Converted"))
        self.convButton.setText(_translate("Form", "Convert"))
        self.saveButton.setText(_translate("Form", "Save"))
        self.playOrgButt.setText(_translate("Form", "Play Oryginal"))


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, plotNumber=1):
        fig = Figure(figsize=(width*0.95, height*0.58), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        if plotNumber == 1:
            self.plotOrg()
        else:
            self.plotConv()


    def plotOrg(self):
        data = [random.random()-0.5 for i in range(250)]
        ax = self.figure.add_subplot(111)
        ax.plot(data)
        ax.set_title('Oryginal sound')
        self.draw()

    def plotConv(self):
        data = [random.random() - 0.5 for i in range(150)]
        ax = self.figure.add_subplot(111)
        ax.plot(data)
        ax.set_title('Converted sound')
        self.draw()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
