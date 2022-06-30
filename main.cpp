#include <iostream>
#include <string>
#include <fstream>
#include "sqlite3.h"
using namespace std;
int num;
int main_num;
string id;
string pw;
string login_id;
string login_pw;
string str;


int main()
{

    string line;
    ifstream file("/home/sss/바탕화면/book.csv");
    if(file. is_open()){
        while(getline(file, line)){
        //    cout << line << endl;
        }
        // file.close();
    }
    sqlite3* db;
    int rc = sqlite3_open(":/home/sss/바탕화면.DB.db:", &db);
    string str = "select * from book limit 5;";

    cout << rc <<endl;
    cout << "메인화면\n";
    cout << "1. 로그인\n2. 회원가입\n";
    cout << "번호를 선택해주세요: _\b";
    cin >> num;

    if (num == 2)
        cout << "---------회원가입---------\n";
        cout << "ID :__________\b\b\b\b\b\b\b\b\b";
        cin >> id;
        cout << "PW :_________\b\b\b\b\b\b\b\b";
        cin >> pw;


    if (num == 1)
        cout << "---------로그인---------\n";
        cout << "ID :__________\b\b\b\b\b\b\b\b\b";
        cin >> login_id;
        if (id != login_id)
            cout << "잘못된 아이디 입니다.\n";
        cout << "PW :_________\b\b\b\b\b\b\b\b";
        cin >> login_pw;
        if (pw != login_pw)
            cout << "잘못된 패스워드 입니다.\n";
            else
            cout << "----------welcome----------\n";
            cout << "---------도서관---------\n";
//             string rand_book =
            cout << "번호를 선택해주세요:\n";
            cout << "1. 조회하기\n2. 대여하기\n3. 반납하기\n";
            cin >> main_num;
            if (main_num == 1){
                cout << "---------조회하기---------\n";
                cout << "도서를 입력해주세요:\n";
                cin >> str;
                if (file.is_open()){
                    while (file.eof()){
//                        cout << "123";
                        line.find(str);

                    }
                }
            file.close() ;
            }
            else if (main_num == 2){
                cout << "---------대여하기---------\n";
            }
            else if (main_num == 3){
                cout << "---------반납하기---------\n";
            }



    return 0;
}