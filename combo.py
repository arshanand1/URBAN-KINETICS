import sys
from PyQt5.QtWidgets import QtApplication, QtWidget, QtComboBox, QtPushButton
 
class ComboBoxDemo(QtWidget):
    def __init__(self):
        super().__init__()
 
        lstCompany = ['One Day Pass', '12 Months', '6 Months', '3 Months', '1 Month']
 
        self.comboBox = QtComboBox(self)
        self.comboBox.setGeometry(50, 50, 400, 35)
        self.comboBox.addItems(lstCompany)
 
        self.btn = QtPushButton('Click', self)
        self.btn.setGeometry(170, 120, 120, 35)
        self.btn.clicked.connect(self.getComboValue)
 
    def getComboValue(self):
        print((self.comboBox.currentText(), self.comboBox.currentIndex()))
 
 
app = QtApplication(sys.argv)
 
demo = ComboBoxDemo()
demo.show()
 
sys.exit(app.exec_())