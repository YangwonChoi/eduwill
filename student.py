import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSlot
from socket import *

form_stu = uic.loadUiType("student.ui")[0]


class SocketClient(QThread):
    add_chat = QtCore.pyqtSignal(list)  # 나중에 데이터 받을때 슬롯들
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
            data = self.cnn.recv(1024)
            data = data.decode()
            print(data)

            if data.startswith('@sign_up') or data.startswith('@log_in') or data.startswith('@member'):
                self.add_user.emit(data)

    def send(self, msg):
        if self.is_run:
            self.cnn.send(f'{msg}'.encode())

    def chat(self, msg):
        if self.is_run:
            self.cnn.send(f'@caht {msg}'.encode())


class Student_Window(QMainWindow, form_stu):
    def __init__(self):
        super(Student_Window, self).__init__()
        self.initUI()
        self.t1 = SocketClient()
        self.t1.connect_cle()
        self.t1.start()
        self.show()
        # -----------------시그널-----------------------------
        self.sign_up_btn.clicked.connect(self.sign_up)  # sign_up버튼 눌렀을때
        self.back_btn.clicked.connect(self.sign_up_exit)  # 취소버튼 눌렀을때
        self.confirm_btn.clicked.connect(self.sign_up_cf)  # 확인버튼 눌렀을때
        self.login_btn.clicked.connect(self.login)  # 로그인 버튼 눌럿을때
        self.idcheck_btn.clicked.connect(self.overlap_id)  # 중복확인 버튼 눌렀을때
        self.chat_btn.clicked.connect(self.chating)  # 상담리스트 버튼 눌렀을때
        self.conect_btn.clicked.connect(self.connect_chat)  # 상담리스트 연결하기 버튼 눌렀을때
        self.exit_st.clicked.connect(self.connect_exit)  # 상담리스트 종료버튼 눌렀을때
        self.chat_exit_bt.clicked.connect(self.chat_exit)#상담(채팅) 종료버튼 눌렀을때
        self.listWidget_2.itemClicked.connect(lambda: self.conect_btn.setDisabled(False))
        self.t1.add_user.connect(self.add_user)

    def initUI(self):
        self.setupUi(self)
        self.sign_widget.hide()  # 로그인 위젯
        self.menu_widget.hide()  # 메뉴 위젯
        self.learn_widget.hide()  # 학습 위젯
        self.chat_widget.hide()  # 상담 채팅 위젯
        self.select_widget.hide()  # 상담 리스트 위젯
        self.sign_pw.setEchoMode(QLineEdit.Password)
        self.sign_pw_2.setEchoMode(QLineEdit.Password)
        self.login_pw.setEchoMode(QLineEdit.Password)

    def sign_up(self): #로그인 버튼 눌렀을때
        self.t1.send("@sign_up")
        self.sign_widget.show()

    def sign_up_exit(self):  # 취소버튼 눌럿을떄
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
            self.t1.send(
                f"{self.sign_id.text()}/{self.sign_pw.text()}/{self.name.text()}")
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
        self.select_widget.show()
        self.conect_btn.setDisabled(True)
        
    def connect_exit(self):
        self.t1.send("@exit")
        self.select_widget.hide()
        self.menu_widget.show()

    def chat_exit(self):
        self.t1.send("@exit")
        self.chat_widget.hide()
        self.select_widget.show()

    @pyqtSlot(str)
    def add_user(self, msg):
        if msg.startswith('@sign_up'):
            msg = msg.replace('@sign_up ', '', 1)

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
                self.login_id.clear()
                self.login_pw.clear()
            else:
                QMessageBox.about(self, '경고', '비밀번호가 잘못 되었습니다')
                self.login_id.clear()
                self.login_pw.clear()
        elif msg.startswith('@member'):
            msg = msg.replace('@member ', '', 1)
            self.listWidget_2.clear()
            for i in msg.split('/'):
                self.listWidget_2.addItem(i)
                print(i)
        elif msg.startswith('@chat'):
            msg = msg.replace('@chat ', '', 1)
            self.chats.append(msg)
        elif msg.startswith('@invite'):
            if msg == '@invite':
                buttonReply = QMessageBox.information(
                    self, '채팅요청', "상담요청이왔습니다.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    print('Yes clicked.')


    def connect_chat(self):
        self.chat_bro.clear()
        self.select_widget.hide()
        self.chat_widget.show()
        self.t1.send(f"@chat {self.listWidget.currentItem().text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Student_Window()
    sys.exit(app.exec())
