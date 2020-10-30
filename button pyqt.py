import sys
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,500,500)
        self.setWindowTitle("first window")
        self.UI()

        # self.show()

    def UI(self):
        self.text = QLabel("Hello", self)
        self.text.move(250,250)
        enterBtn = QPushButton("ENTER",self)
        enterBtn.move(200,300)
        enterBtn.clicked.connect(self.enterFunc)

        exitBtn = QPushButton("EXIT",self)
        exitBtn.move(300,300)
        exitBtn.clicked.connect(self.exitFunc)
        self.show()

    def enterFunc(self):
        self.text.setText("ENTER PRESSED")
        self.text.resize(150,10)

    def exitFunc(self):
        self.text.setText("EXIT PRESSED")
        self.text.resize(150,10)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())