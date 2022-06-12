import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSlot
from socket import *

form_main = uic.loadUiType("professor.ui")[0]

class SocketClient(QThread):  # 서버와 클라이언트 그리고 서버에서 받은 메세지와 메인 구동클래스를 연결시켜주는 클래스
    add_user = QtCore.pyqtSignal(str) # pyqt5 solot을 이용한 클래스 객체

    def __init__(self, parent=None):
        super().__init__()
        self.main = parent
        self.is_run = False

    def connect_cle(self):
        self.cnn = socket(AF_INET, SOCK_STREAM)
        self.cnn.connect(('localhost', 2090))
        self.is_run = True
        self.cnn.send('tea'.encode())

    def run(self): # recv받는 스레드
        while True:
            data = self.cnn.recv(1024)
            data = data.decode()

            if data.startswith('@sign_up') or data.startswith('@log_in') or data.startswith('@member') or data.startswith('@chat') or data.startswith('@list_q') or data.startswith('@invite'):
                self.add_user.emit(data) #구동클래스에 데이터 전달
                print("커멘드메세지",data)

            else:
                print('이상한메세지',data)

    def send(self, msg): #서버에 데이터 전달
        if self.is_run:
            self.cnn.send(f'{msg}'.encode())
            print('보낸메세지 ',msg)

class Professor_Window(QMainWindow, form_main):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.t1 = SocketClient(self)
        self.t1.connect_cle()
        self.menu_widget.hide()
        self.select_widget.hide()
        self.chat_widget.hide()
        self.quiz_widget.hide()
        self.make_widget.hide()
        self.sign_widget.hide()
        self.row = 1
        self.t1.start()
        self.show()
        self.id_check = None
#-----------------시그널-----------------------------
        self.sign_up_btn.clicked.connect(self.sign_up) #회원가입 버튼을 누를시
        self.back_btn.clicked.connect(self.sign_up_exit) #뒤로가기 버튼을 누를시
        self.confirm_btn.clicked.connect(self.sign_up_cf) #회원가입확인 버튼을 누를시
        self.login_btn.clicked.connect(self.login)  # 로그인 버튼 누를시
        self.idcheck_btn.clicked.connect(self.overlap_id) #중복확인 버튼을 누를시
        self.chat_btn.clicked.connect(self.chating) #메뉴에서 채팅버튼을 누를시
        self.t1.add_user.connect(self.add_user) # 중요 q스레드 클래스와 메인클래스를 연결시키는 시그널
        self.exit_st.clicked.connect(self.connect_exit) #종료버튼을 누를시
        self.conect_btn.clicked.connect(self.connect_chat)
        self.listWidget.itemClicked.connect(lambda: self.conect_btn.setDisabled(False))
        self.chat_exit_bt.clicked.connect(self.connect_exit)
        self.quiz_btn.clicked.connect(self.quiz_time) #qiuz 버튼 누를시
        self.back_btn_2.clicked.connect(self.quiz_back)
        self.sub_btn.clicked.connect(self.send_quiz)
        self.surv_radiobtn.clicked.connect(lambda :self.radio_check(self.surv_radiobtn.text()))
        self.land_radiobtn.clicked.connect(lambda :self.radio_check(self.land_radiobtn.text()))
        self.char_radiobtn.clicked.connect(lambda :self.radio_check(self.char_radiobtn.text()))
        self.backback_btn.clicked.connect(self.hide)
        self.send_btn.clicked.connect(self.send_serv)
        self.send_btn_2.clicked.connect(self.send_chat_msg)

    def initUI(self):
        self.setupUi(self)
        self.sign_pw.setEchoMode(QLineEdit.Password) #비밀번호 출력 암호화
        self.sign_pw_2.setEchoMode(QLineEdit.Password)
        self.login_pw.setEchoMode(QLineEdit.Password)
        self.listWidget_2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch) #문제풀기 기능에서 테이블위젯의 컬럼의 비율

    def sign_up(self): # 회원가입 버튼 누를때 서버에 상황전달
        self.t1.send("@sign_up")
        self.sign_widget.show()

    def sign_up_exit(self): #종료 버튼누를시 화원가입 위젯 초기화
        self.t1.send('exit')
        self.sign_id.setDisabled(False)
        self.idcheck_btn.setDisabled(False)
        self.name.clear()
        self.sign_id.clear()
        self.sign_pw.clear()
        self.sign_pw_2.clear()
        self.sign_widget.close()
    def overlap_id(self): #중복체크 버튼을 누를시 아이디 서버에 전송
        id = self.sign_id.text()
        sys.stdin.flush()
        self.t1.send(id)

    def sign_up_cf(self): #확인 버튼 누를시 정규식 검사
        sign_check = True
        if self.sign_pw.text() != self.sign_pw_2.text(): #비밀번호 확인
            sign_check = False
        if not self.id_check: #아이디 충복체크
            sign_check = False

        if not sign_check: #정규식 통과 못할시
            QMessageBox.about(self, '경고', '잘못된 양식 입니다')
        else: #정규식 통과

            self.t1.send(f"{self.sign_id.text()}/{self.sign_pw.text()}/{self.name.text()}")
            self.name.clear()
            self.sign_id.clear()
            self.sign_pw.clear()
            self.sign_pw_2.clear()
            self.sign_widget.close()

    def login(self):  # 로그인 버튼 눌럿을때 서버에 아이디 비밀번호 전달
        self.t1.send(f"@log_in/{self.login_id.text()}/{self.login_pw.text()}")

    def chating(self): # 메뉴에서 채팅버튼 누를시 서버에 현재 접속된 학생 요청
        self.menu_widget.hide()
        self.t1.send("@member")

        self.conect_btn.setDisabled(True)
        self.select_widget.show()

    def connect_exit(self):
        self.t1.send("@exit")
        self.select_widget.hide()
        self.chat_widget.hide()
        self.menu_widget.show()

    @pyqtSlot(str)
    def add_user(self, msg):

        if msg.startswith('@sign_up'):
            msg = msg.replace('@sign_up ', '', 1)

            if msg == 'OK': # 중복체크 통과시
                self.id_check = True
                QMessageBox.about(self, '중복', '사용 가능한 아이디 입니다')
                self.sign_id.setDisabled(True)
                self.idcheck_btn.setDisabled(True) # 버튼비활성화
            elif msg == 'NO': # 중복체크 통과못할시
                self.id_check = False
                QMessageBox.about(self, '중복', '중복된 아이디 입니다')
                self.sign_id.setDisabled(False)
                self.idcheck_btn.setDisabled(False)
            else:
                self.id_check = False
        elif msg.startswith('@log_in'):
            msg = msg.replace('@log_in ', '', 1)
            if msg == 'sucess': #로그인 성공시
                self.login_widget.hide()
                self.menu_widget.show()
            elif msg == 'ID error': #ID 잘못입력했을때
                QMessageBox.about(self, '경고', '아이디가 잘못 되었습니다')

            else: #PW 잘못입력했을때
                QMessageBox.about(self, '경고', '비밀번호가 잘못 되었습니다')
            self.login_id.clear()
            self.login_pw.clear()
        elif msg.startswith('@member'):
            msg = msg.replace('@member ', '', 1)
            self.listWidget.clear()
            for i in msg.split('/'):
                self.listWidget.addItem(f'{i}')
        elif msg.startswith('@chat'):
            msg = msg.replace('@chat ', '', 1)
            self.chat_bro_2.append(msg)
        elif msg.startswith('@list_q'):
            msg = msg.replace('@list_q ', '', 1)

            for i in msg.split("@list_q "): #클라이언트에서 처리가 늦어 버퍼가 이어서 들어올때 나눠줘야한다
                if i == "done" or i == "empty":
                    self.row = 1 # done이 출력되면 카운트 초기화
                    break

                self.listWidget_2.setRowCount(self.row) #문제 갯수대로 열생성
                self.listWidget_2.setItem(self.row-1, 0, QTableWidgetItem(i.split("/")[2]))
                self.listWidget_2.setItem(self.row-1, 1, QTableWidgetItem(i.split("/")[3]))
                self.row += 1 #문제 갯수 카운트

        elif msg.startswith('@invite'):
            if msg == "@invite":
                buttonReply = QMessageBox.information(self, '상담요청', "상담할래?", QMessageBox.Yes | QMessageBox.No)

                if buttonReply == QMessageBox.Yes:
                    self.t1.send('@invite OK')
                    self.chat_bro_2.clear()
                    self.menu_widget.hide()
                    self.chat_widget.show()
                else:
                    self.t1.send('@invite NO')


    def closeEvent(self, event):
        self.t1.send("@exit")
        event.accept()

    def connect_chat(self):
        self.chat_bro_2.clear()
        self.t1.send(f"@chat/{self.listWidget.currentItem().text()}")
        self.select_widget.hide()
        self.chat_widget.show()


    def send_chat_msg(self): # 메세지 서버에 전송
        self.t1.send(f"@chat {self.chat_input_2.text()}")
        self.chat_input_2.clear()


    def quiz_time(self): #quiz버튼을 누를시
        self.menu_widget.hide()
        self.listWidget_2.clearContents()

        self.t1.send(f"@list_q/{self.surv_radiobtn.text()}")
        self.quiz_widget.show()

    def send_serv(self): #문제출제하기버튼 눌렀을 때
        radio = [self.surv_radiobtn,self.land_radiobtn,self.char_radiobtn]
        for i in radio: #라디오버튼 체크항목
            if i.isChecked():
                table = i.text()
                break
        quiz = self.lineEdit.text()
        answer = self.lineEdit_2.text()
        self.t1.send(f'@set_q/{table}/{quiz}/{answer}') #서버에 테이블/문제/답 전송
        self.lineEdit.clear()
        self.lineEdit_2.clear()

    def radio_check(self, a):
        self.listWidget_2.clearContents()
        self.t1.send(f"@list_q/{a}")

    def send_quiz(self):
        self.make_widget.show()

    def quiz_back(self):
        self.quiz_widget.hide()
        self.menu_widget.show()

    def hide(self): #back버튼 누를시 제출한 내용 보여주기
        self.make_widget.hide()
        radio = [self.surv_radiobtn, self.land_radiobtn, self.char_radiobtn]
        for i in radio:
            if i.isChecked():
                table = i.text()
                break

        self.t1.send(f"@list_q/{table}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Professor_Window()
    win.setWindowTitle('교수')
    sys.exit(app.exec())