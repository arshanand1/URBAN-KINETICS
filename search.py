import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QTableView, QHeaderView, QVBoxLayout
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class search(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 1000)
        mainLayout = QVBoxLayout()
        import mysql.connector
        con=mysql.connector.connect(host='localhost',user='root',password='anand',database='urban_kinetics')
        cur=con.cursor()
        query=("select name, gym_price from users")
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

app = QApplication(sys.argv)
demo = search()
demo.show()
sys.exit(app.exec_())       
