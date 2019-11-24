import json
import os
import threading
import time

from PyQt5 import QtWidgets, QtCore

from P2P.p2p_main import P2P
from UI_design.MainWindow_ui import Ui_MainWindow


class flushThread(QtCore.QThread):  # 监听UI更新子线程
    _signal = QtCore.pyqtSignal()

    def __init__(self, sem):
        super().__init__()
        self.sem = sem

    def run(self):
        while True:
            self.sem.acquire()
            self._signal.emit()


class downloadThread(QtCore.QThread):  # 下载线程
    _signal = QtCore.pyqtSignal([QtWidgets.QListWidgetItem, QtCore.QThread, str])
    _fail = QtCore.pyqtSignal(str)
    _updateprocess = QtCore.pyqtSignal([QtWidgets.QProgressBar, int])

    def __init__(self, savePath, path, addr, p2p, wiget, item):
        super().__init__()
        self.savePath = savePath
        self.path = path
        self.addr = addr
        self.p2p = p2p
        self.wiget = wiget
        self.item = item

    def run(self):
        try:
            wiget = self.wiget.children()[-1]
            self.p2p.download(self.savePath, self.path, self.addr, wiget, self._updateprocess)
        except ConnectionRefusedError:
            self._fail.emit('连接被拒绝')
        time.sleep(0.5)
        wiget.setValue(100)
        self._signal.emit(self.item, self, '{}下载成功'.format(os.path.basename(self.path)))


class MainWindow_SLOT(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.ui.pushButton_search.clicked.connect(self.pushButton_search_click)
        self.ui.pushButton_addFile.clicked.connect(self.pushButton_addFile)
        self.ui.pushButton_addDir.clicked.connect(self.pushButton_addDir)
        self.ui.sharingListWidget.setContextMenuPolicy(3)
        self.ui.sharingListWidget.customContextMenuRequested.connect(self.customMenu)
        self.ui.sharingListWidget.itemDoubleClicked.connect(self.shareListItemClicked)

        self.ui.responseListWidget.setContextMenuPolicy(3)
        self.ui.responseListWidget.customContextMenuRequested.connect(self.customMenu2)

        self.semaphore = threading.Semaphore(0)
        fthread = flushThread(self.semaphore)
        fthread._signal.connect(self.flushResponseWidget)
        fthread.start()
        self.threadPool = []

        self.p2p = P2P(self, 8848, 8858)

    def shareListItemClicked(self, item):
        items = self.ui.sharingListWidget.itemWidget(item).children()
        items[1].setChecked(not items[1].isChecked())
        self.p2p.changShareState(items[0].text(), items[1].isChecked())

    def customMenu2(self, pos):
        wiget = self.ui.responseListWidget.itemWidget(self.ui.responseListWidget.itemAt(pos))
        menu = QtWidgets.QMenu()
        opt1 = menu.addAction('下载')
        if isinstance(wiget, QtWidgets.QWidget):
            action = menu.exec_(self.ui.responseListWidget.mapToGlobal(pos))
            if action == opt1:
                child = wiget.children()
                path = child[-1].text()
                addr = child[-2].text()
                self.addDownWiget(child[0].text(), addr, path)

    def customMenu(self, pos):

        item = self.ui.sharingListWidget.itemAt(pos)
        menu = QtWidgets.QMenu()
        opt1 = menu.addAction('删除')
        if isinstance(item, QtWidgets.QListWidgetItem):
            action = menu.exec_(self.ui.sharingListWidget.mapToGlobal(pos))
            if action == opt1:
                wiget = self.ui.sharingListWidget.itemWidget(item)
                child = wiget.children()
                self.p2p.delShare(child[0].text())
                self.flushSharingListWidget()

    def pushButton_search_click(self):
        self.ui.responseListWidget.clear()
        self.p2p.search_send(self.ui.lineEdit.text())

    def pushButton_addFile(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName()
        self.p2p.sharing(filePath)
        self.flushSharingListWidget()

    def pushButton_addDir(self):
        dirPath = QtWidgets.QFileDialog.getExistingDirectory()
        self.p2p.sharing_dir(dirPath)
        self.flushSharingListWidget()

    def flushSharingListWidget(self):
        self.ui.sharingListWidget.clear()

        def get_item_wiget(data):
            wiget = QtWidgets.QWidget()
            wiget.setContentsMargins(0, 0, 0, 0)
            label = QtWidgets.QLabel(wiget)
            label.setText(data['name'])
            label.setGeometry(QtCore.QRect(0, 0, 620, 20))
            check = QtWidgets.QCheckBox(wiget)
            check.setChecked(data['share'])
            check.setGeometry(QtCore.QRect(620, 0, 20, 20))
            check.setText('')
            check.setEnabled(False)
            return wiget

        for shipData in self.p2p.load.getFileList():
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(650, 20))
            wiget = get_item_wiget(shipData)
            self.ui.sharingListWidget.addItem(item)
            self.ui.sharingListWidget.setItemWidget(item, wiget)

        for shipData in self.p2p.load.getDirList():
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(650, 20))
            wiget = get_item_wiget(shipData)
            self.ui.sharingListWidget.addItem(item)
            self.ui.sharingListWidget.setItemWidget(item, wiget)

    def flushResponseWidget(self):
        self.ui.responseListWidget.clear()

        def get_item_wiget(data):
            wiget = QtWidgets.QWidget()
            wiget.setContentsMargins(0, 0, 0, 0)
            name = QtWidgets.QLabel(wiget)
            name.setText(data['name'])
            name.setGeometry(QtCore.QRect(0, 0, 400, 20))
            size = QtWidgets.QLabel(wiget)
            size.setText(str(data['size']))
            size.setGeometry(QtCore.QRect(400, 0, 200, 20))
            addr = QtWidgets.QLabel(wiget)
            addr.setText(data['addr'])
            addr.setGeometry(QtCore.QRect(600, 0, 180, 20))
            path = QtWidgets.QLabel(wiget)
            path.setText(data['path'])
            path.setVisible(False)
            return wiget

        for data in self.p2p.responseRecvSet:
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(QtCore.QSize(780, 20))
            wiget = get_item_wiget(json.loads(data))
            self.ui.responseListWidget.addItem(item)
            self.ui.responseListWidget.setItemWidget(item, wiget)

    def addDownWiget(self, name, addr, path):
        def get_wiget(name, addr):
            wiget = QtWidgets.QWidget()
            wiget.setContentsMargins(0, 0, 0, 0)
            nameLabel = QtWidgets.QLabel(wiget)
            nameLabel.setText(name)
            nameLabel.setGeometry(QtCore.QRect(20, 0, 380, 20))
            addrLabel = QtWidgets.QLabel(wiget)
            addrLabel.setText(addr)
            addrLabel.setGeometry(QtCore.QRect(400, 0, 200, 20))
            processbar = QtWidgets.QProgressBar(wiget)
            processbar.setGeometry(QtCore.QRect(600, 0, 180, 20))
            processbar.setValue(0)
            return wiget

        wiget = get_wiget(name, addr)

        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(QtCore.QSize(780, 20))
        savePath = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', name)[0]
        self.ui.loadListWidget.addItem(item)
        self.ui.loadListWidget.setItemWidget(item, wiget)

        if savePath == '':
            return
        dthread = downloadThread(savePath, path, addr, self.p2p, wiget, item)
        dthread._signal.connect(self.removeLoadListWiget)
        dthread._fail.connect(lambda s: QtWidgets.QMessageBox.warning(self, '错误', s))
        dthread._updateprocess.connect(lambda x, y: x.setValue(y))
        dthread.start()
        self.threadPool.append(dthread)

    def removeLoadListWiget(self, item: QtWidgets.QListWidgetItem, thread, message):
        QtWidgets.QMessageBox.information(self, '成功', message)
        self.ui.loadListWidget.takeItem(self.ui.loadListWidget.row(item))
        self.threadPool.remove(thread)
