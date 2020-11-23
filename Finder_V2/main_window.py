import sys
import time
import subprocess
import os
from threading import Thread
import pickle
import re
from PyQt5 import QtCore, QtGui, QtWidgets

drive1 = False
folder1 = False
item1 = ""
dict1 = {}


def get_drives():
    resp = os.popen('wmic logicaldisk get caption')
    drive = resp.read()
    return drive.split()[1:]


def peopen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    res = process.stdout.read().split()[1:]
    final = []
    for each in res:
        each = each.decode('utf-8')
        final.append(each)
    return final


def creating_Dict(dr):
    for root, dir, files in os.walk(dr, topdown=True):
        dir = [each+">" for each in dir]
        files.extend(dir)
        for file in files:
            file = file.lower()
            if file in dict1:
                pass
            else:
                dict1[file] = root + "\\" + file


def create_Index1():
    tnow = time.time()
    list1_th = []
    list1 = peopen('wmic logicaldisk get caption')
    for each in list1:
        each = each + "\\"
        th1 = Thread(target=creating_Dict, args=(each,))
        th1.start()
        list1_th.append(th1)

    for th1 in list1_th:
        th1.join()

    file_path = os.path.expanduser('~')
    os.chdir(file_path)
    fw = open("finder_index", "wb")
    pickle.dump(dict1, fw)
    fw.close()
    t2 = time.time()


def search(file1, drive=None, folder_f=None, dr1=None):
    file_path = os.path.expanduser('~')
    os.chdir(file_path)
    fr = open("finder_index", "rb")
    data1 = pickle.load(fr)
    fr.close()
    file_to_be_searched = file1.lower()
    file_to_be_searched = r'{}'.format(file_to_be_searched)
    list1 = []
    for k in data1:
        if re.search(file_to_be_searched, k, re.I):
            str1 = data1[k]
            list1.append(str1)
    list1.sort()

    if drive:
        drive = dr1
        list1 = [each for each in list1 if each.startswith(drive)]

    if list1:
        list3 = []
        if folder_f:
            for each in list1:
                if each.endswith(">"):
                    list3.append(each)
                else:
                    pass
                list1 = list3

    dict_data = {}
    for index, item in enumerate(list1):
        if folder_f:
            if item.endswith(">"):
                dict_data[index] = item.split("|")[0].rstrip(">")
            else:
                pass
        else:
            if item.endswith(">"):
                pass
            else:
                dict_data[index] = item.split("|")[0]
    t2 = time.time()
    return dict_data


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1060, 533)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 30, 461, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.inser = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.inser.setFont(font)
        self.inser.setObjectName("inser")
        self.horizontalLayout.addWidget(self.inser)
        self.btnser = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.btnser.setFont(font)
        self.btnser.setObjectName("btnser")
        self.horizontalLayout.addWidget(self.btnser)
        self.btnchk = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.btnchk.setFont(font)
        self.btnchk.setObjectName("btnchk")
        self.horizontalLayout.addWidget(self.btnchk)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(31, 70, 333, 27))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chkfolder = QtWidgets.QCheckBox(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.chkfolder.setFont(font)
        self.chkfolder.setObjectName("chkfolder")
        self.horizontalLayout_2.addWidget(self.chkfolder)
        self.chkdrive = QtWidgets.QCheckBox(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.chkdrive.setFont(font)
        self.chkdrive.setObjectName("chkdrive")
        self.horizontalLayout_2.addWidget(self.chkdrive)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 150, 1000, 261))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalScrollBar()
        self.tableWidget.verticalScrollBar()
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 430, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.drive_combo = QtWidgets.QComboBox(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.drive_combo.setFont(font)
        self.drive_combo.setObjectName("drive_combo")
        self.horizontalLayout_2.addWidget(self.drive_combo)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.inser, self.btnser)
        MainWindow.setTabOrder(self.btnser, self.btnchk)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Search_Files"))
        self.label.setText(_translate("MainWindow", "Key Word:"))
        self.btnser.setText(_translate("MainWindow", "Search"))
        self.btnser.clicked.connect(self.on_Search)
        self.btnchk.setText(_translate("MainWindow", "Create Index"))
        self.btnchk.clicked.connect(self.on_create)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Files/Folders"))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.cellClicked.connect(self.cclicked)
        self.chkfolder.setText(_translate("MainWindow", "Folder Only"))
        self.chkdrive.setText(_translate("MainWindow", "Search by Drive"))
        self.pushButton.setText(_translate("MainWindow", "Open"))
        self.pushButton.clicked.connect(self.on_open)
        self.pushButton.setEnabled(False)
        resp = peopen('wmic logicaldisk get caption')
        for each in resp:
            self.drive_combo.addItem(each)

    def showdata(self, dict_res):
        row = 0
        self.tableWidget.setRowCount(len(dict(dict_res)))
        if len(dict(dict_res)) > 0:
            for k, v in dict_res.items():
                self.tableWidget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(v))
                row += 1
            self.tableWidget.resizeColumnsToContents()
        else:
            self.pushButton.setEnabled(False)

    def on_open(self):
        global item1
        if self.chkfolder.isChecked():
            folder_path = item1.split(">")[0]
            os.chdir(folder_path)
            subprocess.Popen(r'explorer /E,"." ')
        else:
            file_name = item1
            os.startfile(file_name)

    def on_Search(self):
        global drive1, folder1
        if self.chkdrive.isChecked() and self.chkfolder.isChecked() == False:
            drive1 = True
            drv1 = str(self.drive_combo.currentText())
            self.pushButton.setEnabled(True)
            file_name = self.inser.text()
            dict_res = search(file_name, drive1, folder1, drv1)
            self.showdata(dict_res)
            drive1 = False
        elif self.chkfolder.isChecked() and self.chkdrive.isChecked() == False:
            folder1 = True
            self.pushButton.setEnabled(True)
            file_name = self.inser.text()
            dict_res = search(file_name, drive1, folder1)
            self.showdata(dict_res)
            folder1 = False
        elif self.inser.text() == "":
            pass
        elif self.chkfolder.isChecked() and self.chkdrive.isChecked():
            folder1 = True
            drive1 = True
            drv1 = str(self.drive_combo.currentText())
            self.pushButton.setEnabled(True)
            file_name = self.inser.text()
            dict_res = search(file_name, drive1, folder1, drv1)
            self.showdata(dict_res)
            drive1 = False
            folder1 = False
        else:
            self.pushButton.setEnabled(True)
            file_name = self.inser.text()
            dict_res = search(file_name, drive1, folder1)
            self.showdata(dict_res)

    def cclicked(self, row, column):
        global item1
        self.row = row
        self.column = column
        item1 = (self.tableWidget.item(self.row, self.column)).text()

    def on_create(self):
        create_Index1()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
