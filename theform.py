from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import *
import sys
import mysql.connector

class loginform(QWidget):


    def __init__(self):
        super().__init__()
    
        self.setWindowTitle(" ENTER YOUR DETAILS ")
        self.setGeometry(200,200,350,200)
        self.setStyleSheet("background-color:rgb(170, 170, 255);font-family: Comic Sans;font-size:14pt;")
        self.mainform()
        self.layouts()


    def mainform(self):
        self.lable = QLabel("URBAN KINETICS")
        

        self.namelable = QLineEdit()
        self.namelable.setPlaceholderText("ENTER NAME")

        self.address = QLineEdit()
        self.address.setPlaceholderText("ENTER ADDRESS")

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("ENTER PHONE NUMBER")

        self.male = QRadioButton("MALE")
        self.female = QRadioButton("FEMALE")

        self.join = QLineEdit()
        self.join.setPlaceholderText("ENTER JOINING DATE")

        options=['One Day Pass', '12 Months', '6 Months', '3 Months', '1 Month']
        self.timeperiod = QComboBox()
        self.timeperiod.addItems(options)
        

        self.renewal = QLineEdit()
        self.renewal.setPlaceholderText("ENTER LAST DATE PACKAGE")

        self.gymfee = QLineEdit()
        self.gymfee.setPlaceholderText("ENTER GYM FEES")

        self.discountpercent = QLineEdit()
        self.discountpercent.setPlaceholderText("ENTER DISCOUNT PERCENT")

        traineroption=['REGULAR','PERSONAL']
        self.trainertype = QComboBox()
        self.trainertype.setPlaceholderText("CHOOSE")
        self.trainertype.addItems(traineroption)

        self.trainerprice = QLineEdit()
        self.trainerprice.setPlaceholderText("ENTER TRAINER FEE")

        self.idproof = QLineEdit()
        self.idproof.setPlaceholderText("ID PROOF PROVIDED")

        self.modeofpayment = QLineEdit()
        self.modeofpayment.setPlaceholderText("PAYMENT MADE THROUGH")

        self.signup = QPushButton("SIGN UP")

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.subLayout = QFormLayout()

        self.setLayout(self.mainLayout)

        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.subLayout)
        self.mainLayout.addStretch()

        self.subLayout.setVerticalSpacing(15)
        self.subLayout.addRow("",self.lable)
        self.subLayout.addRow("NAME:",self.namelable)
        self.subLayout.addRow("ADDRESS:",self.address)
        self.subLayout.addRow("PHONE:",self.phone)
        self.subLayout.addRow("GENDER:",self.male)

        self.subLayout.addRow("JOINING DATE:",self.join)
        self.subLayout.addRow("TIME PERIOD:",self.timeperiod)
        self.subLayout.addRow("RENEW DATE:",self.renewal)
        self.subLayout.addRow("GYM FEES:",self.gymfee)
        self.subLayout.addRow("DISCOUNT:",self.discountpercent)
        self.subLayout.addRow("TRAINER TYPE",self.trainertype)
        self.subLayout.addRow("TRAINER PRICE",self.trainerprice)
        self.subLayout.addRow("ID PROOF",self.idproof)
        self.subLayout.addRow("MODE OF PAYMENT",self.modeofpayment)
        self.subLayout.addRow("",self.signup)
        self.show()
        

    

    # def signup(self):
    #     con=mysql.connector.connect(host="localhost",user="root",password="anand",database="urban_kinetics")
    #     cur=con.cursor()
    #     query="insert into users(card_num,name,phn,address,gender,joining_date,time_period,renewal_date,gym_price,trainer_type,trainer_price,discount_percent,mode_of_payment,id_proof) \
    #     values (131,'%s',%s,'%s','%s','%s','%s','%s',%s,'%s',%s,%s,'%s','%s')"%(name,phn,address,gender,join,till,renew,fees,ttype,tprice,disc,mop,idproof)
    #     data=cur.execute(query)
    #     con.commit()
    #     if (not data):
    #         self.messagebox("Congrats","You are now a member of URBAN KINETICS")
    #     cur.close()
    #     con.close()





def main():
    app= QApplication(sys.argv)
    demo = loginform()
    ui=loginform()
    # ui.setupui()
    # demo.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
