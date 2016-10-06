# coding=UTF8
import functionsCarto

import os
import sys
from PyQt4 import QtGui
from PyQt4 import uic
from pathlib import Path



API_KEY =''
cartodb_user = ''


isUserAssigned = True

class initWindow(QtGui.QMainWindow):
       def __init__(self):
              QtGui.QMainWindow.__init__(self)
              uic.loadUi("initWindow.ui", self)
              self.btnUpload.clicked.connect(self.uploadFile)
              self.btnFileCSV.clicked.connect(self.showDlgGetFile)

       
       def showEvent(self, event):
              my_file = Path("secret")
              if my_file.is_file():
                     print("111")
              else:
                     #cartodb_user, API_KEY = dlgApikey.getUserApiKey()
                     #if API_KEY == "".strip() or cartodb_user.strip() == "":
                     #       isUserAssigned = False                            
                     return      
       
       def closeEvent(self, event):
              rsult = QtGui.QMessageBox.question(self, "Exit", "Desea mantener los datos para volverte conectar a cartoDB con este ususario?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
              if rsult == QtGui.QMessageBox.No:
                     os.remove("secret")                     
              return

       def uploadFile(self):
              functionsCarto.uploadFile(API_KEY, cartodb_user, self.txtFile.text(), False)
              
       def openDlgApikey(self):
              #self.dlgApi.exec_()
              a =""
              
       def showDlgGetFile(self):
              file_name = QtGui.QFileDialog.getOpenFileName(self, "Open Data File", "", "CSV data files (*.csv)")
              self.txtFile.setText(file_name) 
              
class dlgApikey(QtGui.QDialog):
       def __init__(self):
              QtGui.QMainWindow.__init__(self)
              uic.loadUi("dlgApikey.ui", self)
              self.btnOk.clicked.connect(self.acceptBtn)
              
       def getTxtUser(self):
              return self.txtUser.text().strip() 

       def getTxtApiKey(self):
              return self.txtApikey.text().strip()    
       
       @staticmethod
       def getUserApiKey():
              dialog = dlgApikey()
              result = dialog.exec_()
              return result.getTxtUser(), result.getTxtApiKey()              
       
       def closeEvent(self, event):
                     return
                     
       def acceptBtn(self):
              b = False
              if self.txtUser.text().strip() == "":
                     self.txtUser.setStyleSheet("border: 1px solid red;")
                     b = True
              else:
                     self.txtUser.setStyleSheet("border: 1px solid green;")                     
              
              if self.txtApikey.text().strip() == "":
                     self.txtApikey.setStyleSheet("border: 1px solid red;")
                     b = True
              else:
                     self.txtApikey.setStyleSheet("border: 1px solid green;")                     
              
              
              API_KEY = self.txtApikey.text()
              cartodb_user = self.txtUser.text()
              if b == False:              
                     self.accept()

                     
app= QtGui.QApplication(sys.argv)
w=initWindow()
w.show()
if isUserAssigned == True:
       app.exec_()



