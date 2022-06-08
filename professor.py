import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSlot
from socket import *

form_main = uic.loadUiType("professor.ui")[0]

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
        self.cnn.send('tea'.encode())

    def recv(self):
        sys.stdout.flush()
        data = self.cnn.recv(2048)
        data = data.decode()
        return data

    def send(self, msg):
        if self.is_run:
            self.cnn.send(f'{msg}'.encode())

class Professor_Window(QMainWindow, form_main):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.t1 = SocketClient()
        self.t1.connect_cle()
        self.menu_widget.hide()
        self.show()
        self.id_check = None
#-----------------시그널-----------------------------
        self.sing_up_btn.clicked.connect(self.sing_up)
        self.back_btn.clicked.connect(self.sing_up_exit)
        self.confirm_btn.clicked.connect(self.sing_up_cf)
        self.login_btn.clicked.connect(self.login)  # 로그인 버튼 눌럿을때
        self.idcheck_btn.clicked.connect(self.overlap_id)

    def initUI(self):
        self.setupUi(self)
        self.sing_widget.hide()
        self.sing_pw.setEchoMode(QLineEdit.Password)
        self.sing_pw_2.setEchoMode(QLineEdit.Password)
        self.login_pw.setEchoMode(QLineEdit.Password)
        self.login_btn.clicked.connect(self.login)


    def sing_up(self):
        self.t1.send("@sign_up")
        self.sing_widget.show()

    def sing_up_exit(self):
        self.t1.send('@exit')
        self.sing_di.setDisabled(False)
        self.idcheck_btn.setDisabled(False)
        self.name.clear()
        self.sing_di.clear()
        self.sing_pw.clear()
        self.sing_pw_2.clear()
        self.sing_widget.close()
    def overlap_id(self):
        id = self.sing_di.text()
        sys.stdin.flush()
        self.t1.send(id)
        msg = self.t1.recv()

        if msg == 'OK':
            self.id_check = True
            QMessageBox.about(self, '중복', '사용 가능한 아이디 입니다')
            self.sing_di.setDisabled(True)
            self.idcheck_btn.setDisabled(True)

        elif msg == 'NO':
            self.id_check = False
            QMessageBox.about(self, '중복', '중복된 아이디 입니다')
            self.sing_di.setDisabled(False)
            self.idcheck_btn.setDisabled(False)
        else:
            self.id_check = False
    def sing_up_cf(self):
        sing_check = True
        if self.sing_pw.text() != self.sing_pw_2.text():
            sing_check = False
        if not self.id_check:
            sing_check = False

        if not sing_check:
            pass
        else:

            self.t1.send(f"{self.sing_di.text()}/{self.sing_pw.text()}/{self.name.text()}")
            self.name.clear()
            self.sing_di.clear()
            self.sing_pw.clear()
            self.sing_pw_2.clear()
            self.sing_widget.close()

    def login(self):  # 로그인 버튼 눌럿을때
        self.t1.send(f"@log_in/{self.login_id.text()}/{self.login_pw.text()}")
        check = self.t1.recv()
        print(check)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Professor_Window()
    sys.exit(app.exec())

