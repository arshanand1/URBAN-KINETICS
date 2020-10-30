from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *
import sys
import mysql.connector
from cryptography.fernet import Fernet
import subprocess
import os
import getpass
import time
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import smtplib
import time
from socket import error
import datetime

userEmail = ""
userName = ""
urbanWindowCount=0
mySqlPassword  = ""
con = None
cur = None

databaseName = "urban_kinetics"

usersTableName = "users"
usersTableFields = "card_num int(5) NOT NULL AUTO_INCREMENT, name varchar(20) NOT NULL,\
            phn int(10) NOT NULL, address varchar(100) NOT NULL, gender varchar(1) NOT NULL, joining_date date,\
                time_period varchar(50), renewal_date date, gym_price int(6), trainer_name varchar(20),\
                    trainer_type varchar(20), trainer_price int(5), id_proof varchar(20),\
                        mode_of_payment varchar(20), PRIMARY KEY(card_num)"


trainersTableName = "trainers"
trainersTableFields = "sr_no int(5) NOT NULL AUTO_INCREMENT, name varchar(20),\
    experience varchar(20), speciality varchar(50), age int(2), PRIMARY KEY(SR_NO)"

trainersNameList = ['Thomas', 'Stephen','Lewis','Samuel', 'Kane']
trainersExperience = ['2 Years','5 Years','8 Years','10 Years','6 Years', '3 Years']
trainersSpeciality = ['Weight Loss', 'Muscle Gain', 'Aesthetics','Calisthenics','Aerobics']
trainersAge = [26, 28, 32, 35, 30, 29]
trainer_id=None

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
        self.loginButton.clicked.connect(self.getUserLogin)

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
        global userName 
        global mySqlPassword
        global con
        global cur
        

        userEmail += self.userEmail.text()
        userName += self.userName.text()
        mySqlPassword += self.userMySqlPassword.text()
        print(userEmail)
        print(userName)
        print(mySqlPassword)

        try:
            con = mysql.connector.connect(host = "localhost", user = "root", password = mySqlPassword, get_warnings =True)
            cur = con.cursor()
            self.urban_kinetics = UrbanKineticsMainWindow()
            self.close()
            self.sendEmail()
            


        except mysql.connector.Error as err:
            if err.errno == 1045:
                wrongPassMsg = QMessageBox.critical(self,"INCORRECT MYSQL PASSWORD!","PASSWORD YOU JUST TYPED IS INCORRECT,\nPLEASE CHECK THE PASSWORD!",QMessageBox.Ok|QMessageBox.Close,QMessageBox.Ok)

                if wngPassMsg == QMessageBox.Close:
                    sys.exit()


    def sendEmail(self):

        while True:
            try:
                def sendMsg(subject, msg):
                    try:
                        server = smtplib.SMTP('smtp.gmail.com:587')
                        server.ehlo()
                        server.starttls()
                        time.sleep(0.5)
                        server.login('urban.kinetics.no.reply@gmail.com','urban12345')
                        message = f'Subject: {subject}\n\n{msg}'
                        time.sleep(0.5)
                        server.sendmail('urban.kinetics.no.reply@gmail.com',userEmail,message)
                        time.sleep(0.5)
                        server.quit()
                    except error as e:
                        if e.errno == 11004:
                            QMessageBox.information(self,"NO INTERNET","Can't Send You Updates Via Email, Make Sure You Are Connected To The Internet, Now!\nSorry For Inconvinence!")
                            # print("Make Sure You Are Connected To Internet To Receive The Updates You Made!")
                        else: 
                            QMessageBox.information(self,"No EMAIL UPDATES!","Can't Send You Updates Via Email, Now!\nSorry For Inconvinence!")
                            # print('Internal Server Error While Sending You Updates Via Email! \n\nSorry For The Inconvenience')
                        
                break
                
            except  Exception as e:
                print("Server Error, Trying again!")
                time.sleep(5)

        subject = "You Just Logged in to Urban-Kinetics"
        msg = f"Hello From URBAN KINETICS, {userName} You Just Logged Into Urban-Kinetics at {datetime.datetime.now().time().strftime('%H:%M:%S')} on {datetime.datetime.now().date()} Please Check If It Was Not You!\n\nAuto Generated message mailed at {datetime.datetime.now().date()}  {datetime.datetime.now().time().strftime('%H:%M:%S')}\nDo Not Reply To This Message!\n\nTHANK YOU!\nTEAM URBAN-KINETICS"

        sendMsg(subject,msg)





class UrbanKineticsMainWindow(QWidget):
    #----------------------------------------------------------

    #----------------------------------------------------------
    def __init__(self):
        global urbanWindowCount
        super().__init__()
        print(mySqlPassword, "pass")

        self.setWindowTitle("URBAN-KINETICS :- THE ONLY GYM YOU NEED!")
        self.setGeometry(200,200,500,500)
        self.setStyleSheet("background-color:rgb(170, 170, 255);font-family: Comic Sans;font-size:14pt;")
        if urbanWindowCount == 0:
            self.MySqlHandler()
        self.mainDesign()
        self.layouts()

    def mainDesign(self):
        self.urbanKineticsLabel = QLabel("URBAN KINETICS")
        self.urbanKineticsLabel.setStyleSheet("font-size:24pt;font-family:Open Sans; text-decoration:underline;")

        self.addMemberButton = QPushButton(" Add A New Member ") 
        self.addMemberButton.setStyleSheet("background-color:rgb(255, 255, 0)")
        self.addMemberButton.clicked.connect(self.enterMemberDetails)

        self.showExistingRecordButton = QPushButton("   Existing Records   ") 
        self.showExistingRecordButton.setStyleSheet("background-color:rgb(0, 255, 127)")
        self.showExistingRecordButton.clicked.connect(self.showExistingRecord)

        self.showTrainerButton = QPushButton("   Trainers Records   ") 
        self.showTrainerButton.clicked.connect(self.getTrainersRecord)

        self.showTrainerButton.setStyleSheet("background-color:rgb(85, 170, 0)")

        self.showBalanceButton = QPushButton("           Balance           ") 
        self.showBalanceButton.setStyleSheet("background-color:rgb(255, 170, 0)")
        self.showBalanceButton.clicked.connect(self.showBalance)



    def MySqlHandler(self):
        global urbanWindowCount
        urbanWindowCount+=1
        self.trainersTableInitialiser()
        self.usersTableInitialiser()


    def trainersTableInitialiser(self):
        global trainersTableName
        global trainersTableFields
        global trainersNameList
        global trainersExperience
        global trainersSpeciality
        global trainersAge
       
        trainersId = "NULL"

        trainersTableName = "trainers"
        trainersTableFields = "sr_no int(5) NOT NULL AUTO_INCREMENT, name varchar(20),\
            experience varchar(20), speciality varchar(50), age int(2), PRIMARY KEY(SR_NO)"

        trainersNameList = ['Thomas', 'Stephen','Lewis','Samuel', 'Kane']
        trainersExperience = ['2 Years','5 Years','8 Years','10 Years','6 Years', '3 Years']
        trainersSpeciality = ['Weight Loss', 'Muscle Gain', 'Aesthetics','Calisthenics','Aerobics']
        trainersAge = [26, 28, 32, 35, 30, 29]

        makeOrCheckDatabase = f"create database if not exists {databaseName}"
        cur.execute(makeOrCheckDatabase)

        useDatabase = f"use {databaseName}"
        cur.execute(useDatabase)

        makeOrCheckTrainersTable = f"create table if not exists {trainersTableName}({trainersTableFields}) "
        cur.execute(makeOrCheckTrainersTable)

        if cur.fetchwarnings():
            for errorNumber in cur.fetchwarnings():
                
                if errorNumber[1]==1050:
                    break
            else:
                print("Making trainer table")
                makeAutoIncrementAt1001 = f"ALTER TABLE {trainersTableName} AUTO_INCREMENT = 1001"
                cur.execute(makeAutoIncrementAt1001)


                def query(command):
                    cur.execute(command)
                    con.commit()


                for i in range(len(trainersNameList)):
                    insertTrainersRecord = f"insert into {trainersTableName} value({trainersId}, '{trainersNameList[i]}','{trainersExperience[i]}', '{trainersSpeciality[i]}', '{trainersAge[i]}')"

                    query(insertTrainersRecord)

        else:
            print('making trainer table')
            makeAutoIncrementAt1001 = f"ALTER TABLE {trainersTableName} AUTO_INCREMENT = 1001"
            cur.execute(makeAutoIncrementAt1001)


            def query(command):
                cur.execute(command)
                con.commit()


            for i in range(len(trainersNameList)):
                insertTrainersRecord = f"insert into {trainersTableName} value({trainersId}, '{trainersNameList[i]}','{trainersExperience[i]}', '{trainersSpeciality[i]}', '{trainersAge[i]}')"

                query(insertTrainersRecord)


    def usersTableInitialiser(self):

        global usersTableName
        global usersTableFields
        usersId = "NULL"

        usersTableName = "users"

        usersTableFields = "card_num int(5) NOT NULL AUTO_INCREMENT, name varchar(20) NOT NULL,\
            phn int(10) NOT NULL, address varchar(100) NOT NULL, gender varchar(1) NOT NULL, joining_date date,\
                time_period varchar(50), renewal_date date, gym_price int(6), trainer_name varchar(20),\
                    trainer_type varchar(20), trainer_price int(5), id_proof varchar(20),\
                        mode_of_payment varchar(20), PRIMARY KEY(card_num)"

        makeOrCheckDatabase = f"create database if not exists {databaseName}"
        cur.execute(makeOrCheckDatabase)

        useDatabase = f"use {databaseName}"
        cur.execute(useDatabase)

        makeOrCheckUsersTable = f"create table if not exists {usersTableName}({usersTableFields}) "
        cur.execute(makeOrCheckUsersTable)

        if cur.fetchwarnings():
            for errorNumber in cur.fetchwarnings():
                
                if errorNumber[1]==1050:
                    break
            else:
                print("making users table")
                makeAutoIncrementAt1001 = f"ALTER TABLE {usersTableName} AUTO_INCREMENT = 1001"
                cur.execute(makeAutoIncrementAt1001)
        
        else:
            print("making users table")
            makeAutoIncrementAt1001 = f"ALTER TABLE {usersTableName} AUTO_INCREMENT = 1001"
            cur.execute(makeAutoIncrementAt1001)


    def showExistingRecord(self):
        self.existingRecord = UsersRecord()
        self.close()


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
        

        self.topLayout.addStretch()
        self.topLayout.addWidget(self.urbanKineticsLabel)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(25,20,10,50)


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


    def enterMemberDetails(self):
        self.memberForm = LoginForm()
        self.close()

    def getTrainersRecord(self):
        self.trainerRecord = TrainersRecord()
        self.close()

    def showBalance(self):
        self.balance = ShowBalance()
        self.close()



class LoginForm(QWidget):


    def __init__(self):
        super().__init__()
    
        self.setWindowTitle(" ENTER YOUR DETAILS ")
        self.setGeometry(200,200,400,200)
        self.setStyleSheet("background-color:rgb(170, 170, 255);font-family: Comic Sans;font-size:10pt;")
        self.mainForm()
        self.layouts()


    def mainForm(self):
        self.urbanKineticslable = QLabel("URBAN KINETICS")
        self.urbanKineticslable.setStyleSheet("background-color:rgb(89, 155, 255);font-family: Comic Sans;font-size:16pt;text-decoration:underline;")
        

        self.cardnumlable = QLineEdit()
        self.cardnumlable.setPlaceholderText("ENTER CARD NO. OR LEAVE BLANK FOR AUTO GENERATION")

        self.namelable = QLineEdit()
        self.namelable.setPlaceholderText("ENTER NAME")

        self.address = QLineEdit()
        self.address.setPlaceholderText("ENTER ADDRESS")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("ENTER PHONE NUMBER")

        self.male = QRadioButton("MALE")
        self.female = QRadioButton("FEMALE")
        self.male.setChecked(True)

        self.join = QLineEdit()
        self.join.setPlaceholderText("ENTER JOINING DATE")

        options=['One Day Pass', '12 Months', '6 Months', '3 Months', '1 Month']
        self.timeperiod = QComboBox()
        self.timeperiod.setPlaceholderText("CHOOSE")
        self.timeperiod.addItems(options)
        

        self.renewal = QLineEdit()
        self.renewal.setPlaceholderText("ENTER LAST DATE PACKAGE")

        feeStructure=['500', '24000', '15000', '8000', '3000']
        self.gymfee = QComboBox()
        self.gymfee.setPlaceholderText("CHOOSE")
        self.gymfee.addItems(feeStructure)

        # self.discountpercent = QLineEdit()
        # self.discountpercent.setPlaceholderText("ENTER DISCOUNT PERCENT")


        trainerNameQuery = f"select name from {trainersTableName}"
        cur.execute(trainerNameQuery)
        self.trainerName = QComboBox()
        for trainerName in cur.fetchall():
            self.trainerName.addItem(trainerName[0])

        traineroption=['REGULAR','PERSONAL']
        self.trainertype = QComboBox()
        self.trainertype.setPlaceholderText("CHOOSE")
        self.trainertype.addItems(traineroption)

        trainerpriceoption = ['800','1500']
        self.trainerprice = QComboBox()
        self.trainerprice.setPlaceholderText("ENTER TRAINER FEE")
        self.trainerprice.addItems(trainerpriceoption)

        self.idproof = QLineEdit()
        self.idproof.setPlaceholderText("ID PROOF PROVIDED")

        self.modeofpayment = QLineEdit()
        self.modeofpayment.setPlaceholderText("PAYMENT MADE THROUGH")

        self.addMember = QPushButton("ADD MEMBER")
        self.addMember.setStyleSheet("background-color:rgb(255, 255, 127);font-size:12pt;text-decoration:bold;")
        self.addMember.clicked.connect(self.fillForm)



    def fillForm(self):
        card_no = self.cardnumlable.text()
        if len(card_no)==0:
            card_no = "NULL"
        name=self.namelable.text()
        address=self.address.text()
        phn=self.phone.text()
        if self.male.isChecked():
            gender = "M"
        
        else:
            gender = "F"

        joining_date=self.join.text()
        time_period=self.timeperiod.currentText()
        renewal_date=self.renewal.text()
        gym_price=self.gymfee.currentText()
        trainer_name=self.trainerName.currentText()
        trainer_type=self.trainertype.currentText()
        trainer_price=self.trainerprice.currentText()
        # discount_percent=self.discountpercent.text()
        mode_of_payment=self.modeofpayment.text()
        id_proof=self.idproof.text()
        # query="insert into users(card_num,name,phn,address,gender,joining_date,time_period,renewal_date,gym_price,trainer_name,trainer_type,trainer_price,discount_percent,id_proof,mode_of_payment) \
        # values (%s,'%s',%s,'%s','%s','%s','%s','%s','%s','%s',%s,%s,'%s','%s','%s')"%(card_no,name,phn,address,gender,joining_date,time_period,renewal_date,gym_price,trainer_name,trainer_type,trainer_price,discount_percent,id_proof,mode_of_payment)

        query=f"insert into users(card_num,name,phn,address,gender,joining_date,time_period,renewal_date,gym_price,trainer_name,trainer_type,trainer_price,id_proof,mode_of_payment) \
        values ({card_no},'{name}',{phn},'{address}','{gender}','{joining_date}','{time_period}','{renewal_date}',{gym_price},'{trainer_name}','{trainer_type}',{trainer_price},'{id_proof}','{mode_of_payment}')"
        data = cur.execute(query)
        con.commit()
        if (not data):
            congratsMsg = QMessageBox.information(self,"Congrats","MEMBER ADDED TO URBAN KINETICS",QMessageBox.Ok)
        if congratsMsg == QMessageBox.Ok:
            self.close()


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.subLayout = QFormLayout()
        self.urbanKineticslableLayout = QHBoxLayout()
        self.genderLayout = QHBoxLayout()
        self.addMemberLayout = QHBoxLayout()

        self.setLayout(self.mainLayout)

        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.subLayout)
        self.mainLayout.addStretch()

        self.urbanKineticslableLayout.addStretch()
        self.urbanKineticslableLayout.addWidget(self.urbanKineticslable)
        self.urbanKineticslableLayout.addStretch()

        self.genderLayout.addWidget(self.male)
        self.genderLayout.addWidget(self.female)

        self.addMemberLayout.addStretch()
        self.addMemberLayout.addWidget(self.addMember)
        self.addMemberLayout.addStretch()

        self.subLayout.setVerticalSpacing(15)
        self.subLayout.addRow(self.urbanKineticslableLayout)
        self.subLayout.addRow("CARD NUMBER:",self.cardnumlable)
        self.subLayout.addRow("NAME:",self.namelable)
        self.subLayout.addRow("ADDRESS:",self.address)
        self.subLayout.addRow("PHONE:",self.phone)
        self.subLayout.addRow("GENDER:",self.genderLayout)

        self.subLayout.addRow("JOINING DATE:",self.join)
        self.subLayout.addRow("TIME PERIOD:",self.timeperiod)
        self.subLayout.addRow("RENEW DATE:",self.renewal)
        self.subLayout.addRow("GYM FEES:",self.gymfee)
        self.subLayout.addRow("TRAINER NAME:",self.trainerName)
        # self.subLayout.addRow("DISCOUNT:",self.discountpercent)
        self.subLayout.addRow("TRAINER TYPE",self.trainertype)
        self.subLayout.addRow("TRAINER PRICE",self.trainerprice)
        self.subLayout.addRow("ID PROOF",self.idproof)
        self.subLayout.addRow("MODE OF PAYMENT",self.modeofpayment)
        self.subLayout.addRow(self.addMemberLayout)
        self.show()

    def closeEvent(self,event):
        self.mainWindow = UrbanKineticsMainWindow()
        


# con = mysql.connector.connect(host = "localhost",user = "root", password = "12345678", database = "urban_kinetics")
# cur = con.cursor()
# trainer_id=None

class TrainersRecord(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TRAINERS OF URBAN KINETICS")
        self.setGeometry(450,150,700,300)
        self.UI()
        self.show()

    def closeTrainersRecord(self):
        self.close()
        self.mainWindow = UrbanKineticsMainWindow()


    def UI(self):
        self.mainDesign()
        self.layouts()
        self.getTrainers()
        self.displayFirstRecord()

    def mainDesign(self):
        self.setStyleSheet("font-size:14pt;font-family:Arial Bold;")
        self.trainersList=QListWidget()
        self.trainersList.itemClicked.connect(self.singleClick)
        self.btnNew=QPushButton("New")
        self.btnNew.clicked.connect(self.addTrainer)
        self.btnUpdate=QPushButton("Update")
        self.btnUpdate.clicked.connect(self.updateTrainer)
        self.btnDelete=QPushButton("Delete")
        self.btnDelete.clicked.connect(self.deleteTrainer)
        self.btnClose=QPushButton("Close")
        self.btnClose.clicked.connect(self.closeTrainersRecord)

    def layouts(self):
        ###################Layouts###############
        self.mainLayout=QHBoxLayout()
        self.leftLayout=QFormLayout()
        self.rightMainLayout=QVBoxLayout()
        self.rightTopLayout=QHBoxLayout()
        self.rightBottomLayout=QHBoxLayout()
        #####################Adding child layouts to main layout###########
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBottomLayout)
        self.mainLayout.addLayout(self.leftLayout,40)
        self.mainLayout.addLayout(self.rightMainLayout,60)
        ###################adding wigdets to layouts#################
        self.rightTopLayout.addWidget(self.trainersList)
        self.rightBottomLayout.addWidget(self.btnNew)
        self.rightBottomLayout.addWidget(self.btnUpdate)
        self.rightBottomLayout.addWidget(self.btnDelete)
        self.rightBottomLayout.addWidget(self.btnClose)
        ##############setting main window layout#####################
        self.setLayout(self.mainLayout)

    def addTrainer(self):
        self.newTrainer=AddTrainer()
        self.close()
    def getTrainers(self):
        query="SELECT * FROM trainers"
        cur.execute(query)
        trainers=cur.fetchall()
        for trainer in trainers:
            self.trainersList.addItem(str(trainer[0])+"-"+trainer[1]+" "+trainer[2]+" "+trainer[3]+" "+str(trainer[4]))

    def displayFirstRecord(self):
        query="SELECT * FROM trainers ORDER BY sr_no ASC LIMIT 1"
        cur.execute(query)
        trainer=cur.fetchone()

        name=QLabel(trainer[1])
        experience=QLabel(trainer[2])
        speciality=QLabel(trainer[3])
        age=QLabel(str(trainer[4]))

        self.leftLayout.setVerticalSpacing(20)
        self.leftLayout.addRow("Name: ",name)
        self.leftLayout.addRow("Experience :",experience)
        self.leftLayout.addRow("Speciality :",speciality)
        self.leftLayout.addRow("Age :",age)
        

    def singleClick(self):
        for i in reversed(range(self.leftLayout.count())):
            widget=self.leftLayout.takeAt(i).widget()

            if widget is not None:
                widget.deleteLater()

        trainer=self.trainersList.currentItem().text()
        id=trainer.split("-")[0]
        query=(f"SELECT * FROM trainers WHERE sr_no={id}")
        cur.execute(query)#single item tuple=(1,)
        trainer=cur.fetchone()#single item tuple=(1,)
    
        name = QLabel(trainer[1])
        experience = QLabel(trainer[2])
        speciality = QLabel(trainer[3])
        age = QLabel(str(trainer[4]))

        self.leftLayout.setVerticalSpacing(20)
    
        self.leftLayout.addRow("Name: ", name)
        self.leftLayout.addRow("Experience :", experience)
        self.leftLayout.addRow("Speciality :", speciality)
        self.leftLayout.addRow("Age :", age)


    def deleteTrainer(self):
        if self.trainersList.selectedItems():
            trainer=self.trainersList.currentItem().text()
            id = trainer.split("-")[0]
            mbox=QMessageBox.question(self,"Warning","Are you sure to delete this Trainer?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if mbox == QMessageBox.Yes:

                try:
                    query=f"DELETE FROM Trainers WHERE sr_no={id}"
                    cur.execute(query)
                    con.commit()
                    QMessageBox.information(self,"Info!!!","Trainer has been deleted")
                    self.close()
                    self.trainersRecord=TrainersRecord()

                except:
                    QMessageBox.critical(self,"Warning!!!","Trainer has not been deleted")


        else:
            QMessageBox.critical(self, "Warning!!!", "Please select a Trainer to delete")


    def updateTrainer(self):
        global trainer_id
        if self.trainersList.selectedItems():
            trainer = self.trainersList.currentItem().text()
            trainer_id=trainer.split("-")[0]
            self.updateWindow=UpdateTrainer()
            self.close()

        else:
            QMessageBox.information(self, "Warning!!!", "Please select a Trainer to update")



class UpdateTrainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Trainer")
        self.setGeometry(450,150,600,250)
        self.UI()
        self.show()

    def UI(self):

        self.getTrainer()
        self.mainDesign()
        self.layouts()

    def closeEvent(self, event):
        self.trainersRecord = TrainersRecord()

    def getTrainer(self):
        global trainer_id
        query=f"SELECT * FROM trainers WHERE sr_no={trainer_id}"
        cur.execute(query)
        trainer=cur.fetchone()
        print(trainer)
        self.sr_no=trainer[0]
        self.name=trainer[1]
        self.experience=trainer[2]
        self.speciality=trainer[3]
        self.age=trainer[4]

    def mainDesign(self):
        ################Top Layout widgets#######################
        self.setStyleSheet("background-color:white;font-size:14pt;font-family:Times")
        self.title = QLabel("Update Trainer's Information")
        self.title.setStyleSheet('font-size: 24pt;font-family:Arial Bold;')

        ###################Bottom Layout Widgets#####################
        self.sr_noLbl = QLabel("Serial Number :")
        self.sr_noEntry = QLineEdit()
        self.sr_noEntry.setText(str(self.sr_no))
        self.nameLbl = QLabel("Name :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.name)
        self.experienceLbl = QLabel("Experience :")
        self.experienceEntry = QLineEdit()
        self.experienceEntry.setText(self.experience)
        self.specialityLbl = QLabel("Speciality :")
        self.specialityEntry = QLineEdit()
        self.specialityEntry.setText(self.speciality)
        self.ageLbl = QLabel("Age :")
        self.ageEntry = QLineEdit()
        self.ageEntry.setText(str(self.age))

        self.addButton = QPushButton("Update")
        self.addButton.setStyleSheet("background-color:orange;font-size:10pt")
        self.addButton.clicked.connect(self.updateTrainer)

    def layouts(self):
        ##################creating main layouts##########
        self.mainLayout = QVBoxLayout()

        self.updateFormLayout = QFormLayout()

        ##########adding child layout to main layout##############
        self.mainLayout.addLayout(self.updateFormLayout)

        ##################adding wigdets to layouts##############
        ###########bottom layout#################
        self.updateFormLayout.addRow(self.sr_noLbl, self.sr_noEntry)
        self.updateFormLayout.addRow(self.nameLbl, self.nameEntry)
        self.updateFormLayout.addRow(self.experienceLbl, self.experienceEntry)
        self.updateFormLayout.addRow(self.specialityLbl, self.specialityEntry)
        self.updateFormLayout.addRow(self.ageLbl, self.ageEntry)
        self.updateFormLayout.addRow("", self.addButton)

        ###########setting main layout for window##################
        self.setLayout(self.mainLayout)




    def updateTrainer(self):
        global trainer_id
        sr_no=self.sr_noEntry.text()
        name=self.nameEntry.text()
        experience=self.experienceEntry.text()
        speciality=self.specialityEntry.text()
        age=self.ageEntry.text()
        
        if (name and experience and speciality !=""):
            try:
                if sr_no==trainer_id:
                    query=f"UPDATE trainers set sr_no = {sr_no}, name ='{name}',\
                        experience='{experience}',speciality='{speciality}',age={age} WHERE sr_no={trainer_id}"

                    cur.execute(query)
                    con.commit()

                else:
                    query = f"delete from trainers where sr_no={trainer_id}"
                    cur.execute(query)
                    con.commit()

                    query=f"INSERT INTO trainers VALUE({sr_no},'{name}','{experience}','{speciality}',{age})"
                    cur.execute(query)
                    con.commit()



                QMessageBox.information(self,"Success","Trainer has been updated Successfully!")
                self.close()
                self.trainersRecord=TrainersRecord()
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    QMessageBox.critical(self, "Warning", "Serial Number Already Exists!\nPlease Change The Serial Number")
                elif err.errno == 1054 :
                    QMessageBox.critical(self, "Warning", "Serial Number and Age of Trainer Should be Integer!")

                else: 
                    QMessageBox.critical(self, "Warning", "Trainer has not been updated!\nInternal Error")

        else:
            QMessageBox.critical(self, "Warning", "Trainer can not be empty!")



class AddTrainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add A New Trainer")
        self.setGeometry(450,150,600,250)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def closeEvent(self, event):
        self.trainersRecord=TrainersRecord()

    def mainDesign(self):
        ################Top Layout widgets#######################
        self.setStyleSheet("background-color:white;font-size:14pt;font-family:Times")
        self.title=QLabel("Add Trainer")
        self.title.setStyleSheet('font-size: 24pt;font-family:Arial Bold;')

        ###################Bottom Layout Widgets#####################
        self.sr_noLbl=QLabel("Serial Number: ")
        self.sr_noEntry = QLineEdit()
        self.sr_noEntry.setPlaceholderText("Enter Trainer Sr. No. OR Leave blank for Auto Generation")
        self.nameLbl=QLabel("Name :")
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Trainer Name")
        self.experienceLbl = QLabel("Experience :")
        self.experienceEntry = QLineEdit()
        self.experienceEntry.setPlaceholderText("Enter Trainer Experience")
        self.specialityLbl = QLabel("Speciality :")
        self.specialityEntry = QLineEdit()
        self.specialityEntry.setPlaceholderText("Enter Trainer Speciality")
        self.ageLbl = QLabel("Age :")
        self.ageEntry = QLineEdit()
        self.ageEntry.setPlaceholderText("Enter Trainer Age")


        self.addButton=QPushButton("Add")
        self.addButton.setStyleSheet("background-color:orange;font-size:10pt")
        self.addButton.clicked.connect(self.addTrainer)

    def layouts(self):
        ##################creating main layouts##########
        self.mainLayout=QVBoxLayout()
    
        self.addFormLayout=QFormLayout()

        ##########adding child layouts to main layout##############
  
        self.mainLayout.addLayout(self.addFormLayout)

        ##################adding wigdets to layouts##############
                ###########bottom layout#################

        self.addFormLayout.addRow(self.sr_noLbl,self.sr_noEntry)
        self.addFormLayout.addRow(self.nameLbl,self.nameEntry)
        self.addFormLayout.addRow(self.experienceLbl,self.experienceEntry)
        self.addFormLayout.addRow(self.specialityLbl,self.specialityEntry)
        self.addFormLayout.addRow(self.ageLbl,self.ageEntry)
    
        self.addFormLayout.addRow("",self.addButton)

        ###########setting main layout for window##################
        self.setLayout(self.mainLayout)




    def addTrainer(self):
        sr_no=self.sr_noEntry.text()
        name=self.nameEntry.text()
        experience=self.experienceEntry.text()
        speciality=self.specialityEntry.text()
        age=self.ageEntry.text()
        if len(sr_no)==0:
            sr_no = "NULL"

        if (name and experience and speciality !=""):
            try:
                query=f"INSERT INTO trainers VALUE({sr_no},'{name}',\
                    '{experience}','{speciality}',{age})"
                cur.execute(query)
                con.commit()
                QMessageBox.information(self,"Success","Trainer has been added Successfully")
                self.close()
                self.trainersRecord=TrainersRecord()
            except mysql.connector.Error as err:

                if err.errno == 1062:
                    QMessageBox.critical(self, "Warning", "Serial Number Already Exists!\nPlease Change The Serial Number")
                elif err.errno == 1054 :
                    QMessageBox.critical(self, "Warning", "Serial Number and Age of Trainer Should be Integer!")

                else:
                    QMessageBox.critical(self, "Warning", "Trainer has not been added!\nInternal Error")

        else:
            QMessageBox.critical(self, "Warning", "Fields can not be empty")



class UsersRecord(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MEMBERS OF URBAN KINETICS")
        self.setGeometry(450,150,700,300)
        self.UI()
        self.show()

    def closeEvent(self,event):
        self.urbanKinetics = UrbanKineticsMainWindow()


    def UI(self):
        self.mainDesign()
        self.layouts()
        self.getUsers()
        self.displayFirstRecord()

    def mainDesign(self):
        self.setStyleSheet("font-size:14pt;font-family:Arial Bold;")
        self.usersList=QListWidget()
        self.usersList.itemClicked.connect(self.singleClick)
    
        self.btnClose=QPushButton("Close")
        self.btnClose.clicked.connect(self.closeUsersRecord)

    def layouts(self):
        ###################Layouts###############
        self.mainLayout=QHBoxLayout()
        self.leftLayout=QFormLayout()
        self.rightMainLayout=QVBoxLayout()
        self.rightTopLayout=QHBoxLayout()
        self.rightBottomLayout=QHBoxLayout()
        #####################Adding child layouts to main layout###########
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBottomLayout)
        self.mainLayout.addLayout(self.leftLayout,40)
        self.mainLayout.addLayout(self.rightMainLayout,60)
        ###################adding wigdets to layouts#################
        self.rightTopLayout.addWidget(self.usersList)
        self.rightBottomLayout.addWidget(self.btnClose)
        ##############setting main window layout#####################
        self.setLayout(self.mainLayout)

    def getUsers(self):
        query="SELECT * FROM users"
        cur.execute(query)
        users=cur.fetchall()
        if users:
            for user in users:
                self.usersList.addItem(str(user[0])+"-"+user[1]+" "+str(user[2])+" "+user[3]+" "+str(user[4]+" "+str(user[5])+" "+user[6]+" "+str(user[7])+" "+str(user[8])+" "+user[9]+" "+user[10]+" "+str(user[11])+" "+user[12]+" "+user[13]))

    def displayFirstRecord(self):
        query="SELECT * FROM users ORDER BY card_num ASC LIMIT 1"
        cur.execute(query)
        user=cur.fetchone()
        if user:
            card_num = QLabel(str(user[0]))
            name = QLabel(user[1])
            phone = QLabel(str(user[2]))
            address = QLabel(user[3])
            gender = QLabel(str(user[4]))
            joining_date=QLabel(str(user[5]))
            time_period=QLabel(user[6])
            renewal_date=QLabel(str(user[7]))
            gym_price=QLabel(str(user[8]))
            trainer_name=QLabel(user[9])
            trainer_type=QLabel(user[10])
            trainer_price=QLabel(str(user[11]))
            # discount_percent=self.discountpercent.text()
            mode_of_payment=QLabel(user[12])
            id_proof=QLabel(user[13])

            self.leftLayout.setVerticalSpacing(20)

            self.leftLayout.addRow("CARD NUMBER:",card_num)
            self.leftLayout.addRow("NAME:",name)
            self.leftLayout.addRow("ADDRESS:",address)
            self.leftLayout.addRow("PHONE:",phone)
            self.leftLayout.addRow("GENDER:",gender)

            self.leftLayout.addRow("JOINING DATE:",joining_date)
            self.leftLayout.addRow("TIME PERIOD:",time_period)
            self.leftLayout.addRow("RENEW DATE:",renewal_date)
            self.leftLayout.addRow("GYM FEES:",gym_price)
            self.leftLayout.addRow("TRAINER NAME:",trainer_name)

            self.leftLayout.addRow("TRAINER TYPE",trainer_type)
            self.leftLayout.addRow("TRAINER PRICE",trainer_price)
            self.leftLayout.addRow("ID PROOF",id_proof)
            self.leftLayout.addRow("MODE OF PAYMENT",mode_of_payment)

        else:
            QMessageBox.information(self,"NO MEMBER EXIST IN RECORD","Currently There is No Member\nAdded To Record\nPlease Add The Members First!")

    def singleClick(self):
        for i in reversed(range(self.leftLayout.count())):
            widget=self.leftLayout.takeAt(i).widget()

            if widget is not None:
                widget.deleteLater()

        user=self.usersList.currentItem().text()
        id=user.split("-")[0]
        query=(f"SELECT * FROM users WHERE card_num={id}")
        cur.execute(query)#single item tuple=(1,)
        user=cur.fetchone()#single item tuple=(1,)
    
        card_num = QLabel(str(user[0]))
        name = QLabel(user[1])
        phone = QLabel(str(user[2]))
        address = QLabel(user[3])
        gender = QLabel(str(user[4]))
        joining_date=QLabel(str(user[5]))
        time_period=QLabel(user[6])
        renewal_date=QLabel(str(user[7]))
        gym_price=QLabel(str(user[8]))
        trainer_name=QLabel(user[9])
        trainer_type=QLabel(user[10])
        trainer_price=QLabel(str(user[11]))
        mode_of_payment=QLabel(user[12])
        id_proof=QLabel(user[13])

        self.leftLayout.setVerticalSpacing(20)
        self.leftLayout.addRow("CARD NUMBER:",card_num)
        self.leftLayout.addRow("NAME:",name)
        self.leftLayout.addRow("ADDRESS:",address)
        self.leftLayout.addRow("PHONE:",phone)
        self.leftLayout.addRow("GENDER:",gender)

        self.leftLayout.addRow("JOINING DATE:",joining_date)
        self.leftLayout.addRow("TIME PERIOD:",time_period)
        self.leftLayout.addRow("RENEW DATE:",renewal_date)
        self.leftLayout.addRow("GYM FEES:",gym_price)
        self.leftLayout.addRow("TRAINER NAME:",trainer_name)

        self.leftLayout.addRow("TRAINER TYPE:",trainer_type)
        self.leftLayout.addRow("TRAINER PRICE:",trainer_price)
        self.leftLayout.addRow("ID PROOF:",id_proof)
        self.leftLayout.addRow("MODE OF PAYMENT:",mode_of_payment)  


    def closeUsersRecord(self):
        self.close()

class ShowBalance(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(300, 250)
        mainLayout = QVBoxLayout()
        query=(f"select name, gym_price from {usersTableName}")
        hey=cur.execute(query)
        y=cur.fetchall()
        print(type(y))

        model = QStandardItemModel(len(y), 2)
        model.setHorizontalHeaderLabels(['Members','Gym Fees'])


        # model.setHorizontalHeaderLabels(['Gym fess'])

        # for i in y:
        #     z=("{}".format(i[0][:20]))
        for row, user in enumerate(y):
            item = QStandardItem(user[0])
            model.setItem(row, 0, item)
            item = QStandardItem(str(user[1]))
            model.setItem(row,1,item)
            


        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)

        search_field = QLineEdit()          
        search_field.setStyleSheet('font-size: 16px; height: 25px;')
        search_field.textChanged.connect(filter_proxy_model.setFilterRegExp)
        mainLayout.addWidget(search_field)

        table = QTableView()
        table.setStyleSheet('font-size: 16px;')
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setModel(filter_proxy_model)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)
        self.show()

    def closeEvent(self,event):
        self.urbanKinetics=UrbanKineticsMainWindow()

def main():
    global mySqlPassword
    App = QApplication(sys.argv)
    start_application = UserNamePassLogin()
    sys.exit(App.exec_())      


if __name__ == "__main__":
    main()