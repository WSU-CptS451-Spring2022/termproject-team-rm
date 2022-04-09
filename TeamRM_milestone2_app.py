import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "D:\Masters WSU\Database Systems\Term Project\Milestone2App.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class milestone2(QMainWindow):
    def __init__(self):
        super(milestone2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentTextChanged.connect(self.stateChanged)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.zipList.itemSelectionChanged.connect(self.zipchanged)



    def executeQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='milestone2db' user ='postgres' host='localhost' password='0722'")
        except:
            print("Unable to connect")
        cur = conn.cursor()
        cur.execute(sql_str)
        result = cur.fetchall()
        conn.close()
        return result

    def loadStateList(self):
        self.ui.stateList.clear()
        sql_str = "SELECT DISTINCT business_state FROM business ORDER BY business_state;"
        try:
            results = self.executeQuery(sql_str)
            for row in results:
                self.ui.stateList.addItem(row[0])
        except:
            print("Query Failed")
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    def stateChanged(self):
        self.ui.cityList.clear()
        self.ui.zipList.clear()

        if (self.ui.stateList.currentIndex() >= 0):
            state = self.ui.stateList.currentText()
            sql_str = "SELECT distinct city FROM business WHERE business_state ='" + state + "' ORDER BY city;"
            sql_str1 = "SELECT distinct postalcode FROM business WHERE business_state ='" + state + "' ORDER BY postalcode;"
            sql_str2 = "SELECT distinct category_name FROM business_category;"


            try:
                results = self.executeQuery(sql_str)
                results1 = self.executeQuery(sql_str1)
                results2 = self.executeQuery(sql_str2)
                for row in results:
                    self.ui.cityList.addItem(row[0])
                for row in results1:
                    self.ui.zipList.addItem(row[0])
                for row in results2:
                        self.ui.catList.addItem(row[0])
            except:
                print("Query Failed!")
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT business_name, city, business_state, postalcode FROM business WHERE business_state ='" + state + "' ORDER BY business_name;"
            try:
                results = self.executeQuery(sql_str)
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State', 'Zip Code'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(1, 70)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1

            except:
                print("Query Failed!!")

    def cityChanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT business_name, city,business_state, postalcode FROM business WHERE city ='" + city + "' AND business_state= '" + state +"'ORDER BY business_name;"


            results = self.executeQuery(sql_str)

            try:
                results = self.executeQuery(sql_str)

                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State','Zip Code'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(1, 70)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                    currentRowCount += 1

            except:
                print("Query Failed!!")

    def zipchanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.zipList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT business_name, city,business_state, postalcode FROM business WHERE postalcode ='" + zip + "' AND business_state= '" + state + "'ORDER BY business_name;"
            results = self.executeQuery(sql_str)
            try:
                results = self.executeQuery(sql_str)
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(
                    ['Business Name', 'City', 'State', 'Zip Code'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(1, 70)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount,
                                                      QTableWidgetItem(row[colCount]))
                    currentRowCount += 1
            except:
                print("Query Failed!!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())