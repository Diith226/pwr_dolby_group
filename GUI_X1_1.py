# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\AXDition\Documents\Qt\QtDesignerProjects\GUI_Test2\GUI_Test2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import threading
import winsound

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog


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
        self.toolButton.clicked.connect(self.loadFile)

        self.horizontalLayout.addWidget(self.toolButton)

        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.myCanvas_Conv = QtWidgets.QWidget(Form)
        self.myCanvas_Conv.setGeometry(QtCore.QRect(510, 140, 441, 231))
        self.myCanvas_Conv.setObjectName("myCanvas_Conv")

        self.playConvButt = QtWidgets.QPushButton(Form)
        self.playConvButt.setGeometry(QtCore.QRect(690, 390, 101, 41))
        self.playConvButt.setObjectName("playConvButt")
        self.playConvButt.clicked.connect(self.playConv)

        self.convButton = QtWidgets.QPushButton(Form)
        self.convButton.setGeometry(QtCore.QRect(640, 40, 120, 51))
        self.convButton.setObjectName("convButton")
        self.convButton.clicked.connect(self.dreamSound)

        self.saveButton = QtWidgets.QPushButton(Form)
        self.saveButton.setGeometry(QtCore.QRect(800, 40, 120, 51))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.saveYourDream)

        self.playOrgButt = QtWidgets.QPushButton(Form)
        self.playOrgButt.setGeometry(QtCore.QRect(230, 390, 101, 41))
        self.playOrgButt.setObjectName("playOrgButt")
        self.playOrgButt.clicked.connect(self.playOrgNewThread)

        self.myCanvas_Org = QtWidgets.QWidget(Form)
        self.myCanvas_Org.setGeometry(QtCore.QRect(50, 140, 441, 231))
        self.myCanvas_Org.setObjectName("myCanvas_Org")

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
        self.playOrgButt.setText(_translate("Form", "Play Original"))

        # Widgets metods/slots

    key = 1
    playOrgThread = threading.Thread

    def playOrgNewThread(self):
        if self.key:
            self.key = 0

            if self.lineEdit.text():
                self.playOrgThread = threading.Thread(target=self.playOrg())
                self.playOrgThread.start()
        else:
            self.key = 1
            winsound.PlaySound(self.filename, winsound.SND_PURGE)

    def playOrg(self):
        self.filename = self.lineEdit.text()
        winsound.PlaySound(self.filename, winsound.SND_FILENAME)

    def playConv(self):
        print("Not plaing yet :D")

    def loadFile(self):
        filename, _ = QFileDialog.getOpenFileName(filter="All Files (*);;Wave files (*.wav)",
                                                  initialFilter="Wave files (*.wav)")
        self.lineEdit.setText(filename)

    def dreamSound(self):
        print("Converting file")

    def saveYourDream(self):
        print("Saving deep dream sound")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
sys.exit(app.exec_())
