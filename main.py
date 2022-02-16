import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QFileDialog
from mrc4 import *

import cv2

#-----UTILITIES-----
def goBack():
    # widget.setCurrentIndex(widget.currentIndex() - 1)
    widget.removeWidget(widget.currentWidget())

#-----RC4SCREENS-----
class RC4Screen(QDialog):
    def __init__(self):
        super(RC4Screen, self).__init__()
        loadUi("UI/main.ui", self)

        self.pushButton.clicked.connect(self.goToRC4Encrypt)
        self.pushButton_2.clicked.connect(self.goToRC4Decrypt)

    def goToRC4Encrypt(self):
        rc1 = RC4EncryptScreen()
        widget.addWidget(rc1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToRC4Decrypt(self):
        rc1 = RC4DecryptScreen()
        widget.addWidget(rc1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RC4EncryptScreen(QDialog):
    def __init__(self):
        super(RC4EncryptScreen, self).__init__()
        loadUi("UI/encrypt.ui", self)
        self.mode = "encrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.goButton.clicked.connect(self.runEncoding)
        self.backButton.clicked.connect(goBack)

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/Desktop')
        self.inputFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = readfile_bin(path)
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "output_encrypt/" + self.outputFileField.text() + "." + self.outputFormatField.text()

    def runEncoding(self):
        self.getMessage()
        self.getOutputPath()
        self.key = self.keyField.text()
        acquire_key(self.key)
        result = encrypt_text(self.message)
        writefile_bin(self.outputPath, result)

        self.outputField.setText(result)
        self.label_3.setText("Lihat File Hasil pada Folder Output!")

class RC4DecryptScreen(QDialog):
    def __init__(self):
        super(RC4DecryptScreen, self).__init__()
        loadUi("UI/decrypt.ui", self)
        self.mode = "decrypt"
        self.message = ""
        self.outputPath = ""
        self.key = ""

        #actions
        self.inputButton_1.toggled.connect(self.toggleInputButton1)
        self.inputButton_2.toggled.connect(self.toggleInputButton2)
        self.inputFileButton.clicked.connect(self.browseInput)
        self.goButton.clicked.connect(self.runDecoding)
        self.backButton.clicked.connect(goBack)

    def browseInput(self):
        f = QFileDialog.getOpenFileName(self, 'Open file', '~/Desktop')
        self.inputFileField.setText(f[0])

    def toggleInputButton1(self): self.btnInputState(self.inputButton_1)
    def toggleInputButton2(self): self.btnInputState(self.inputButton_2)

    def btnInputState(self, b):
        if b.text() == "File":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(True)
                self.inputFileButton.setEnabled(True)
                self.fileInputMethod = "File"
                self.inputKeyboardField.setText("")
        elif b.text() == "Keyboard":
            if b.isChecked():
                self.inputKeyboardField.setReadOnly(False)
                self.inputFileButton.setEnabled(False)
                self.fileInputMethod = "Keyboard"
                self.inputFileField.setText("")

    def getMessage(self):
        if (self.fileInputMethod == "File"):
            path = self.inputFileField.text()
            self.message = readfile_bin(path)
        else:
            self.message = self.inputKeyboardField.text()

    def getOutputPath(self):
        self.outputPath = "output_decrypt/" + self.outputFileField.text() + "." + self.outputFormatField.text()

    def runDecoding(self):
        self.getMessage()
        self.getOutputPath()
        self.key = self.keyField.text()
        acquire_key(self.key)
        result = decrypt_text(self.message)
        writefile_bin(self.outputPath, result)
        
        self.outputField.setText(result)
        self.label_3.setText("Lihat File Hasil pada Folder Output!")

    def goToHome(self):
        for i in range(3):
            goBack()

#-----MAIN-----
app = QApplication(sys.argv)
widget = QStackedWidget()

main = RC4Screen()

widget.addWidget(main)
widget.setFixedWidth(640)
widget.setFixedHeight(640)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")