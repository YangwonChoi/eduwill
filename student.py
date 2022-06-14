import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSlot
from socket import *
import sqlite3
import datetime
from PyQt5.QtGui import *


form_stu = uic.loadUiType("student.ui")[0]

#DB 연결, 커서획득 함수
def get_DBcursor():
    con = sqlite3.connect('clntDB')  # DB open
    c = con.cursor()  # 커서 획득
    return (con, c)

class SocketClient(QThread): # Q쓰레드 클래스 선언
    add_chat = QtCore.pyqtSignal(list)  # 나중에 데이터 받을때 슬롯들
    add_user = QtCore.pyqtSignal(str)

    def __init__(self, parent=None): 
        super().__init__()
        self.main = parent
        self.is_run = False

    def connect_cle(self): #소켓연결
        self.cnn = socket(AF_INET, SOCK_STREAM)
        self.cnn.connect(('localhost', 2090))
        self.is_run = True
        self.cnn.send('stu'.encode())

    def run(self):
        while True:
            data = self.cnn.recv(1024)
            data = data.decode()
            print(data)

            if data.startswith('@sign_up') or data.startswith('@log_in') or data.startswith('@member') or data.startswith('@chat') or data.startswith('@set_q') or data.startswith('@invite') or data.startswith("@QnA"):
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
        self.chat_exit_bt.clicked.connect(self.chat_exit)  # 상담 종료버튼 눌렀을때
        self.listWidget_2.itemClicked.connect(lambda: self.conect_btn.setDisabled(False))
        self.t1.add_user.connect(self.add_user)
        self.send_btn.clicked.connect(self.chat_send) # 상담 보내기 버튼 눌렀을때
        self.learn_btn.clicked.connect(self.lean_title) # 학습 버튼 눌렀을때
        self.title_btn.clicked.connect(self.lean_dino) # 공룡 버튼 눌렀을때
        self.lean_exit_btn.clicked.connect(self.lean_exit) # 학습 종료버튼 눌렀을때
        self.listWidget.itemClicked.connect(self.item_clicked)
        self.qa_btn.clicked.connect(self.send_qna)###########현성
        self.qn_back_btn.clicked.connect(self.qna_back)
        self.qn_anser_btn.clicked.connect(self.answer_qna)
        self.anser_back.clicked.connect(self.answer_back)
        self.reg_btn.clicked.connect(self.q_a_reg)

    def initUI(self):
        self.setupUi(self)
        self.sign_widget.hide()  # 로그인 위젯
        self.menu_widget.hide()  # 메뉴 위젯
        self.learn_widget.hide()  # 학습 위젯
        self.lean_menu_widget.hide() # 학습주제 위젯
        self.chat_widget.hide()  # 상담 채팅 위젯
        self.select_widget.hide()  # 상담 리스트 위젯
        self.dino_widget.hide() # 학습 위젯
        self.widget_2.hide()################################
        self.qn_widget.hide()
        self.widget.hide()
        self.quiz_widget.hide()#####################################
        self.sign_pw.setEchoMode(QLineEdit.Password)
        self.sign_pw_2.setEchoMode(QLineEdit.Password)
        self.login_pw.setEchoMode(QLineEdit.Password)
        self.tableWidget.setColumnWidth(0, 590)  # 컬럼 크기맞추기
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(1, 146)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("dino.png")))
        self.setPalette(palette)
        self.learn_btn.setStyleSheet("""
                QPushButton {
                color: rgb(68, 255, 0);
                    background-image : url(ss.png); 
                }
                QPushButton:hover {
                    background-image : url(ssdd.png);
                }
                QPushButton:pressed{
        background-image : url(ssdds.png);}

            """)
        self.quiz_btn.setStyleSheet("""
                        QPushButton {
                        color: rgb(68, 255, 0);
                            background-image : url(ss.png); 
                        }
                        QPushButton:hover {
                            background-image : url(ssdd.png);
                        }
                        QPushButton:pressed{
                background-image : url(ssdds.png);}

                    """)
        self.qa_btn.setStyleSheet("""
                        QPushButton {
                        color: rgb(68, 255, 0);
                            background-image : url(ss.png); 
                        }
                        QPushButton:hover {
                            background-image : url(ssdd.png);
                        }
                        QPushButton:pressed{
                background-image : url(ssdds.png);}

                    """)
        self.chat_btn.setStyleSheet("""
                        QPushButton {
                            color: rgb(68, 255, 0);
                            background-image : url(ss.png); 
                        }
                        QPushButton:hover {
                            background-image : url(ssdd.png);
                        }
                        QPushButton:pressed{
                background-image : url(ssdds.png);}

                    """)
        # ---------------------------------------------------------------------
        

    def sign_up(self):  #회원가입 버튼 눌렀을때
        self.t1.send("@sign_up")
        self.sign_widget.show()

    def sign_up_exit(self):  #회원가입 취소버튼 눌럿을떄
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
        self.ID = self.login_id.text()

    def chating(self): #상담버튼 눌렀을때
        self.menu_widget.hide()
        self.t1.send("@member")
        self.select_widget.show()
        self.conect_btn.setDisabled(True)

    def connect_exit(self): # 상담리스트 종료버튼 눌렀을때
        self.t1.send("@exit")
        self.select_widget.hide()
        self.menu_widget.show()

    def chat_exit(self): # 상담 종료버튼 눌렀을때
        self.t1.send("@exit")
        self.chat_widget.hide()
        self.select_widget.show()

    def chat_send(self): #상담 보내기버튼 눌렀을때
        self.t1.send(f"@chat {self.chat_input.text()}")
        self.chat_input.clear()

    def lean_title(self):
        self.menu_widget.hide()
        self.learn_widget.show()
        self.lean_menu_widget.show()
        print("주제선택")

    def lean_dino(self):
        self.lean_menu_widget.hide()
        self.dino_widget.show()
        con, c = get_DBcursor()
        c.execute("SELECT 한글명 FROM study")
        rows = c.fetchall()
        rows = list(rows)
        for row in rows:
            row = list(row)
            self.listWidget.addItem(f'{row[0]}')
        con.close()
        print("학습창")

    def lean_exit(self):
        self.learn_widget.hide()
        self.dino_widget.hide()
        self.menu_widget.show()
        print("학습종료")



    def item_clicked(self):

        con, c = get_DBcursor()
        c.execute("SELECT * FROM study where 한글명 = ?", (self.listWidget.currentItem().text(),))
        rows = c.fetchone()
        rows =list(rows)
        self.dino_num.setText(rows[0])
        self.kor_name.setText(rows[1])
        self.eng_name.setText(rows[2])
        self.dino_t.setText(rows[3])
        self.dino_f.setText(rows[4])
        self.dino_w.setText(rows[5])
        self.dino_d.setText(rows[6])
        self.dino_a.setText(rows[7])
        self.dino_type.setText(rows[9])
        self.dino_info.setText(rows[8])

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
            self.chat_bro.append(msg)
        elif msg.startswith('@invite'):
            if msg == '@invite':
                buttonReply = QMessageBox.information(self, '채팅요청', "상담요청이 왔습니다.", QMessageBox.Yes | QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    self.t1.send('@invite OK')
                    self.chat_widget.show()
        elif msg.startswith('@QnA'):
            msg = msg.replace('@QnA ', '', 1)

            for i in msg.split('@QnA '):
                if i == "done" or i == "empty":
                    break

                self.tableWidget.setRowCount(int(i.split('/')[0]))  # 문제 갯수대로 열생성
                self.tableWidget.setItem(int(i.split('/')[0]) - 1, 0, QTableWidgetItem(i.split("/")[3]))
                self.tableWidget.setItem(int(i.split('/')[0]) - 1, 3, QTableWidgetItem(i.split("/")[2]))
                self.tableWidget.setItem(int(i.split('/')[0]) - 1, 1, QTableWidgetItem(i.split("/")[1]))
                self.tableWidget.setItem(int(i.split('/')[0]) - 1, 2, QTableWidgetItem(i.split("/")[4]))

    def connect_chat(self): # 상담 연결하기 버튼 눌렀을때
        self.chat_bro.clear()
        self.select_widget.hide()
        self.chat_widget.show()
        self.t1.send(f"@chat/{self.listWidget_2.currentItem().text()}")
        print(self.listWidget_2.currentItem().text())

    def send_qna(self):
        self.menu_widget.hide()
        self.qn_widget.show()
        self.t1.send("@QnA")

    def qna_back(self):
        self.qn_widget.hide()
        self.menu_widget.show()
        self.t1.send("@exit")

    def answer_qna(self):
        self.widget_2.show()
        self.qn_widget.hide()
        self.menu_widget.hide()

    def answer_back(self):
        self.widget_2.hide()
        self.lineEdit.clear()
        self.qn_widget.show()

    def q_a_reg(self):
        self.t1.send(f"{self.login_id.text()}/{datetime.datetime.now().date()}/{self.lineEdit.text()}")
        self.widget_2.hide()
        self.lineEdit.clear()
        self.qn_widget.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Student_Window()
    win.setWindowTitle('학생')
    sys.exit(app.exec())
