import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSlot
from socket import *

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
        self.cnn.connect(('localhost', 2090))
        self.is_run = True
        self.cnn.send('stu'.encode())

    def run(self):
        while True:
            data = self.cnn.recv(2048)

            if not data:
                break
            data = data.decode()

    def send(self, msg):
        if self.is_run:
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
        self.sing_up_btn.clicked.connect(self.sing_up)  # sing_up버튼 눌럿을떄
        self.back_btn.clicked.connect(self.sing_up_exit)  # 취소버튼 눌럿을떄
        self.confirm_btn.clicked.connect(self.sing_up_cf)  # 확인버튼 눌럿을떄
        self.login_btn.clicked.connect(self.login) #로그인 버튼 눌럿을때

    def initUI(self):
        self.setupUi(self)
        self.sing_widget.hide()
        self.menu_widget.hide()
        self.learn_widget.hide()
        self.sing_pw.setEchoMode(QLineEdit.Password)
        self.sing_pw_2.setEchoMode(QLineEdit.Password)
        self.login_pw.setEchoMode(QLineEdit.Password)

    def sing_up(self):
        self.t1.send("@sign_up")
        self.sing_widget.show()

    def sing_up_exit(self):  # 취소버튼 눌럿을떄
        self.name.clear()
        self.sing_di.clear()
        self.sing_pw.clear()
        self.sing_pw_2.clear()
        self.sing_widget.close()

    def sing_up_cf(self): #확인 눌럿을때
        sing_check = True
        if self.sing_pw.text() != self.sing_pw_2.text():
            sing_check = False
        if not sing_check:
            pass
        else:
            self.t1.send()
            self.name.clear()
            self.sing_di.clear()
            self.sing_pw.clear()
            self.sing_pw_2.clear()
            self.sing_widget.close()

    def login(self): #로그인 버튼 눌럿을때
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Student_Window()
    sys.exit(app.exec())
