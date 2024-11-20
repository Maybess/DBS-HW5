import mysql.connector

config = {
    'user': 'leeminki',
    'password': '3051',
    'host': '192.168.56.101',
    'database': 'madang',
}

def connect_to_database():
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL 연결 오류: {err}")
        return None

def insert_book(cursor, book_data):
    try:
        insert_query = "INSERT INTO Book (bookid, bookname, publisher, price) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, book_data)
        print("새로운 책이 추가되었습니다.")
    except mysql.connector.Error as err:
        print(f"데이터 삽입 오류: {err}")

def delete_book(cursor, book_id):
    try:
        delete_query = "DELETE FROM Book WHERE bookid = %s"
        cursor.execute(delete_query, (book_id,))
        if cursor.rowcount > 0:
            print(f"bookid {book_id}인 책이 삭제되었습니다.")
        else:
            print(f"bookid {book_id}인 책을 찾을 수 없습니다.")
    except mysql.connector.Error as err:
        print(f"데이터 삭제 오류: {err}")

def search_books_by_keyword(cursor, keyword):
    try:
        select_query = "SELECT * FROM Book WHERE bookname LIKE %s"
        cursor.execute(select_query, (f"%{keyword}%",)) 
        rows = cursor.fetchall()
        if rows:
            print(f"\n'{keyword}'를 포함하는 책 검색 결과:")
            for row in rows:
                print(row)
        else:
            print(f"'{keyword}'를 포함하는 책을 찾을 수 없습니다.")
    except mysql.connector.Error as err:
        print(f"데이터 검색 오류: {err}")
        
def search_books(cursor):
    try:
        select_query = "SELECT * FROM Book"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        if rows:
            print("\n모든 책 정보:")
            for row in rows:
                print(row)
        else:
            print("책 정보가 없습니다.")
    except mysql.connector.Error as err:
        print(f"데이터 검색 오류: {err}")

conn = connect_to_database()
if conn:
    cursor = conn.cursor()
    try:
        while True:
            print("\n원하는 작업을 선택하세요:")
            print("1. 책 추가")
            print("2. 책 삭제")
            print("3. 제목으로 책 검색")
            print("4. 책 목록")
            print("5. 종료")
            choice = input("선택: ")

            if choice == '1':
                book_id = int(input("책 ID: "))
                book_name = input("책 이름: ")
                publisher = input("출판사: ")
                price = int(input("가격: "))
                insert_book(cursor, (book_id, book_name, publisher, price))
            elif choice == '2':
                book_id = int(input("삭제할 책 ID: "))
                delete_book(cursor, book_id)
            elif choice == '3':
                keyword = input("검색할 문자열: ")
                search_books_by_keyword(cursor, keyword)
            elif choice == '4':
                search_books(cursor)
            elif choice == '5':
                break
            else:
                print("제대로 된 숫자를 입력해주세요.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        conn.commit()
        cursor.close()
        conn.close()
        print("MySQL 연결이 닫혔습니다.")
