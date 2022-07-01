#include <iostream>
#include <string>
#include <fstream>
#include "sqlite3.h"

using namespace std;
int num;
int main_num;
int search_num;
string id;
string pw;
string login_id;
string login_pw;
string bookname;
int join();
int login();
int search();
int callback(void *, int, char , char );



//int callback(void *, int, char , char );
//int callback(
//        void *NotUsed,
//        int argc,
//        char argv,
//        char azColName)
//{
//    NotUsed = 0;
//
//    for (int i = 0; i < argc; i++)
//    {
//        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
//    }
//
//    printf("\n");
//
//    return 0;
//}



int main() {
    sqlite3 *db;
    string cart_list[10];
    int cart_count = 0, rows, columns;
    char **result;
    char *err_msg = 0;
    string book_name, lent_number, c, book_number, c1, c2, line, id_cart;

    int rc = sqlite3_open("DB.db", &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "cannot open database: %s\n", sqlite3_errmsg(db));
        sqlite3_close(db);
        return 1;
    }

    cout << "메인화면\n";
    cout << "1. 로그인\n2. 회원가입\n";
    cout << "번호를 선택해주세요:\n";
    cin >> main_num;


    if (main_num == 2)
        join();
        login();

    if (main_num == 1){
        login();
        cout <<"----------welcome----------\n";
        cout << "1. 조회하기\n 2. 대여하기\n 3. 반납하기\n";
        cout << "번호를 선택해주세요:\n";
        cin >> num;
        if (num == 1)
            search();}


    return 0;
}


int join() {
    sqlite3 *db;
    string cart_list[10];
    int cart_count = 0, rows, columns;
    char **result;
    char *err_msg = 0;
    string book_name, lent_number, c, book_number, c1, c2, line, id_cart;

    int rc = sqlite3_open("DB.db", &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "cannot open database: %s\n", sqlite3_errmsg(db));
    }
    cout << "---------회원가입---------\n";
    end:
    cout << "ID :\n";
    cin >> id;

    string sql = "select id from login where id = ('" + id + "');";
    rc = sqlite3_get_table(db, sql.c_str(),&result,&rows,&columns,&err_msg);
    if (SQLITE_OK != rows) {
        cout << "중복된 아이디입니다.\n";
        cout << "다시 입력해주세요\n";
        goto end;
    }

    cout << "PW :\n";
    cin >> pw;
    string sql2 = "insert into login(id,pw) values ('" + id + "','" + pw + "');";
    rc = sqlite3_exec(db, sql2.c_str(), 0, 0, &err_msg);

    sqlite3_close(db);

    cout << "가입이 완료되었습니다.\n";
    return 0;
}



int login() {
    while (true) {
        sqlite3 *db;
        string cart_list[10];
        int cart_count = 0, rows, columns;
        char **result;
        char *err_msg = 0;
        string book_name, lent_number, c, book_number, c1, c2, line, id_cart;

        int rc = sqlite3_open("DB.db", &db);
        if (rc != SQLITE_OK) {
            fprintf(stderr, "cannot open database: %s\n", sqlite3_errmsg(db));
        }

        cout << "---------로그인---------\n";
        cout << "ID :\n";
        cin >> login_id;
        cout << "PW :\n";
        cin >> login_pw;

        string sql = "select id,pw from login where id = ('" + login_id + "') and pw = ('" + login_pw + "');";
        rc = sqlite3_get_table(db, sql.c_str(),&result,&rows,&columns,&err_msg);
        sqlite3_close(db);

        if (SQLITE_OK != rows) {
            cout << "로그인 완료 !! ^_^ b\n";

            break;
        }
        else {
            cout << "다시 입력해주세요\n";
            continue;
        }
    }
    return 0;
}

int search() {
    sqlite3 *db;
    string cart_list[10];
    int cart_count = 0, rows, columns;
    char **result;
    char *err_msg = 0;
    string book_name, lent_number, c, book_number, c1, c2, line, id_cart;

    int rc = sqlite3_open("DB.db", &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "cannot open database: %s\n", sqlite3_errmsg(db));
    }

    cout << "---------조회하기---------\n";
    cout << "번호를 선택해주세요:\n";
    cout << "1. 도서검색\n2. 저자검색\n3. 도서관 검색\n";
    cin >> search_num;
    if (search_num == 1) {
        cout << "도서를 검색해주세요\n";
        cin >> bookname;
        string sql = "select book_name from book where book_name =('" + bookname + "');";
        rc = sqlite3_exec(db, sql.c_str(), 0, 0, &err_msg);
        cout << rc << endl;
    }

    cout << bookname << "을 장바구니에 추가하시겠어요 ?\n";
    cout << "1. 예\n2. 아니오\n";
    cin >> num;
    if (num == 1) {
        cout << bookname << "을 장바구니에 추가했습니다.";
        string sql = "insert into login(basket) values ('" + bookname + "');";
        rc = sqlite3_exec(db, sql.c_str(), 0, 0, &err_msg);
    }

    if (num == 2)
        cout << "추가 x";

    sqlite3_close(db);
}
