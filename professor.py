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
    def run(self):
        while True:
            data = self.cnn.recv(1024)
            data = data.decode()
            print(data)

            if data.startswith('@sign_up') or data.startswith('@log_in'):
                self.add_user.emit(data)


            else:
                self.add_chat.emit(data)


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
        self.select_widget.hide()
        self.chat_widget.hide()
        self.t1.start()

        self.show()
        self.id_check = None
#-----------------시그널-----------------------------
        self.sign_up_btn.clicked.connect(self.sign_up)
        self.back_btn.clicked.connect(self.sign_up_exit)
        self.confirm_btn.clicked.connect(self.sign_up_cf)
        self.login_btn.clicked.connect(self.login)  # 로그인 버튼 눌럿을때
        self.idcheck_btn.clicked.connect(self.overlap_id)
        self.chat_btn.clicked.connect(self.chating)
        self.t1.add_user.connect(self.add_user)

    def initUI(self):
        self.setupUi(self)
        self.sign_widget.hide()
        self.sign_pw.setEchoMode(QLineEdit.Password)
        self.sign_pw_2.setEchoMode(QLineEdit.Password)
        self.login_pw.setEchoMode(QLineEdit.Password)



    def sign_up(self):
        self.t1.send("@sign_up")
        self.sign_widget.show()

    def sign_up_exit(self):
        self.t1.send('@exit')
        self.sign_id.setDisabled(False)
        self.idcheck_btn.setDisabled(False)
        self.name.clear()
        self.sign_id.clear()
        self.sign_pw.clear()
        self.sign_pw_2.clear()
        self.sign_widget.close()
    def overlap_id(self):
        id = self.sign_id.text()
        sys.stdin.flush()
        self.t1.send(id)

    def sign_up_cf(self):
        sign_check = True
        if self.sign_pw.text() != self.sign_pw_2.text():
            sign_check = False
        if not self.id_check:
            sign_check = False

        if not sign_check:
            QMessageBox.about(self, '경고', '잘못된 양식 입니다')
        else:

            self.t1.send(f"{self.sign_id.text()}/{self.sign_pw.text()}/{self.name.text()}")
            self.name.clear()
            self.sign_id.clear()
            self.sign_pw.clear()
            self.sign_pw_2.clear()
            self.sign_widget.close()

    def login(self):  # 로그인 버튼 눌럿을때
        self.t1.send(f"@log_in/{self.login_id.text()}/{self.login_pw.text()}")

    def chating(self):
        self.menu_widget.hide()
        self.t1.send("@member")
        #리시브받아서 리스트위젯에 넣어야함
        self.select_widget.show()

    @pyqtSlot(str)
    def add_user(self, msg):
        print(msg)
        if msg.startswith('@sign_up'):
            msg = msg.replace('@sign_up ', '', 1)
            print(msg)
            if msg == 'OK':
                self.id_check = True
                QMessageBox.about(self, '중복', '사용 가능한 아이디 입니다')
                self.sign_id.setDisabled(True)
                self.idcheck_btn.setDisabled(True)
            elif msg == 'NO':
                self.id_check = False
                QMessageBox.about(self, '중복', '중복된 아이디 입니다')
                self.sign_id.setDisabled(False)
                self.idcheck_btn.setDisabled(False)
            else:
                self.id_check = False
        elif msg.startswith('@log_in'):
            msg = msg.replace('@log_in ', '', 1)
            if msg == 'sucess':
                self.login_widget.hide()
                self.menu_widget.show()
            elif msg == 'ID error':
                QMessageBox.about(self, '경고', '아이디가 잘못 되었습니다')

            else:
                QMessageBox.about(self, '경고', '비밀번호가 잘못 되었습니다')
            self.login_id.clear()
            self.login_pw.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Professor_Window()
    sys.exit(app.exec())

