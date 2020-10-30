import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton
 
class ComboBoxDemo(QWidget):
    def __init__(self):
        super().__init__()
 
        lstCompany = ['One Day Pass', '12 months', '6 months', '3 months', '1 month']

        
 
        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(160, 290, 104, 31)
        self.comboBox.addItems(lstCompany)
 
        self.btn = QPushButton('Click', self)
        self.btn.setGeometry(170, 120, 120, 35)
        self.btn.clicked.connect(self.getComboValue)
 
    def getComboValue(self):
        print(self.comboBox.currentText())

        if self.comboBox.currentIndex()==0:
            print()
 
app = QApplication(sys.argv)
 
demo = ComboBoxDemo()
demo.show()
demo.getComboValue() 

sys.exit(app.exec_())

