import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QAbstractItemView, QLabel, QPushButton
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import psycopg2

qtCreatorFile = "D:\Masters WSU\Database Systems\Term Project\Finalapp.ui" # Enter file here.

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
        self.ui.catList.currentTextChanged.connect(self.catchanged)
        self.ui.businessTable.itemSelectionChanged.connect(self.displayBusinessDetails)
        self.ui.attList.currentTextChanged.connect(self.attchanged)
        self.ui.searchButton.clicked.connect(self.search_button_pressed)
        self.ui.attsearchButton.clicked.connect(self.attsearch_button_pressed)
        self.ui.tButton.clicked.connect(self.tips_button_pressed)
        self.ui.checkButton.clicked.connect(self.checkin_button_pressed)
        # GUI Elements - Users Page
        self.ui.loginUserName.textChanged.connect(self.user_login_updated)
        self.ui.loginUserIDs.itemSelectionChanged.connect(self.user_id_selected)
        self.ui.updateloc.clicked.connect(self.update_location)
        self.listCat = []
        self.atrList = []

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

    def updateQuery(self, sql_str):
        try:
            conn = psycopg2.connect("dbname='milestone2db' user ='postgres' host='localhost' password='0722'")
        except:
            print("Unable to connect")
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        count = cur.rowcount
        print(count, "Record Updated successfully ")
        conn.close()

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
        self.ui.catList.clear()

        if (self.ui.stateList.currentIndex() >= 0):
            state = self.ui.stateList.currentText()
            sql_str = "SELECT distinct city FROM business WHERE business_state ='" + state + "' ORDER BY city;"
            sql_str1 = "SELECT distinct postalcode FROM business WHERE business_state ='" + state + "' ORDER BY postalcode;"
            sql_str2 = "SELECT distinct category_name FROM (business b JOIN business_category a on b.business_id=a.business_id) WHERE business_state ='" + state + "' ORDER BY category_name;"
            sql_str3 = "SELECT distinct attribute_name FROM (business b JOIN business_attributes a on b.business_id=a.business_id) WHERE business_state ='" + state + "' ORDER BY attribute_name;"


            try:
                results = self.executeQuery(sql_str)
                results1 = self.executeQuery(sql_str1)
                results2 = self.executeQuery(sql_str2)
                results3 = self.executeQuery(sql_str3)
                for row in results:
                    self.ui.cityList.addItem(row[0])
                for row in results1:
                    self.ui.zipList.addItem(row[0])
                for row in results2:
                    self.ui.catList.addItem(row[0])
                for row in results3:
                    self.ui.attList.addItem(row[0])
            except:
                print("Query Failed!")
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)
            sql_str = "SELECT business_name, address,city, business_state, rating,numtips,numcheckins FROM business WHERE business_state ='" + state + "' ORDER BY business_name;"
            try:
                results = self.executeQuery(sql_str)
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address','City', 'State', 'rating','# of tips','Total Checkins',])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except:
                print("Query Failed!!")

    def cityChanged(self):
        self.ui.zipList.clear()
        self.ui.cityList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            city = self.ui.cityList.selectedItems()[0].text()
            sql_str = "SELECT business_name,address, city,business_state, rating,numtips,numcheckins FROM business WHERE city ='" + city + "' AND business_state= '" + state + "'ORDER BY business_name;"
            sql_str1 = "SELECT distinct postalcode FROM business WHERE city ='" + city + "' ORDER BY postalcode;"
            sql_str2 = "SELECT distinct category_name FROM business a, business_category b WHERE a.business_id=b.business_id AND  city ='" + city + "'ORDER BY category_name;"
            results = self.executeQuery(sql_str)
            results1 = self.executeQuery(sql_str1)
            results2 = self.executeQuery(sql_str2)

            try:
                results = self.executeQuery(sql_str)
                results1 = self.executeQuery(sql_str1)
                results2 = self.executeQuery(sql_str2)

                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address','City', 'State', 'rating','# of tips','Total Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                for row in results1:
                    self.ui.zipList.addItem(row[0])
                for row in results2:
                    self.ui.catList.addItem(row[0])

            except:
                print("Query Failed!!")

    def zipchanged(self):
        self.ui.catList.clear()
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.zipList.selectedItems()) > 0):
            state = self.ui.stateList.currentText()
            zip = self.ui.zipList.selectedItems()[0].text()
            sql_str = "SELECT business_name,address,city,business_state, rating,numtips,numcheckins FROM business WHERE postalcode ='" + zip + "' AND business_state= '" + state + "'ORDER BY business_name;"

            sql_str1 = "SELECT distinct category_name FROM business a, business_category b WHERE a.business_id=b.business_id AND  postalcode ='" + zip + "'ORDER BY category_name;"

            results = self.executeQuery(sql_str)
            results1 = self.executeQuery(sql_str1)

            try:
                results = self.executeQuery(sql_str)
                results1 = self.executeQuery(sql_str1)

                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business Name','Address','City', 'State', 'rating','# of tips','Total Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0, 300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                for row in results1:
                    self.ui.catList.addItem(row[0])

            except:
                print("Query Failed!!")

    def catchanged(self):

        #self.ui.businessTable.clear()

        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.catList.selectedItems()) > 0):
            self.listCat = []
            state = self.ui.stateList.currentText()
            # city = self.ui.cityList.currentText()
            # zip = self.ui.zipList.currentText()
            self.ui.catList.setSelectionMode(
                QtWidgets.QAbstractItemView.ExtendedSelection
            )
            try:
                for i in range(len(self.ui.catList.selectedItems())):
                    cat = self.ui.catList.selectedItems()[i].text()
                    self.listCat.append(cat)
                #joined_string = ",".join(self.listCat)
                joined_string = ', '.join(["'{}'".format(value) for value in self.listCat])
                print(joined_string)
                sql_str = "SELECT business_name, address,city,business_state, postalcode FROM business a, business_category b WHERE a.business_id=b.business_id AND  business_state = '" + state + "' AND  category_name in (" + joined_string + ") ORDER BY category_name;"
                print(sql_str)
                results = self.executeQuery(sql_str)
            except Exception as e:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                line_number = exception_traceback.tb_lineno
                print(line_number)
                print(e)
            try:
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(
                    ['Business Name', 'Address','City', 'State', 'rating','# of tips','Total Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                self.ui.businessTable.setColumnWidth(1, 100)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount,
                                                      QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1



            except:
                print("Query Failed!!")
            for i in reversed(range(self.ui.businessTable.rowCount())):
                self.ui.businessTable.removeRow(i)

    def displayBusinessDetails(self):
        self.ui.bname.setText("")
        self.ui.location.setText("")
        self.ui.otimings.setText("")
        self.ui.ctimings.setText("")
        selection = self.ui.businessTable.selectedItems()
        if len(selection) > 0 :
            name = selection[0].text()
            sql_str = "SELECT business_name FROM business WHERE business_name ='" + name + "'"
            sql_str1 = "SELECT address FROM business WHERE business_name ='" + name + "'"
            sql_str2 = "SELECT opening_time FROM (business b JOIN business_hour a on b.business_id=a.business_id) WHERE business_name ='" + name + "'"
            sql_str3 = "SELECT closing_time FROM (business b JOIN business_hour a on b.business_id=a.business_id) WHERE business_name ='" + name + "'"




            try:
                results = self.executeQuery(sql_str)
                results1 = self.executeQuery(sql_str1)
                results2 = self.executeQuery(sql_str2)
                results3 = self.executeQuery(sql_str3)



                self.ui.bname.setText(results[0][0])
                self.ui.location.setText(results1[0][0])
                self.ui.otimings.setText(str(results2[0][0]))
                self.ui.ctimings.setText(str(results3[0][0]))

            except Exception as e:
                print(e)

    def attchanged(self):
        if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.attList.selectedItems()) > 0):
            self.atrList = []
            state = self.ui.stateList.currentText()
            self.ui.attList.setSelectionMode(
                QtWidgets.QAbstractItemView.ExtendedSelection
            )
            try:
                for i in range(len(self.ui.attList.selectedItems())):
                    att = self.ui.attList.selectedItems()[i].text()
                    self.atrList.append(att)
                joined_string1 = ', '.join(["'{}'".format(value) for value in self.atrList])
                sql_str = "SELECT business_name,address, city,business_state, rating,numtips,numcheckins FROM business a, business_attributes b WHERE a.business_id=b.business_id AND  business_state ='" + state + "'  AND  category_name in (" + joined_string + ") AND attribute_value = 'True' AND  attribute_name in (" + joined_string1 + ") ORDER BY attribute_name;"
                print(sql_str)

            except Exception as e:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                line_number = exception_traceback.tb_lineno
                print(line_number)
                print(e)
            try:
                results = self.executeQuery(sql_str)
                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(
                    ['Business Name','Address', 'City', 'State', 'rating','# of tips','Total Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                self.ui.businessTable.setColumnWidth(1, 100)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount,
                                                      QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1


            except Exception as e:
                print(e)

    def search_button_pressed(self):
        try:
            joined_string = ', '.join(["'{}'".format(value) for value in self.listCat])

            if len(self.ui.catList.selectedItems()) > 0:
                zip = self.ui.zipList.selectedItems()[0].text()
            if len(self.ui.cityList.selectedItems()) > 0:
                city = self.ui.cityList.selectedItems()[0].text()
        #if len(self.ui.attList.selectedItems()) > 0:
            #att = self.ui.attList.selectedItems()[0].text()

                for i in reversed(range(self.ui.businessTable.rowCount())):
                    self.ui.businessTable.removeRow(i)

                sql_str = "SELECT business_name, city,business_state, rating,numtips,numcheckins FROM business a, business_category b WHERE a.business_id=b.business_id AND category_name in (" + joined_string + ") AND postalcode = '" + zip + "' AND city = '" + city + "' ORDER BY business_name;"
            #sql_str = "SELECT business_name, city,business_state, rating,numcheckins FROM (business a INNER JOIN business_category b ON a.business_id = b.business_id INNER JOIN business_attributes c ON a.business_id = c.business_id AND b.business_id = c.business_id) where category_name = '" + cat + "' AND postalcode = '" + zip + "' AND city = '" + city + "' AND attribute_name = '" + att + "' ORDER BY business_name;"
            #sql_str1 = "SELECT business_name, city,business_state, rating,numcheckins FROM business a, business_attributes b WHERE a.business_id=b.business_id AND attribute_name = '" + att + "' AND postalcode = '" + zip + "' AND city = '" + city + "'ORDER BY business_name;"

                print(sql_str)



                results = self.executeQuery(sql_str)
                #results1 = self.executeQuery(sql_str1)
                #print(results1)

                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(
                    ['Business Name', 'City', 'State', 'rating', '# of tips','Total Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                self.ui.businessTable.setColumnWidth(1, 100)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount,
                                                     QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1




        except Exception as e:
            print(e)
    def attsearch_button_pressed(self):
        try:
            # self.ui.latestTipsOfMyFriendsTable.clear()
            # self.ui.latestTipsOfMyFriendsTable.setColumnCount(0)
            # self.ui.latestTipsOfMyFriendsTable.setRowCount(0)
            # self.ui.myFriendsTable.clear()
            # self.ui.myFriendsTable.setColumnCount(0)
            # self.ui.myFriendsTable.setRowCount(0)
            joined_string = ', '.join(["'{}'".format(value) for value in self.atrList])
            joined_string_cat = ', '.join(["'{}'".format(value) for value in self.listCat])
            print(joined_string)
            print(joined_string_cat)
            if len(self.ui.catList.selectedItems()) > 0:
                zip = self.ui.zipList.selectedItems()[0].text()
            if len(self.ui.cityList.selectedItems()) > 0:
                city = self.ui.cityList.selectedItems()[0].text()


            # for i in reversed(range(self.ui.businessTable.rowCount())):
            #     self.ui.businessTable.removeRow(i)

                sql_str = "SELECT distinct business_name, city,business_state, rating,numtips,numcheckins FROM business a, business_attributes b, business_category bc WHERE a.business_id=b.business_id AND a.business_id=bc.business_id AND attribute_value = 'True'  AND category_name in (" + joined_string_cat + ")AND attribute_name in (" + joined_string + ") AND postalcode = '" + zip + "' AND city = '" + city + "'ORDER BY business_name;"
            #sql_str = "SELECT business_name, city,business_state, rating,numcheckins FROM (business a INNER JOIN business_category b ON a.business_id = b.business_id INNER JOIN business_attributes c ON a.business_id = c.business_id AND b.business_id = c.business_id) where category_name = '" + cat + "' AND postalcode = '" + zip + "' AND city = '" + city + "' AND attribute_name = '" + att + "' ORDER BY business_name;"
            #sql_str1 = "SELECT business_name, city,business_state, rating,numcheckins FROM business a, business_attributes b WHERE a.business_id=b.business_id AND attribute_name = '" + att + "' AND postalcode = '" + zip + "' AND city = '" + city + "'ORDER BY business_name;"

                print(sql_str)
                print("")


                results = self.executeQuery(sql_str)
                #results1 = self.executeQuery(sql_str1)
                print(results)
                print("")
                #print(results1)

                style = ":: section(""background-color: #f3f3f3; )"
                self.ui.businessTable.horizontalHeader().setStyleSheet(style)
                self.ui.businessTable.setColumnCount(len(results[0]))
                self.ui.businessTable.setRowCount(len(results))
                self.ui.businessTable.setHorizontalHeaderLabels(
                    ['Business Name', 'City', 'State', 'rating', '# of tips','Total Checkins'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,300)
                self.ui.businessTable.setColumnWidth(1, 100)
                self.ui.businessTable.setColumnWidth(2, 50)
                self.ui.businessTable.setColumnWidth(1, 100)

                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount,
                                                     QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line_number = exception_traceback.tb_lineno
            print(line_number)
            print(e)

    def tips_button_pressed(self):
        print("a")
        if len(self.ui.zipList.selectedItems()) > 0:
            zip = self.ui.zipList.selectedItems()[0].text()
        if len(self.ui.cityList.selectedItems()) > 0:
            city = self.ui.cityList.selectedItems()[0].text()
        print("b")
        # for i in reversed(range(self.ui.tipTable.rowCount())):
        #     self.ui.tipTable.removeRow(i)

        #sql_str = "SELECT tip_date,compliment_count,tip_text FROM business a, tip b WHERE a.business_id=b.business_id AND postalcode = '" + zip + "' AND city = '" + city + "'ORDER BY business_name;"

        try:
            sql_str = "SELECT tip_date,compliment_count,tip_text FROM business a, tip b WHERE a.business_id=b.business_id AND postalcode = '" + zip + "' AND city = '" + city + "'ORDER BY business_name;"
            results = self.executeQuery(sql_str)
            # results1 = self.executeQuery(sql_str1)
            print(results)
            style = ":: section(""background-color: #f3f3f3; )"
            self.ui.tipTable.horizontalHeader().setStyleSheet(style)
            self.ui.tipTable.setColumnCount(len(results[0]))
            self.ui.tipTable.setRowCount(len(results))
            self.ui.tipTable.setHorizontalHeaderLabels(['Tip date', 'Likes', 'Text'])
            self.ui.tipTable.resizeColumnsToContents()
            self.ui.tipTable.setColumnWidth(0,300)
            self.ui.tipTable.setColumnWidth(1, 100)
            self.ui.tipTable.setColumnWidth(2, 50)
            currentRowCount = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.tipTable.setItem(currentRowCount, colCount,
                                                      QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line_number = exception_traceback.tb_lineno
            print(line_number)
            print(e)
    def checkin_button_pressed(self): # The results are visible in page2 of the business UI
        if len(self.ui.zipList.selectedItems()) > 0:
            zip = self.ui.zipList.selectedItems()[0].text()
        if len(self.ui.cityList.selectedItems()) > 0:
            city = self.ui.cityList.selectedItems()[0].text()

        sql_str = "SELECT checkin_date,business_name,numcheckins FROM business a, checkin b WHERE a.business_id=b.business_id AND postalcode = '" + zip + "' AND city = '" + city + "'ORDER BY business_name;"

        print(sql_str)
        print("")

        try:
            results = self.executeQuery(sql_str)
            # results1 = self.executeQuery(sql_str1)
            print(results)
            print("")
            # print(results1)

            style = ":: section(""background-color: #f3f3f3; )"
            self.ui.tipTable.horizontalHeader().setStyleSheet(style)
            self.ui.tipTable.setColumnCount(len(results[0]))
            self.ui.tipTable.setRowCount(len(results))
            self.ui.tipTable.setHorizontalHeaderLabels(['Checkin date', 'Business Name', 'Checkins'])
            self.ui.tipTable.resizeColumnsToContents()
            self.ui.tipTable.setColumnWidth(0, 300)
            self.ui.tipTable.setColumnWidth(1, 300)
            self.ui.tipTable.setColumnWidth(2, 50)

            currentRowCount = 0
            for row in results:
                for colCount in range(0, len(results[0])):
                    self.ui.tipTable.setItem(currentRowCount, colCount,
                                             QTableWidgetItem(str(row[colCount])))
                currentRowCount += 1

        except Exception as e:

            print(e)

    def user_login_updated(self):
            self.ui.loginUserIDs.clear()
            user_name = self.ui.loginUserName.toPlainText()
            if len(user_name) > 0:
                sql_statement = "SELECT u.yelp_user_id, u.yelp_user_name  FROM yelp_user AS u WHERE yelp_user_name LIKE '" + user_name + "%'"
                try:
                    results = self.executeQuery(sql_statement)
                    for row in results:
                        self.ui.loginUserIDs.addItem(row[0])
                except Exception as e:
                    print(e)

    def user_id_selected(self):
        self.ui.infoName.clear()
        self.ui.infoStars.clear()
        self.ui.infoFans.clear()
        self.ui.infoYelpingSince.clear()
        self.ui.infoFunny.clear()
        self.ui.infoCool.clear()
        self.ui.infoUseful.clear()
        self.ui.latestTipsOfMyFriendsTable.clear()
        self.ui.myFriendsTable.setColumnCount(0)
        self.ui.latestTipsOfMyFriendsTable.setColumnCount(0)
        self.ui.tipcount.clear()
        self.ui.totallikes.clear()
        self.ui.latitude.clear()
        self.ui.longitude.clear()
        self.ui.latestTipsOfMyFriendsTable.clear()
        self.ui.latestTipsOfMyFriendsTable.setColumnCount(0)
        self.ui.latestTipsOfMyFriendsTable.setRowCount(0)
        self.ui.myFriendsTable.clear()
        self.ui.myFriendsTable.setColumnCount(0)
        self.ui.myFriendsTable.setRowCount(0)

        print(len(self.ui.loginUserIDs.selectedItems()))
        if len(self.ui.loginUserIDs.selectedItems()) > 0:
            selected_id = self.ui.loginUserIDs.selectedItems()[0].text()
            name_sql = "SELECT u.yelp_user_name,u.rating,u.fans_count,u.yelping_since,u.funny_count,u.cool_count,u.useful_count,u.tipcount,u.totallikes,u.latitude,u.longitude" \
                       " FROM yelp_user AS U WHERE u.yelp_user_id = '" + selected_id + "'"
            friends_table_sql = "Select f.friend_id,u.totallikes,u.rating,u.yelping_since from friends f join yelp_user u on f.friend_id = u.yelp_user_id where f.yelp_user_id = '" + selected_id + "' ORDER BY u.yelp_user_name"
            try:
                name_result = self.executeQuery(name_sql)
                friends_table_results = self.executeQuery(friends_table_sql)
                self.ui.infoName.addItem(str(name_result[0][0]))
                self.ui.infoStars.addItem(str(name_result[0][1]))
                self.ui.infoFans.addItem(str(name_result[0][2]))
                self.ui.infoYelpingSince.addItem(str(name_result[0][3]))
                self.ui.infoFunny.addItem(str(name_result[0][4]))
                self.ui.infoCool.addItem(str(name_result[0][5]))
                self.ui.infoUseful.addItem(str(name_result[0][6]))
                self.ui.tipcount.addItem(str(name_result[0][7]))
                self.ui.totallikes.addItem(str(name_result[0][8]))
                self.ui.latitude.setPlainText(str(name_result[0][9]))
                self.ui.longitude.setPlainText(str(name_result[0][10]))
                self.ui.latestTipsOfMyFriendsTable.clear()
                self.ui.latestTipsOfMyFriendsTable.setColumnCount(0)
                self.ui.latestTipsOfMyFriendsTable.setRowCount(0)
                self.ui.myFriendsTable.clear()
                self.ui.myFriendsTable.setColumnCount(0)
                self.ui.myFriendsTable.setRowCount(0)

                if len(friends_table_results) > 0:
                    a = str(list(zip(*friends_table_results))[0])
                    latest_tips_table_sql = "Select y.yelp_user_name,business_name,city,t.tip_text,maxdate from tip t natural join yelp_user y join (Select yelp_user_id, max(tip_date) as maxdate from tip where yelp_user_id in " + a + "group by yelp_user_id) tt on t.yelp_user_id = tt.yelp_user_id and t.tip_date = tt.maxdate join  business b on b.business_id = t.business_id"
                    latest_tips_table_results = self.executeQuery(latest_tips_table_sql)
                    style = "::section {""background-color: #f3f3f3; }"
                    self.ui.myFriendsTable.horizontalHeader().setStyleSheet(style)
                    self.ui.myFriendsTable.setColumnCount(len(friends_table_results[0]))
                    self.ui.myFriendsTable.setRowCount(len(friends_table_results))
                    self.ui.myFriendsTable.setHorizontalHeaderLabels(
                        ["Friend Name", "Total Likes", "Avg Stars", "Yelping Since"])
                    self.ui.myFriendsTable.resizeColumnsToContents()
                    self.ui.myFriendsTable.setColumnWidth(0, 180)
                    self.ui.myFriendsTable.setColumnWidth(1, 80)
                    self.ui.myFriendsTable.setColumnWidth(2, 80)
                    self.ui.myFriendsTable.setColumnWidth(3, 159)
                    current_row_count = 0
                    for row in friends_table_results:
                        for col_count in range(0, len(friends_table_results[0])):
                            self.ui.myFriendsTable.setItem(current_row_count, col_count,
                                                           QTableWidgetItem(str(row[col_count])))
                        current_row_count += 1
                    if len(latest_tips_table_results) > 0:
                        style = "::section {""background-color: #f3f3f3; }"
                        self.ui.latestTipsOfMyFriendsTable.horizontalHeader().setStyleSheet(style)
                        self.ui.latestTipsOfMyFriendsTable.setColumnCount(len(latest_tips_table_results[0]))
                        self.ui.latestTipsOfMyFriendsTable.setRowCount(len(latest_tips_table_results))
                        self.ui.latestTipsOfMyFriendsTable.setHorizontalHeaderLabels(
                            ["User Name", "Business", "City", "Text", "Date"])
                        self.ui.latestTipsOfMyFriendsTable.resizeColumnsToContents()
                        self.ui.latestTipsOfMyFriendsTable.setColumnWidth(0, 110)
                        self.ui.latestTipsOfMyFriendsTable.setColumnWidth(1, 150)
                        self.ui.latestTipsOfMyFriendsTable.setColumnWidth(2, 75)
                        self.ui.latestTipsOfMyFriendsTable.setColumnWidth(3, 110)
                        self.ui.latestTipsOfMyFriendsTable.setColumnWidth(4, 130)
                        current_row_count = 0
                        for row in latest_tips_table_results:
                            for col_count in range(0, len(latest_tips_table_results[0])):
                                self.ui.latestTipsOfMyFriendsTable.setItem(current_row_count, col_count,
                                                                           QTableWidgetItem(str(row[col_count])))
                            current_row_count += 1
                    else:
                        self.ui.latestTipsOfMyFriendsTable.clear()
                        self.ui.latestTipsOfMyFriendsTable.setColumnCount(0)
                        self.ui.latestTipsOfMyFriendsTable.setRowCount(0)
                else:
                    self.ui.latestTipsOfMyFriendsTable.clear()
                    self.ui.latestTipsOfMyFriendsTable.setColumnCount(0)
                    self.ui.latestTipsOfMyFriendsTable.setRowCount(0)
                    self.ui.myFriendsTable.clear()
                    self.ui.myFriendsTable.setColumnCount(0)
                    self.ui.myFriendsTable.setRowCount(0)

            except Exception as e:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                line_number = exception_traceback.tb_lineno
                print(line_number)
                print(e)

    def update_location(self):
        latitude = self.ui.latitude.toPlainText()
        longitude = self.ui.longitude.toPlainText()
        # Update_location = "Select y.yelp_user_name,business_name,city,t.tip_text,maxdate from tip t natural join yelp_user y join (Select yelp_user_id, max(tip_date) as maxdate from tip where yelp_user_id in " + a + "group by yelp_user_id) tt on t.yelp_user_id = tt.yelp_user_id and t.tip_date = tt.maxdate join  business b on b.business_id = t.business_id"
        selected_id = self.ui.loginUserIDs.selectedItems()[0].text()
        Update_location_sql = "update yelp_user set latitude =" + str(latitude) + " ,longitude = " + str(
            longitude) + " where yelp_user_id = '" + selected_id + "'"
        print(Update_location_sql)
        try:
            self.updateQuery(Update_location_sql)
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line_number = exception_traceback.tb_lineno
            print(line_number)
            print(e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2()
    window.show()
    sys.exit(app.exec_())
