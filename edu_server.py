import socket
import threading
import sqlite3
import sys


PORT = 2090
BUF_SIZE = 1024
lock = threading.Lock()
clnt_imfor = []  # [sock, id, type, state]
clnt_cnt = 0


def get_DBcursor():
    con = sqlite3.connect('edu.db')  # DB open
    c = con.cursor()  # 커서 획득
    return (con, c)


def recv_clnt_msg(clnt_sock):
    sys.stdout.flush()  # 버퍼 비우기
    clnt_msg = clnt_sock.recv(BUF_SIZE)  # 메세지 받아오기
    clnt_msg = clnt_msg.decode()  # 디코딩
    return clnt_msg


def send_clnt_msg(clnt_sock, msg):
    sys.stdin.flush()  # 버퍼 비우기
    msg = msg.encode()  # 인코딩
    clnt_sock.send(msg)  # 메세지 보내기


def delete_imfor(clnt_sock):
    global clnt_cnt
    for i in range(0, clnt_cnt):
        if clnt_sock == clnt_imfor[i][0]:  # 해당 소켓 가진 클라이언트 정보 찾기
            print('exit client')
            while i < clnt_cnt - 1:  # 그 뒤에 있는 클라이언트 정보들을 한 칸씩 앞으로 당겨옴
                clnt_imfor[i] = clnt_imfor[i + 1]
                i += 1
            break
    clnt_cnt -= 1


def sign_up(clnt_num):
    print('dd')
    con, c = get_DBcursor()
    clnt_sock = clnt_imfor[clnt_num][0]
    type = clnt_imfor[clnt_num][2]

    while True:
        check = 0
        check_id = recv_clnt_msg(clnt_sock)
        if check_id == "exit":  # 클라이언트에서 회원가입창 닫을 시 return
            con.close()
            break

        if type == 'stu':  # 학생/선생 table 열어서 id 가져옴
            c.execute("SELECT ID FROM studentTBL")
        elif type == 'tea':
            c.execute("SELECT ID FROM teacherTBL")
        else:
            print('type error in sign_up')
            con.close()
            return
        for row in c:                               # id 중복시 NO send
            if check_id in row:
                send_clnt_msg(clnt_sock, 'NO')
                check = 1
                break
        if check == 1:
            continue
        send_clnt_msg(clnt_sock, 'OK')  # 중복 아닐시 OK sende

        user_data = recv_clnt_msg(clnt_sock)  # id포함 회원가입 데이터 받아옴(구분자 : /)
        if user_data == 'exit':
            con.close()
            return
        user_data = user_data.split('/')
        print(user_data)
        lock.acquire()
        if type == 'stu':  # 학생/선생 맞춰서 table에 데이터 저장
            c.executemany(
                "INSERT INTO studentTBL(ID, PW, Name) VALUES(?, ?, ?)", (user_data,))
        elif type == 'tea':
            c.executemany(
                "INSERT INTO teacherTBL(ID, PW, Name) VALUES(?, ?, ?)", (user_data,))
        else:
            print('type error2 in sign_up')
            con.close()
            return
        con.commit()
        con.close()
        lock.release()
        return


def log_in(clnt_num, log_in_data):
    print(log_in_data)
    con, c = get_DBcursor()
    clnt_sock = clnt_imfor[clnt_num][0]
    type = clnt_imfor[clnt_num][2]
    log_in_data = log_in_data.split('/')  # log_in_data = 'log_in/ID/PW'
    check_id = log_in_data[1]
    check_pw = log_in_data[2]

    if type == 'stu':  # table에서 id 가져오기
        c.execute('SELECT PW FROM studentTBL WHERE ID=?', (check_id,))
    elif type == 'tea':
        c.execute('SELECT PW FROM teacherTBL WHERE ID=?', (check_id,))
    else:
        print('type error in log_in')
        con.close()
        return
    pw = c.fetchone()
    if not c:  # 해당 id 없을시 @ID error
        send_clnt_msg(clnt_sock, 'ID error')
        con.close()
        return
    else:  # 해당 id에 대한 pw 일치 시 @sucess send 및 clnt_imfor 갱신
        if (check_pw,) == pw:
            send_clnt_msg(clnt_sock, 'sucess')
            clnt_imfor[clnt_num][1] = check_id
            clnt_imfor[clnt_num][3] = 1
            print('login %s, %s' % (type, check_id))
            con.close()
        else:  # id는 있지만 pw 불일치시 @PW error
            send_clnt_msg(clnt_sock, 'PW error')
            con.close()
    return


def QA_ctrl_func(clnt_num):  # Q&A 관련 함수 작성중
    con, c = get_DBcursor()
    type = clnt_imfor[clnt_num][2]
    if type == 'stu':
        c.execute('SELECT * FROM Q&ATBL WHERE ID=?', (clnt_imfor[clnt_num][1],))
        rows = c.fetchall()
        if not c:  #등록된 질문 없을 시 X send
            send_clnt_msg(clnt_imfor[clnt_num][0], 'X')
        else:  #질문 등록돼있으면 리스트 다 보내줌
            for row in rows:
                row = list(row)
                row[0] = str(row[0])
                row = '/'.join(row)
                send_clnt_msg(clnt_imfor[clnt_num][0], row)
            send_clnt_msg(clnt_imfor[clnt_num][0], 'done')
        while True:  #클라이언트에서 quit 보내기 전 까지 계속 질문 받음
            msg = recv_clnt_msg(clnt_imfor[clnt_num][0])
            if msg == 'quit':
                con.close()
                return
            else:
                msg = msg.split('/')
                c.executemany('INSERT INTO Q&ATBL(ID, Date, Question) VALUES(?, ?, ?)', (msg,))
                con.commit()
                con.close()
    elif type == 'tea':
        c.execute('SELECT * FROM Q&ATBL')
        rows = c.fetchall()
        if not c:  #등록된 질문 없을 시 X send
            send_clnt_msg(clnt_imfor[clnt_num][0], 'X')
            con.close()
            return
        else:
            for row in rows:
                row = list(row)
                row[0] = str(row[0])
                row = '/'.join(row)
                send_clnt_msg(clnt_imfor[clnt_num][0], row)
            send_clnt_msg(clnt_imfor[clnt_num][0], 'done')
        while True:
            msg = recv_clnt_msg(clnt_imfor[clnt_num][0])
            if msg == 'quit':
                con.close()
                break
            else:
                answer = msg.split('/')
                num = int(answer[0])
                c.execute('UPDATE Q&ATBL SET Answer=? WHERE No=?', (num, answer[1]))
                con.commit()
    else:
        print('type error in QA')
        con.close()
        return


def set_questions(clnt_num, question):  # 문제출제 함수
    question = question.split('/')
    question.remove('set_q')
    con, c = get_DBcursor()
    if clnt_imfor[clnt_num][2] != 'tea':  # 선생 아니면 문제출제 불가 예외처리
        print('student cant set questions')
        con.close()
        return
    else:  # 과목/문제/정답 삽입
        lock.acquire
        c.executemany(
            "INSERT INTO quizTBL(Subject, Quiz, Answer) VALUES(?, ?, ?)", (question,))
        con.commit()
        con.close()
        lock.release()
    return


def get_chat(clnt_num):
    con, c = get_DBcursor()
    type = clnt_imfor[clnt_num][2]
    if type == 'stu':  # 학생/선생 table 열어서 id 가져옴
        c.execute("SELECT Name FROM studentTBL WHERE ID=?", (clnt_imfor[clnt_num][1]))
    elif type == 'tea':
        c.execute("SELECT Name FROM teacherTBL WHERE ID=?", (clnt_imfor[clnt_num][1]))
    else:
        print('type error in get_chat')
        return
    clnt_name = c.fetchone()
    clnt_name = ''.join(clnt_name)
    
    while True:
        msg = recv_clnt_msg(clnt_imfor[clnt_num][0])
        if msg == 'quit':
            clnt_imfor[clnt_num][3] = 1
            break
        else:
            for i in range(0, clnt_cnt):
                if clnt_imfor[clnt_num][3] == clnt_imfor[i][3]:
                    send_clnt_msg(clnt_imfor[i][0], (clnt_name + msg))
    con.close()
    return


def set_chat_state(clnt_num):           #수정 필요
    con, c = get_DBcursor()
    if clnt_imfor[clnt_num][2] == 'stu':  # 학생이 채팅요청 했을 경우
        c.execute('SELECT Teacher FROM studentTBL WHERE ID=?',
                  (clnt_imfor[clnt_num][1]))  # 해당 학생의 담당선생님 id 추출
        teacher = c.fetchone()
        teacher = ''.join(teacher)
        teacher.split('|')
        lock.acquire()
        for i in range(0, len(clnt_imfor)):  # 선생 id 접속중이면 채팅요청 보냄
            if teacher[0] == clnt_imfor[i][1]:
                if clnt_imfor[i][3] == 1:
                    send_clnt_msg(
                        clnt_imfor[i][0], ('@plz_chat/%s' % clnt_imfor[clnt_num][1]))
                    clnt_imfor[i][3] = 2
                    clnt_imfor[clnt_num][3] = 2
                    get_chat(clnt_num)
                    con.close()
                    return
                else:  # 해당 선생 채팅중이면 채팅중 send
                    send_clnt_msg(clnt_imfor[clnt_num][0], 'teacher_chatting')
                    con.close()
                    return
        lock.release()
        # 해당 선생 접속중 아니면 offline send
        send_clnt_msg(clnt_imfor[clnt_num, 'offline_teacher'])
        con.close()
        return
    return


def call_func(clnt_num, instruction):
    if instruction == 'sign_up':
        sign_up(clnt_num)
    elif instruction.startswith('log_in'):
        log_in(clnt_num, instruction)
    elif instruction.startswith('set_q'):
        set_questions(clnt_num, instruction)
    elif instruction.startswith('Q&A'):
        QA_ctrl_func(clnt_num)
    elif instruction == 'chat':
        set_chat_state(clnt_num, instruction)
    else:
        return


def handle_clnt(clnt_sock):
    lock.acquire()
    for i in range(0, clnt_cnt):                # clnt_imfor에 해당 클라이언트가 몇 번째에 있는지 추출
        if clnt_imfor[i][0] == clnt_sock:
            clnt_num = i
            break
    lock.release()

    while True:
        clnt_msg = recv_clnt_msg(clnt_sock)
        if not clnt_msg:                        # 클라이언트 연결 끊길 시
            lock.acquire()
            delete_imfor(clnt_sock)
            lock.release()
            break

        if clnt_msg.startswith('@'):            # 특정 기능 실행 시 @ 붙여서 받음
            clnt_msg = clnt_msg.replace('@', '')
            call_func(clnt_num, clnt_msg)       # 명령어 함수 호출하는 함수
        else:
            continue


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', PORT))
    sock.listen(5)

    while True:
        clnt_sock, addr = sock.accept()
        clnt_msg = recv_clnt_msg(clnt_sock)

        lock.acquire()
        clnt_imfor.insert(clnt_cnt, [clnt_sock, '!log_in', clnt_msg, 0])
        clnt_cnt += 1
        print('connect client, type %s' % clnt_msg)
        lock.release()

        t = threading.Thread(target=handle_clnt, args=(clnt_sock,))
        t.start()
