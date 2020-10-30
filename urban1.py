from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import *
import sys
import mysql.connector
from cryptography.fernet import Fernet
import subprocess
import os
import getpass
import time

mySqlPassword  = ""


# #------------------*** CHECKING AND CREATING NEEDED FILES AND FOLDERS ***------------------

# if not os.path.isdir(r"./Dependencies"):
#     os.mkdir(r"./Dependencies")

#     os.mkdir(r"./Dependencies/Encryption")

#     if not os.path.isfile(r"./Dependencies/userpassword.txt"):
#         with open(r"./Dependencies/userpassword.txt","w") as writeFile:
#             pass

# else:
#     if not os.path.isdir(r"./Dependencies/Encryption"):
#         os.mkdir(r"./Dependencies/Encryption")

#     if not os.path.isfile(r"./Dependencies/userpassword.txt"):
#         with open(r"./Dependencies/userpassword.txt","w") as writeFile:
#             pass


# #------------------*** CHECKING AND CREATING NEEDED FILES AND FOLDERS ***------------------

# if not os.path.isdir(r"./Dependencies"):
#     os.mkdir(r"./Dependencies")

#     os.mkdir(r"./Dependencies/Encryption")

#     if not os.path.isfile(r"./Dependencies/userpassword.txt"):
#         with open(r"./Dependencies/userpassword.txt","w") as writeFile:
#             pass

# else:
#     if not os.path.isdir(r"./Dependencies/Encryption"):
#         os.mkdir(r"./Dependencies/Encryption")

#     if not os.path.isfile(r"./Dependencies/userpassword.txt"):
#         with open(r"./Dependencies/userpassword.txt","w") as writeFile:
#             pass



# #-----------*** FUNCTIONS FOR ENCRYPTING AND DECRYPTING USER'S CONFIDENTIAL AND SENSITIVE DATA ***--------

# def writeKey():
#     if not os.path.isfile(r"./Dependencies/Encryption/key.key") or \
#         len(open(r"./Dependencies/Encryption/key.key").read())==0:
#         key=Fernet.generate_key()
#         with open(r"./Dependencies/Encryption/key.key","wb") as writeKeyFile:
#             writeKeyFile.write(key)

# def loadKey():
#     with open(r"./Dependencies/Encryption/key.key","rb") as loadKeyFile:
#         return loadKeyFile.read()
 
# def encrypt(data,key):
#     f = Fernet(key)
#     encryptedData = f.encrypt(data.encode())
#     with open(r'./Dependencies/userpassword.txt','wb') as encryptedPass:
#         encryptedPass.write(encryptedData)

# def decrypt(encrypted,key):

#     f = Fernet(key)
#     decryptedData = f.decrypt(encrypted,ttl=None)
#     return decryptedData.decode()


# writeKey()
# key = loadKey()
# f = Fernet(key)







class UserNamePassLogin(QWidget):
    # def checkExistingUser(self):
    #     with open(r'./Dependencies/userpassword.txt','r+') as savedPass:
    #         self.userPass=savedPass.read()
    #         if len(self.userPass)==0:


    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOGIN TO URBAN KINETICS!")
        self.setGeometry(200,200,350,200)
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.loginLabel = QLabel("LOGIN / SIGNUP ")
        self.loginLabel.setStyleSheet("font-size:18pt;font-family:Open Sans; text-decoration:underline;")

        self.userEmail = QLineEdit()
        self.userEmail.setPlaceholderText("Enter YOUR EMAIL HERE!")

        self.userName = QLineEdit()
        self.userName.setPlaceholderText("ENTER YOUR USERNAME HERE!")

        self.userMySqlPassword = QLineEdit()
        self.userMySqlPassword.setPlaceholderText("ENTER YOUR MYSQL PASSWORD HERE!")
        self.userMySqlPassword.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton("LOGIN / SIGNUP")
        # self.loginButton.clicked.connect(self.getUserLogin)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.subLayout = QFormLayout()

        self.setLayout(self.mainLayout)

        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.subLayout)
        self.mainLayout.addStretch()

        self.subLayout.setVerticalSpacing(15)
        self.subLayout.addRow("",self.loginLabel)
        self.subLayout.addRow("EMAIL :", self.userEmail)
        self.subLayout.addRow("USERNAME:", self.userName)
        self.subLayout.addRow("MYSQL PASSWORD :", self.userMySqlPassword)
        self.subLayout.addRow("",self.loginButton)

        self.show()


    def getUserLogin(self):
        global userEmail
        global UserName 

        userEmail = self.userEmail.text()
        userName = self.userName.text()
        MySqlPassword = self.userMySqlPassword.text()
        print(userEmail)
        print(userName)
        print(MySqlPassword)

        try:
            con = mysql.connector.connect(host = "localhost", user = "root", password = MySqlPassword)
            self.urban_kinetics = UrbanKineticsMainWindow()
            self.close()


        except mysql.connector.Error as err:
            if err.errno == 1045:
                worngPassMsg = QMessageBox.critical(self,"INCORRECT MYSQL PASSWORD!","PASSWORD YOU JUST TYPED IS INCORRECT,\nPLEASE CHECK THE PASSWORD!",QMessageBox.Ok|QMessageBox.Close,QMessageBox.Ok)

                if worngPassMsg == QMessageBox.Close:
                    sys.exit()









class UrbanKineticsMainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("URBAN-KINETICS :- THE ONLY GYM YOU NEED!")
        self.setGeometry(200,200,500,500)
        self.setStyleSheet("background-color:rgb(170, 170, 255);font-family: Comic Sans;font-size:14pt;")
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.urbanKineticsLabel = QLabel("URBAN KINETICS")
        self.urbanKineticsLabel.setStyleSheet("font-size:24pt;font-family:Open Sans; text-decoration:underline;")

        self.addMemberButton = QPushButton(" Add A New Member ") 
        self.addMemberButton.setStyleSheet("background-color:rgb(255, 255, 0)")
        self.addMemberButton.resize(50,20)
        self.addMemberButton.setStatusTip("ADD A MEMBER")

        self.showExistingRecordButton = QPushButton("   Existing Records   ") 
        self.showExistingRecordButton.setStyleSheet("background-color:rgb(0, 255, 127)")

        self.showTrainerButton = QPushButton("   Trainers Records   ") 
        # self.showBalanceButton.iconSize()
        self.showTrainerButton.setStyleSheet("background-color:rgb(85, 170, 0)")

        self.showBalanceButton = QPushButton("           Balance           ") 
        self.showBalanceButton.setStyleSheet("background-color:rgb(255, 170, 0)")

        self.statusBar = QStatusBar()






    def layouts(self):
        self.mainLayout = QVBoxLayout()

        self.topLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        self.addMemberLayout = QHBoxLayout()
        self.showExistingRecordLayout = QHBoxLayout()
        self.showTrainerLayout = QHBoxLayout()
        self.showBalanceLayout = QHBoxLayout()

        self.mainLayout.addStretch()
        # self.mainLayout.addSpacing(200)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.mainLayout.addStretch()
        
        self.bottomLayout.addLayout(self.addMemberLayout)
        self.bottomLayout.addLayout(self.showExistingRecordLayout)
        self.bottomLayout.addLayout(self.showTrainerLayout)
        self.bottomLayout.addLayout(self.showBalanceLayout)
        

        # self.mainLayout.addLayout(self.addMemberLayout)
        # self.mainLayout.addLayout(self.showExistingRecordLayout)
        # self.mainLayout.addLayout(self.showTrainerLayout)
        # self.mainLayout.addLayout(self.showBalanceLayout)
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.urbanKineticsLabel)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(25,20,10,50)

        self.bottomLayout.addWidget(self.statusBar)

        self.addMemberLayout.addStretch()
        self.addMemberLayout.addWidget(self.addMemberButton)
        self.addMemberLayout.addStretch()
    
        self.showExistingRecordLayout.addStretch()
        self.showExistingRecordLayout.addWidget(self.showExistingRecordButton)
        self.showExistingRecordLayout.addStretch()

        self.showTrainerLayout.addStretch()
        self.showTrainerLayout.addWidget(self.showTrainerButton)
        self.showTrainerLayout.addStretch()

        self.showBalanceLayout.addStretch()
        self.showBalanceLayout.addWidget(self.showBalanceButton)
        self.showBalanceLayout.addStretch()

        self.setLayout(self.mainLayout)
        self.show()






def main():
    App = QApplication(sys.argv)
    start_application = UserNamePassLogin()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()