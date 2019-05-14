# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\AXDition\Documents\Qt\QtDesignerProjects\GUI_Test2\GUI_Test3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import _thread
import time
import winsound

import librosa
import librosa.display
import scipy.signal
import sounddevice as sd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import deep_dream
import stream_dream




class Ui_Form(object):
    def setupUi(self, Form, width, height):
        Form.setObjectName("Form")
        window_width = width / 2
        window_height = height / 2
        Form.resize(window_width, window_height - 100)
        self.audio_playing = False
        self.audio_loaded = False

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(40, 10, window_width / 2, 80))
        self.groupBox.setObjectName("groupBox")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, window_width / 2 - 50, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.new_threadLoadFile)

        self.horizontalLayout.addWidget(self.toolButton)

        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.playConvButt = QtWidgets.QPushButton(Form)
        self.playConvButt.setGeometry(QtCore.QRect(3 * window_width / (2 * 2.2) + 90 - window_width / (2 * 10),
                                                   window_height / 1.5 + 100, window_width / 10, window_height / 10))
        self.playConvButt.setObjectName("playConvButt")
        self.playConvButt.clicked.connect(self.playDrmNewThread)

        self.convButton = QtWidgets.QPushButton(Form)
        self.convButton.setGeometry(QtCore.QRect(window_width / 2 + 80, 30, window_width / 5, 51))
        self.convButton.setObjectName("convButton")
        self.convButton.clicked.connect(self.dream)

        self.playOrgButt = QtWidgets.QPushButton(Form)
        self.playOrgButt.setGeometry(QtCore.QRect(50 + window_width / (2 * 2.2) - window_width / (2 * 10),
                                                  window_height / 1.5 + 100, window_width / 10, window_height / 10))
        self.playOrgButt.setObjectName("playOrgButt")
        self.playOrgButt.clicked.connect(self.playOrgNewThread)

        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 100, window_width / 2.2 + 20, window_height / 1.5))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.canvas_Org = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.canvas_Org.setContentsMargins(0, 0, 0, 0)
        self.canvas_Org.setObjectName("canvas_Org")

        self.figure = Figure()
        self.figure.set_tight_layout(True)
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
        self.figure2.set_tight_layout(True)
        self.canvas2 = FigureCanvas(self.figure2)
        self.figure2.set_facecolor("black")
        self.ax2 = self.figure2.add_subplot(111)
        self.ax2.clear()
        self.ax2.grid(False)
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_facecolor("black")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(window_width / 2.2 + 80, 100, window_width / 2.2 + 20,
                                                             window_height / 1.5))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        self.canvas_Conv = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.canvas_Conv.setContentsMargins(0, 0, 0, 0)
        self.canvas_Conv.setObjectName("verticalLayout_3")

        self.canvas_Conv.addWidget(self.canvas2)

        self.convButton_2 = QtWidgets.QPushButton(Form)
        self.convButton_2.setGeometry(QtCore.QRect(window_width / 2 + 120 + window_width / 5, 30, window_width / 5, 51))
        self.convButton_2.setObjectName("convButton_2")
        self.convButton_2.clicked.connect(self.new_threadSaveFile)

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

    def dream(self):
        try:
            self.dreamStream = stream_dream.Dream()
            _thread.start_new_thread(self.dream_inner, ())
            _thread.start_new_thread(self.dream_loading, ())
        except:
            print("Error: unable to start thread")

    def dream_loading(self):
        self.ax2 = self.figure2.add_subplot(111)
        self.ax2.clear()
        self.ax2.axis('off')
        self.ax2.grid(False)
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_facecolor("black")
        self.ax2.set_autoscale_on(True)
        while not self.dreamStream.done():
            try:
                self.ax2.pcolormesh(self.dreamStream.get_table(), cmap='gray')
            except:
                print(sys.exc_info())
            time.sleep(0.1)
            self.canvas2.draw()

    def dream_inner(self):
        dream_result = deep_dream.backend(self.filepath, self.dreamStream)
        self.dreamt_signal = dream_result[0][0]
        self.dreamt_sr = dream_result[0][1]
        self.dreamt = True
        f, t, Sxx = scipy.signal.spectrogram(self.dreamt_signal, self.dreamt_sr, scaling='spectrum')
        self.ax2 = self.figure2.add_subplot(111)
        self.ax2.clear()
        self.ax2.axis('off')
        self.ax2.grid(False)
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_facecolor("black")
        self.ax2.set_autoscale_on(True)
        try:
            self.ax2.pcolormesh(t, f, Sxx, cmap='gist_heat')
        except:
            print(sys.exc_info())
        self.canvas2.draw()

    def new_threadLoadFile(self):
        try:
            _thread.start_new_thread(self.loadFile, ())
        except:
            print("Error: unable to start thread")

    def loadFile(self):
        filename, _ = QFileDialog.getOpenFileName(filter="All Files (*);;Wave or mp3 files (*.wav; *.mp3)",
                                                  initialFilter="Wave or mp3 files (*.wav; *.mp3)")
        self.lineEdit.setText(filename)
        self.filepath = filename
        self.x, self.sr = librosa.load(filename)
        self.audio_loaded = True
        f, t, Sxx = scipy.signal.spectrogram(self.x, self.sr, scaling='spectrum')
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.axis('off')
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_facecolor("black")
        self.ax.set_autoscale_on(True)
        try:
            self.ax.pcolormesh(t, f, Sxx, cmap='gist_heat')
        except:
            print(sys.exc_info())
        self.canvas.draw()

    def new_threadSaveFile(self):
        try:
            _thread.start_new_thread(self.saveFile, ())
        except:
            print("Error: unable to start thread")

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(filter="Wave (*.wav)",
                                                  initialFilter="Wave file (*.wav)")
        librosa.output.write_wav(filename, self.dreamt_signal, self.dreamt_sr)

    def playOrgNewThread(self):
        try:
            _thread.start_new_thread(self.playOrg, ())
        except:
            print("Error: unable to start thread")

    def playOrg(self):
        if self.audio_loaded:
            if self.audio_playing:
                sd.stop()
                self.audio_playing = False
            else:
                sd.play(self.x, self.sr)
                self.audio_playing = True
        else:
            winsound.PlaySound('SystemExclamation', winsound.SND_FILENAME)

    def playDrmNewThread(self):
        try:
            _thread.start_new_thread(self.playDrm, ())
        except:
            print("Error: unable to start thread")

    def playDrm(self):
        if self.dreamt:
            if self.audio_playing:
                sd.stop()
                self.audio_playing = False
            else:
                sd.play(self.dreamt_signal, self.dreamt_sr)
                self.audio_playing = True
        else:
            winsound.PlaySound('SystemExclamation', winsound.SND_FILENAME)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form, width, height)
    Form.show()
    sys.exit(app.exec_())

# TODO: Blokowanie rozciągania/Dynamiczny rozmiar
# TODO: Player - linie po spektrogramach
# TODO: Player - Play/Stop jako napisy
# TODO: Idiotoodporność - wczytywanie pustych plików/wczytywanie super dużych plików
# TODO: Optional: Librosa Loading stop
# TODO: Wybór warstwy
# TODO: Wybór modelu
