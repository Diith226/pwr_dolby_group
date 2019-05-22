# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\AXDition\Documents\Qt\QtDesignerProjects\GUI_Test2\GUI_Test3.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!Ł

import _thread
import time
import winsound

import librosa
import numpy as np
import librosa.display
import scipy.signal
import sounddevice as sd
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import deep_dream
import stream_dream


class Ui_DeepDreamSound(object):
    '''=============================='''
    '''!       Widgets Setup        !'''
    '''=============================='''

    def setupUi(self, DeepDreamSound):
        DeepDreamSound.setObjectName("DeepDreamSound")
        DeepDreamSound.resize(993, 701)
        DeepDreamSound.setMinimumSize(QtCore.QSize(769, 618))
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(DeepDreamSound)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tabWidget = QtWidgets.QTabWidget(DeepDreamSound)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 121))
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 121))
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.filePathTab = QtWidgets.QWidget()
        self.filePathTab.setObjectName("filePathTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.filePathTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.filePathLayout = QtWidgets.QHBoxLayout()
        self.filePathLayout.setObjectName("filePathLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.filePathLayout.addItem(spacerItem)
        self.filePathButt = QtWidgets.QToolButton(self.filePathTab)
        self.filePathButt.setObjectName("filePathButt")
        self.filePathLayout.addWidget(self.filePathButt)
        self.pathView = QtWidgets.QLineEdit(self.filePathTab)
        self.pathView.setEnabled(False)
        self.pathView.setObjectName("pathView")
        self.filePathLayout.addWidget(self.pathView)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.filePathLayout.addItem(spacerItem1)
        self.startDreamButt = QtWidgets.QPushButton(self.filePathTab)
        self.startDreamButt.setEnabled(True)
        self.startDreamButt.setMinimumSize(QtCore.QSize(111, 41))
        self.startDreamButt.setMaximumSize(QtCore.QSize(16777215, 41))
        self.startDreamButt.setObjectName("startDreamButt")
        self.filePathLayout.addWidget(self.startDreamButt)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.filePathLayout.addItem(spacerItem2)
        self.saveDreamButt = QtWidgets.QPushButton(self.filePathTab)
        self.saveDreamButt.setMinimumSize(QtCore.QSize(111, 41))
        self.saveDreamButt.setMaximumSize(QtCore.QSize(16777215, 41))
        self.saveDreamButt.setObjectName("saveDreamButt")
        self.filePathLayout.addWidget(self.saveDreamButt)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.filePathLayout.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.filePathLayout)
        self.tabWidget.addTab(self.filePathTab, "")
        self.dreamSettingsTab = QtWidgets.QWidget()
        self.dreamSettingsTab.setObjectName("dreamSettingsTab")
        self.tabWidget.addTab(self.dreamSettingsTab, "")
        self.verticalLayout_7.addWidget(self.tabWidget)
        self.label1 = QtWidgets.QLabel(DeepDreamSound)
        self.label1.setMinimumSize(QtCore.QSize(171, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(11)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.verticalLayout_7.addWidget(self.label1, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.canvasOrg = QtWidgets.QVBoxLayout()
        self.canvasOrg.setObjectName("canvasOrg")
        self.verticalLayout_7.addLayout(self.canvasOrg)
        self.label2 = QtWidgets.QLabel(DeepDreamSound)
        self.label2.setMinimumSize(QtCore.QSize(171, 31))
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        font.setPointSize(11)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.verticalLayout_7.addWidget(self.label2, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        self.canvasConv = QtWidgets.QVBoxLayout()
        self.canvasConv.setObjectName("canvasConv")
        self.verticalLayout_7.addLayout(self.canvasConv)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_7.addItem(spacerItem4)
        self.playerButtLayout = QtWidgets.QHBoxLayout()
        self.playerButtLayout.setObjectName("playerButtLayout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.playerButtLayout.addItem(spacerItem5)
        self.playOrgButt = QtWidgets.QPushButton(DeepDreamSound)
        self.playOrgButt.setMinimumSize(QtCore.QSize(111, 41))
        self.playOrgButt.setMaximumSize(QtCore.QSize(16777215, 41))
        self.playOrgButt.setObjectName("playOrgButt")
        self.playerButtLayout.addWidget(self.playOrgButt)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.playerButtLayout.addItem(spacerItem6)
        self.stopButt = QtWidgets.QPushButton(DeepDreamSound)
        self.stopButt.setMinimumSize(QtCore.QSize(111, 41))
        self.stopButt.setMaximumSize(QtCore.QSize(16777215, 41))
        self.stopButt.setObjectName("stopButt")
        self.playerButtLayout.addWidget(self.stopButt)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.playerButtLayout.addItem(spacerItem7)
        self.playConvButt = QtWidgets.QPushButton(DeepDreamSound)
        self.playConvButt.setMinimumSize(QtCore.QSize(111, 41))
        self.playConvButt.setMaximumSize(QtCore.QSize(16777215, 41))
        self.playConvButt.setObjectName("playConvButt")
        self.playerButtLayout.addWidget(self.playConvButt)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.playerButtLayout.addItem(spacerItem8)
        self.verticalLayout_7.addLayout(self.playerButtLayout)

        '''=============================='''
        '''!        Buttons Setup        !'''
        '''=============================='''

        self.playConvButt.clicked.connect(self.playDrmNewThread)
        self.playOrgButt.clicked.connect(self.playOrgNewThread)
        self.stopButt.clicked.connect(self.stop)
        self.saveDreamButt.clicked.connect(self.new_threadSaveFile)
        self.filePathButt.clicked.connect(self.new_threadLoadFile)
        self.startDreamButt.clicked.connect(self.dream)

        '''=============================='''
        '''!        Figure Setup        !'''
        '''=============================='''

        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.canvasOrg.addWidget(self.canvas)
        self.figure.set_facecolor("black")
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_facecolor("black")

        self.figure2 = Figure(tight_layout=True)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvasConv.addWidget(self.canvas2)
        self.figure2.set_facecolor("black")
        self.ax2 = self.figure2.add_subplot(111)
        self.ax2.clear()
        self.ax2.grid(False)
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_facecolor("black")

        '''=============================='''
        '''=============================='''
        self.audio_playing = False
        self.audio_loaded = False
        self.retranslateUi(DeepDreamSound)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DeepDreamSound)

    def retranslateUi(self, DeepDreamSound):
        _translate = QtCore.QCoreApplication.translate
        DeepDreamSound.setWindowTitle(_translate("DeepDreamSound", "Deep Dream Sound"))
        self.filePathButt.setText(_translate("DeepDreamSound", "..."))
        self.startDreamButt.setText(_translate("DeepDreamSound", "Start Dreaming"))
        self.saveDreamButt.setText(_translate("DeepDreamSound", "Save Dream"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.filePathTab), _translate("DeepDreamSound", "File path"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dreamSettingsTab),
                                  _translate("DeepDreamSound", "Dream settings"))
        self.label1.setText(_translate("DeepDreamSound", "Original File Spectrogram"))
        self.label2.setText(_translate("DeepDreamSound", "Your Dream Spectrogram"))
        self.playOrgButt.setText(_translate("DeepDreamSound", "Play Oryginal"))
        self.stopButt.setText(_translate("DeepDreamSound", "Stop"))
        self.playConvButt.setText(_translate("DeepDreamSound", "Play Converted"))

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
        #f, t, Sxx = scipy.signal.spectrogram(self.dreamt_signal, self.dreamt_sr, scaling='spectrum')
        S = np.abs(librosa.stft(self.dreamt_signal))
        S = librosa.power_to_db(S ** 2, ref=np.max)
        self.ax2 = self.figure2.add_subplot(111)
        self.ax2.clear()
        self.ax2.axis('off')
        self.ax2.grid(False)
        self.ax2.set_xticks([])
        self.ax2.set_yticks([])
        self.ax2.set_facecolor("black")
        self.ax2.set_autoscale_on(True)
        try:
            self.ax2.pcolormesh(S, cmap='gist_heat')
        except:
            print(sys.exc_info())
        self.canvas2.draw()

    def stop(self):
        sd.stop()
        self.audio_playing = False

    def new_threadLoadFile(self):
        try:
            _thread.start_new_thread(self.loadFile, ())
        except:
            print("Error: unable to start thread")

    def loadFile(self):
        filename, _ = QFileDialog.getOpenFileName(filter="All Files (*);;Wave or mp3 files (*.wav; *.mp3)",
                                                  initialFilter="Wave or mp3 files (*.wav; *.mp3)")
        self.pathView.setText(filename)
        self.filepath = filename
        self.x, self.sr = librosa.load(filename)
        self.audio_loaded = True
        #f, t, Sxx = scipy.signal.spectrogram(self.x, self.sr, scaling='spectrum')
        S = np.abs(librosa.stft(self.x))
        S = librosa.power_to_db(S**2,ref=np.max)
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.axis('off')
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_facecolor("black")
        self.ax.set_autoscale_on(True)
        try:
            self.ax.imshow(S, cmap='gist_heat', aspect ='auto')
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
    DeepDreamSound = QtWidgets.QWidget()
    ui = Ui_DeepDreamSound()
    ui.setupUi(DeepDreamSound)
    DeepDreamSound.show()
    sys.exit(app.exec_())

# TODO: Blokowanie rozciągania/Dynamiczny rozmiar
# TODO: Player - linie po spektrogramach
# TODO: Player - Play/Stop jako napisy
# TODO: Idiotoodporność - wczytywanie pustych plików/wczytywanie super dużych plików
# TODO: Optional: Librosa Loading stop
# TODO: Wybór warstwy
# TODO: Wybór modelu
