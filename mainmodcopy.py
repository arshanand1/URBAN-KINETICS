from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtGui import QFont
import sys,os
import mysql.connector
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem


con = mysql.connector.connect(host = "localhost",user = "root", password = "anand", database = "urban_kinetics")
cur = con.cursor()
# defaultImg="person.png"
trainer_id=None

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TRAINERS OF URBAN KINETICS")
        self.setGeometry(450,150,750,600)
        self.UI()
        self.show()


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
        self.leftLayout.addRow("experience :",experience)
        self.leftLayout.addRow("speciality :",speciality)
        self.leftLayout.addRow("age :",age)
        

    def singleClick(self):
        for i in reversed(range(self.leftLayout.count())):
            widget=self.leftLayout.takeAt(i).widget()

            if widget is not None:
                widget.deleteLater()

        trainer=self.trainersList.currentItem().text()
        id=trainer.split("-")[0]
        query=(f"SELECT * FROM trainers WHERE sr_no={id}")
        cur.execute(query)#single item tuple=(1,)
        person=cur.fetchone()#single item tuple=(1,)
    
        name = QLabel(person[1])
        experience = QLabel(person[2])
        speciality = QLabel(person[3])
        age = QLabel(str(person[4]))

        self.leftLayout.setVerticalSpacing(20)
    
        self.leftLayout.addRow("Name: ", name)
        self.leftLayout.addRow("experience :", experience)
        self.leftLayout.addRow("speciality :", speciality)
        self.leftLayout.addRow("age :", age)


    def deleteTrainer(self):
        if self.trainersList.selectedItems():
            person=self.trainersList.currentItem().text()
            id = person.split("-")[0]
            mbox=QMessageBox.question(self,"Warning","Are you sure to delete this Trainer?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if mbox == QMessageBox.Yes:

                try:
                    query=f"DELETE FROM Trainers WHERE id={id}"
                    cur.execute(query)
                    con.commit()
                    QMessageBox.information(self,"Info!!!","Trainer has been deleted")
                    self.close()
                    self.main=Main()

                except:
                    QMessageBox.critical(self,"Warning!!!","Person has not been deleted")


        else:
            QMessageBox.critical(self, "Warning!!!", "Please select a person to delete")


    def updateTrainer(self):
        global trainer_id
        if self.trainersList.selectedItems():
            person = self.trainersList.currentItem().text()
            trainer_id=person.split("-")[0]
            self.updateWindow=UpdateTrainer()
            self.close()

        else:
            QMessageBox.information(self, "Warning!!!", "Please select a person to update")



class UpdateTrainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Trainer")
        self.setGeometry(450,150,350,600)
        self.UI()
        self.show()

    def UI(self):

        self.getPerson()
        self.mainDesign()
        self.layouts()

    def closeEvent(self, event):
        self.main = Main()

    def getPerson(self):
        global trainer_id
        query=f"SELECT * FROM Trainers WHERE id={trainer_id}"
        trainer=cur.execute(query).fetchone()
        print(trainer)
        self.name=trainer[1]
        self.experience=trainer[2]
        self.speciality=Trainer[3]
        self.age=trainer[4]

    def mainDesign(self):
        ################Top Layout widgets#######################
        self.setStyleSheet("background-color:white;font-size:14pt;font-family:Times")
        self.title = QLabel("Update Trainer's Information")
        self.title.setStyleSheet('font-size: 24pt;font-family:Arial Bold;')

        ###################Bottom Layout Widgets#####################
        self.nameLbl = QLabel("Name :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.name)
        self.experienceLbl = QLabel("experience :")
        self.experienceEntry = QLineEdit()
        self.experienceEntry.setText(self.experience)
        self.specialityLbl = QLabel("speciality :")
        self.specialityEntry = QLineEdit()
        self.specialityEntry.setText(self.speciality)
        self.ageLbl = QLabel("age :")
        self.ageEntry = QLineEdit()
        self.ageEntry.setText(self.age)

        # self.imgLbl = QLabel("Picture: ")
        # self.imgButton = QPushButton("Browse")
        # self.imgButton.setStyleSheet("background-color:orange;font-size:10pt")
        # self.imgButton.clicked.connect(self.uploadImage)
        # self.addressLbl = QLabel("Address: ")
        # self.addressEditor = QTextEdit()
        # self.addressEditor.setText(self.address)

        self.addButton = QPushButton("Update")
        self.addButton.setStyleSheet("background-color:orange;font-size:10pt")
        self.addButton.clicked.connect(self.updateTrainer)

    def layouts(self):
        ##################creating main layouts##########
        self.mainLayout = QVBoxLayout()
        # self.topLayout = QVBoxLayout()
        self.updateFormLayout = QFormLayout()

        ##########adding child layouts to main layout##############
        # self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        ##################adding wigdets to layouts##############
        ##############top layout################
        # self.topLayout.addStretch()
        # self.topLayout.addWidget(self.title)
        # self.topLayout.addWidget(self.imgAdd)
        # self.topLayout.addStretch()
        # self.topLayout.setContentsMargins(110, 20, 10, 30)  # left,top,right,bottom
        ###########bottom layout#################
        self.updateFormLayout.addRow(self.nameLbl, self.nameEntry)
        self.updateFormLayout.addRow(self.experienceLbl, self.experienceEntry)
        self.updateFormLayout.addRow(self.specialityLbl, self.specialityEntry)
        self.updateFormLayout.addRow(self.ageLbl, self.ageEntry)
        self.updateFormLayout.addRow("", self.addButton)

        ###########setting main layout for window##################
        self.setLayout(self.mainLayout)


    # def uploadImage(self):
    #     global defaultImg
    #     size =(128,128)
    #     self.fileName,ok =QFileDialog.getOpenFileName(self,'Upload Image','','Image Files (*.jpg *.png)')

    #     if ok:

    #         defaultImg=os.path.basename(self.fileName)
    #         img=Image.open(self.fileName)
    #         img=img.resize(size)
    #         img.save("images/{}".format(defaultImg))



    def updateTrainer(self):
        global trainer_id
        name=self.nameEntry.text()
        experience=self.experienceEntry.text()
        speciality=self.specialityEntry.text()
        age=self.ageEntry.text()
        
        if (name and experience and speciality !=""):
            try:
                query=f"UPDATE trainers set name ={name}, experience={experience}, speciality={speciality},age={age} WHERE id={trainer_id}"

                cur.execute(query)
                con.commit()
                QMessageBox.information(self,"Success","Trainer has been updated Successfully!")
                self.close()
                self.main=Main()
            except:
                QMessageBox.critical(self, "Warning", "Person has not been updated!\nInternal Error")

        else:
            QMessageBox.critical(self, "Warning", "Fields can not be empty!")



class AddTrainer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add A New Trainer")
        self.setGeometry(450,150,350,600)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()

    def closeEvent(self, event):
        self.main=Main()

    def mainDesign(self):
        ################Top Layout widgets#######################
        self.setStyleSheet("background-color:white;font-size:14pt;font-family:Times")
        self.title=QLabel("Add Person")
        self.title.setStyleSheet('font-size: 24pt;font-family:Arial Bold;')
        # self.imgAdd=QLabel()
        # self.imgAdd.setPixmap(QPixmap("icons/person.png"))
        ###################Bottom Layout Widgets#####################
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

        # self.imgLbl=QLabel("Picture: ")
        # self.imgButton=QPushButton("Browse")
        # self.imgButton.setStyleSheet("background-color:orange;font-size:10pt")
        # self.imgButton.clicked.connect(self.uploadImage)
        # self.addressLbl=QLabel("Address: ")
        # self.addressEditor=QTextEdit()

        self.addButton=QPushButton("Add")
        self.addButton.setStyleSheet("background-color:orange;font-size:10pt")
        self.addButton.clicked.connect(self.addTrainer)

    def layouts(self):
        ##################creating main layouts##########
        self.mainLayout=QVBoxLayout()
        # self.topLayout=QVBoxLayout()
        self.addFormLayout=QFormLayout()

        ##########adding child layouts to main layout##############
        # self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.addFormLayout)

        ##################adding wigdets to layouts##############
                ##############top layout################

        # self.topLayout.addStretch()
        # self.topLayout.addWidget(self.title)
        # self.topLayout.addWidget(self.imgAdd)
        # self.topLayout.addStretch()
        # self.topLayout.setContentsMargins(110,20,10,30) #left,top,right,bottom
                ###########bottom layout#################

        self.addFormLayout.addRow(self.nameLbl,self.nameEntry)
        self.addFormLayout.addRow(self.experienceLbl,self.experienceEntry)
        self.addFormLayout.addRow(self.specialityLbl,self.specialityEntry)
        self.addFormLayout.addRow(self.ageLbl,self.ageEntry)
    
        self.addFormLayout.addRow("",self.addButton)

        ###########setting main layout for window##################
        self.setLayout(self.mainLayout)

    # def uploadImage(self):
    #     global defaultImg
    #     size =(128,128)
    #     self.fileName,ok =QFileDialog.getOpenFileName(self,'Upload Image','','Image Files (*.jpg *.png)')

    #     if ok:

    #         defaultImg=os.path.basename(self.fileName)
    #         img=Image.open(self.fileName)
    #         img=img.resize(size)
    #         img.save("images/{}".format(defaultImg))



    def addTrainer(self):
        name=self.nameEntry.text()
        experience=self.experienceEntry.text()
        speciality=self.specialityEntry.text()
        age=self.ageEntry.text()

        if (name and experience and speciality and age !=""):
            # try:
            query="insert into trainers(sr_no,name,experience,speciality,age) values (1112,'%s','%s','%s',%s)" \
                %(name,experience,speciality,age)

            data=cur.execute(query)
            con.commit()
            QMessageBox.information(self,"Success","Trainer has been added Successfully")
            self.close()
            self.main=Main()
            # except:
            # QMessageBox.critical(self, "Warning", "Person has not been added!\nInternal Error")

        else:
            QMessageBox.critical(self, "Warning", "Fields can not be empty")

    def searchtrainer():
        # class search(QWidget):
        #     def __init__(self):
        #         super().__init__()
        #         self.resize(1200, 1000)

        mainLayout = QVBoxLayout()
        import mysql.connector
        con=mysql.connector.connect(host='localhost',user='root',password='anand',database='urban_kinetics')
        cur=con.cursor()
        query=("select name from trainers")
        hey=cur.execute(query)
        y=cur.fetchall()
        print(type(y))
        

        model = QStandardItemModel(len(y), 1)
        model.setHorizontalHeaderLabels(['Members'])

        # for i in y:
        #     z=("{}".format(i[0][:20]))
        for row, user in enumerate(y):
            item = QStandardItem(str(user[:6]).strip("()',"))
            model.setItem(row, 0, item)
            


        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(0)

        search_field = QLineEdit()          
        search_field.setStyleSheet('font-size: 35px; height: 60px;')
        search_field.textChanged.connect(filter_proxy_model.setFilterRegExp)
        mainLayout.addWidget(search_field)

        table = QTableView()
        table.setStyleSheet('font-size: 35px;')
        table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setModel(filter_proxy_model)
        mainLayout.addWidget(table)

        self.setLayout(mainLayout)
        self.show()
        self.main=Main()

# app = QApplication(sys.argv)
# demo = search()
# demo.show()
# sys.exit(app.exec_())       



def main():
    APP=QApplication(sys.argv)
    window=Main()
    sys.exit(APP.exec_())
if __name__ == '__main__':
    main()