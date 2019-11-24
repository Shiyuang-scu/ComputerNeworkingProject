from socket import *
from P2P.concreteOp import UDLoad
from P2P.ip_related import *
from PyQt5 import QtWidgets, QtGui, QtCore
import platform
import _thread
import select
import json
import struct
import time
import os


class P2P:
    def __init__(self, SLOT, port: int, downRequestport: int):
        """
        :type SLOT: MainWindow_SLOT
        :type port: int
        """
        self.__port = port
        self.__downPort = downRequestport
        self.__timestamp = 0
        self.load = UDLoad()
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        self.sock.bind(('0.0.0.0', port))

        self.tcpsock = socket(AF_INET, SOCK_STREAM)
        self.tcpsock.bind(('', downRequestport))
        self.tcpsock.listen(5)
        # self.tcpsock.setblocking(False)

        self.broadAddr = [(addr, port) for addr in find_all_broad(platform.system())]
        self.myAddr = [(addr, port) for addr in find_all_ip(platform.system())]
        self.mask = find_all_mask(platform.system())
        self.Addr = [{'myAddr': self.myAddr[i], 'broadAddr': self.broadAddr[i], 'mask': self.mask[i]} for i in
                     range(len(self.broadAddr))]
        self.recvSSet = set()  # 接受到的请求搜索的包
        self.responseRecvSet = set()  # 接受到的请求搜索的包
        self.SLOT = SLOT  # 控制反转时，控制主页面
        _thread.start_new_thread(listenFunc, (self,))
        _thread.start_new_thread(tcplistenFunc, (self,))

    def close(self):
        self.sock.shutdown(SHUT_RDWR)
        self.sock.close()

    # Add share file
    def sharing(self, filepath):
        self.load.addShareFile(filepath)

    # Add share file list
    def sharing_dir(self, dirpath):
        self.load.addShareDir(dirpath)

    # Delete share file
    def delShare(self, path):
        self.load.delShare(path)

    # Change share status
    def changShareState(self, path, state):
        self.load.changShareState(path, state)

    # Get the search request
    def search_recv(self, recv, addr):
        if recv in self.recvSSet:  # 如果包已经在内存中出现过，则忽略
            return
        self.recvSSet.add(recv)
        # self.SHOW.ui.lineEdit.setText(recv.decode())
        for addr in self.broadAddr:  # 转发
            self.sock.sendto(recv, addr)
        urecv = json.loads(recv)
        slist = self.load.search(urecv['name'])
        response = {}
        response['opt'] = 'r'
        response['data'] = slist
        response['timestamp'] = urecv['timestamp']
        response['addr'] = [i['myAddr'][0] for i in self.Addr if isSameSubnet(addr[0], i['myAddr'][0], i['mask'])][0]
        if len(slist) != 0:
            self.sock.sendto(json.dumps(response).encode(), (urecv['addr'], self.__port))

    # Get the search contents
    def response_recv(self, urecv, addr):
        if urecv['timestamp'] != self.__timestamp:  # 如果是过期的包，则忽略
            return
        result = urecv['data']
        for data in result:
            data['addr'] = urecv['addr']
        result = set([json.dumps(data) for data in result])
        self.responseRecvSet = self.responseRecvSet | result  # 并集
        self.SLOT.semaphore.release()

    # Send the search request
    def search_send(self, name):
        search = {}
        search['opt'] = 's'
        search['name'] = name
        self.__timestamp = int(time.time())
        search['timestamp'] = self.__timestamp
        self.responseRecvSet = set()
        for addr in self.Addr:
            search['addr'] = addr['myAddr'][0]
            out = json.dumps(search)
            self.recvSSet.add(out.encode())
            self.sock.sendto(out.encode(), addr['broadAddr'])

    # Sent the download request
    def download(self, savePath, path, addr, processbar: QtWidgets.QProgressBar, emit):
        pc = socket(AF_INET, SOCK_STREAM)
        pc.connect((addr, self.__downPort))
        head = {}
        head['path'] = path
        head_s = json.dumps(head).encode()
        head_len = struct.pack('i', len(head_s))

        pc.send(head_len)
        pc.send(head_s)
        port = struct.unpack('i', pc.recv(4))[0]
        pc.close()
        pc = socket(AF_INET, SOCK_STREAM)
        pc.connect((addr, port))
        head_len = struct.unpack('i', pc.recv(4))[0]
        head = json.loads(pc.recv(head_len))
        # savePath = QtWidgets.QFileDialog.getSaveFileName(self.SHOW, 'Save File', head['name'])[0]
        if savePath == '':
            pc.close()
            return
        total_size = head['size']
        last_time = time.time()
        with open(savePath, 'wb') as f:
            recv_size = 0
            while recv_size < total_size:
                res = pc.recv(1024)
                f.write(res)
                recv_size += len(res)
                if time.time() - last_time >= 0.5:
                    last_time = time.time()
                    emit.emit(processbar, int(recv_size * 100 / total_size))
        pc.close()
        # QtWidgets.QMessageBox.information(self.SHOW, '成功', '{}下载完成'.format(head['name']))


def listenFunc(p2p: P2P):
    r_inputs = set()
    r_inputs.add(p2p.sock)
    while True:
        r_list, w_list, e_list = select.select(r_inputs, [], [])
        for event in r_list:
            recv, addr = event.recvfrom(10240)
            if addr in p2p.myAddr:  # 如果发包人是自己，则忽略
                continue
            urecv = json.loads(recv)
            if urecv['opt'] == 's':  # 接收到是请求搜索的数据包
                p2p.search_recv(recv, addr)
            if urecv['opt'] == 'r':  # 收到的是搜索结果的数据包
                p2p.response_recv(urecv, addr)


def tcplistenFunc(p2p: P2P):
    clientAddrlist = []
    while True:
        try:
            clientSocket, clientAddr = p2p.tcpsock.accept()
        except:
            pass
        else:
            # clientSocket.setblocking(False)
            clientAddrlist.append((clientSocket, clientAddr))
        for socket, addr in clientAddrlist:
            try:
                # 接收报头长度
                head_len_byte = socket.recv(4)
                head_len = struct.unpack('i', head_len_byte)[0]
                # 接收报头
                head = socket.recv(head_len)
                recv = json.loads(head)
                path = recv['path']
                port, sock = findFreePort()

                _thread.start_new_thread(downlisten, (sock, path))
                responseHead_len = struct.pack('i', port)
                # 返回端口
                socket.send(responseHead_len)
                socket.close()
                clientAddrlist.remove((socket, addr))
            except Exception as e:
                print(e)


def downlisten(socket: socket, path: str):
    childsocket, childsaddr = socket.accept()
    head = {}
    head['name'] = os.path.basename(path)
    head['size'] = os.path.getsize(path)
    head_json = json.dumps(head).encode()
    head_len = struct.pack('i', len(head_json))
    childsocket.send(head_len)
    childsocket.send(head_json)
    with open(path, 'rb') as f:
        while True:
            sen = f.read(1024)
            if len(sen) == 0:
                break
            childsocket.send(sen)
    childsocket.close()
    socket.close()


