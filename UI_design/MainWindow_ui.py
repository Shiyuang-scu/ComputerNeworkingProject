# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI_design code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(836, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.searchListWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.searchListWidget.setGeometry(QtCore.QRect(20, 0, 800, 591))
        self.searchListWidget.setObjectName("searchListWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 641, 40))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_search = QtWidgets.QPushButton(self.tab)
        self.pushButton_search.setEnabled(True)
        self.pushButton_search.setGeometry(QtCore.QRect(660, 30, 120, 40))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.pushButton_search.setFont(font)
        self.pushButton_search.setObjectName("pushButton_search")
        self.responseListWidget = QtWidgets.QListWidget(self.tab)
        self.responseListWidget.setGeometry(QtCore.QRect(10, 99, 780, 431))
        self.responseListWidget.setGridSize(QtCore.QSize(0, 20))
        self.responseListWidget.setObjectName("responseListWidget")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 10, 341, 16))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 261, 16))
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(10, 540, 221, 16))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(660, 540, 141, 20))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(350, 540, 201, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(320, 80, 171, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(640, 80, 91, 16))
        self.label_8.setObjectName("label_8")
        self.searchListWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton_addFile = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_addFile.setEnabled(True)
        self.pushButton_addFile.setGeometry(QtCore.QRect(430, 10, 120, 40))
        self.pushButton_addFile.setObjectName("pushButton_addFile")
        self.pushButton_addDir = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_addDir.setEnabled(True)
        self.pushButton_addDir.setGeometry(QtCore.QRect(240, 10, 120, 40))
        self.pushButton_addDir.setObjectName("pushButton_addDir")
        self.sharingListWidget = QtWidgets.QListWidget(self.tab_2)
        self.sharingListWidget.setGeometry(QtCore.QRect(20, 70, 761, 501))
        self.sharingListWidget.setGridSize(QtCore.QSize(0, 20))
        self.sharingListWidget.setObjectName("sharingListWidget")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(20, 50, 131, 16))
        self.label_5.setObjectName("label_5")
        self.searchListWidget.addTab(self.tab_2, "")
        self.loadListWidget = QtWidgets.QListWidget(self.centralwidget)
        self.loadListWidget.setGeometry(QtCore.QRect(29, 590, 791, 131))
        self.loadListWidget.setGridSize(QtCore.QSize(0, 20))
        self.loadListWidget.setObjectName("loadListWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 836, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.searchListWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_search.setText(_translate("MainWindow", "搜索"))
        self.label.setText(_translate("MainWindow", "请输入搜索关键词：（Note：大小写敏感）"))
        self.label_3.setText(_translate("MainWindow", "搜索结果："))
        self.label_2.setText(_translate("MainWindow", "下载文件："))
        self.label_4.setText(_translate("MainWindow", "下载进度："))
        self.label_6.setText(_translate("MainWindow", "源IP："))
        self.label_7.setText(_translate("MainWindow", "文件大小:"))
        self.label_8.setText(_translate("MainWindow", "源IP:"))
        self.searchListWidget.setTabText(self.searchListWidget.indexOf(self.tab), _translate("MainWindow", "下载共享文件"))
        self.pushButton_addFile.setText(_translate("MainWindow", "添加文件"))
        self.pushButton_addDir.setText(_translate("MainWindow", "添加目录"))
        self.label_5.setText(_translate("MainWindow", "加入文件/目录："))
        self.searchListWidget.setTabText(self.searchListWidget.indexOf(self.tab_2), _translate("MainWindow", "上传共享文件"))
