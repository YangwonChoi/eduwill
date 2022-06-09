import imp
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSlot
from socket import *
import sys

form_stu = uic.loadUiType("student.ui")[0]


class SocketClient(QThread):
    add_chat = QtCore.pyqtSignal(list) #나중에 데이터 받을때 슬롯들
    add_user = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.is_run = False

    def connect_cle(self):
        self.cnn = socket(AF_INET, SOCK_STREAM)
        self.cnn.connect(('127.0.0.1', 2090))
        self.is_run = True
        self.cnn.send('stu'.encode())

    def recv(self):
        sys.stdout.flush()
        data = self.cnn.recv(2048)
        data = data.decode()

    def send(self, msg):
        if self.is_run:
            sys.stdin.flush()
            self.cnn.send(f'{msg}'.encode())


class Student_Window(QMainWindow, form_stu):
    def __init__(self):
        super(Student_Window, self).__init__()
        self.initUI()
        self.t1 = SocketClient()
        self.t1.connect_cle()
        self.t1.start()
        self.show()
        # -----------------시그널-----------------------------
        self.sign_up_btn.clicked.connect(self.sign_up)  # sign_up버튼 눌럿을떄
        self.back_btn.clicked.connect(self.sign_up_exit)  # 취소버튼 눌럿을떄
        self.confirm_btn.clicked.connect(self.sign_up_cf)  # 확인버튼 눌럿을떄
        self.login_btn.clicked.connect(self.login) #로그인 버튼 눌럿을때
        self.idcheck_btn.clicked.connect(self.check_id)

    def check_id(self):
        id = self.sign_id.text()
        self.t1.send(id)
        msg = self.t1.recv()
        if msg == 'OK':
            pass
        elif msg == 'NO':
            pass
        else:
            pass

    def initUI(self):
        self.setupUi(self)
        self.sign_widget.hide()
        self.sign_pw.setEchoMode(QLineEdit.Password)
        self.sign_pw_2.setEchoMode(QLineEdit.Password)
        self.login_pw.setEchoMode(QLineEdit.Password)

    def sign_up(self):
        self.t1.send("@sign_up")
        self.sign_widget.show()

    def sign_up_exit(self):  # 취소버튼 눌럿을떄
        self.name.clear()
        self.sign_id.clear()
        self.sign_pw.clear()
        self.sign_pw_2.clear()
        self.sign_widget.close()

    def sign_up_cf(self): #확인 눌럿을때
        if self.sign_pw.text() != self.sign_pw_2.text():
            pass
        else:
            data = self.sign_id.text() + '/' + self.sign_pw.text() + '/' + self.name.text()
            self.t1.send(data)
            self.sign_widget.close()


    def login(self): #로그인 버튼 눌럿을때
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Student_Window()
    win.show()
    sys.exit(app.exec())
