import sqlite3
import hashlib
import json


def read_all_credentials(filename: str) -> list:
    """
    Read all usernames and passwords from a JSON file.

    Parameters:
    - filename (str): The name of the JSON file containing credentials.

    Returns:
    - list: A list of tuples, each containing a username and hashed password.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as pass_file:
            pass_data = json.load(pass_file)

            credentials_list = [(data.get('帳號', ''), data.get('密碼', '')) for data in pass_data]
    except FileNotFoundError:
        print(f'Error: File {filename} not found.')
        return []

    return credentials_list


def check_credentials(username: str, password: str, input_username: str, input_password: str) -> bool:
    """
    Check if the input credentials match the stored credentials.

    Parameters:
    - username (str): The stored username.
    - password (str): The stored hashed password.
    - input_username (str): The username entered by the user.
    - input_password (str): The password entered by the user.

    Returns:
    - bool: True if the credentials match, False otherwise.
    """
    if input_username == username and hashlib.md5(input_password.encode()).hexdigest() == password:
        print('Login successful!\n')
        return True
    else:
        print('Incorrect username or password. Exiting program.')
        return False


def create_database_table(db_filename: str) -> None:
    """
    Create members table in SQLite database.

    Parameters:
    - db_filename (str): The name of the SQLite database file.
    """
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            iid INTEGER PRIMARY KEY AUTOINCREMENT,
            mname TEXT NOT NULL,
            msex TEXT NOT NULL,
            mphone TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def create_members_table(db_filename: str) -> None:
    """
    Create the members table in the SQLite database.

    Parameters:
    - db_filename (str): The name of the SQLite database file.
    """
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # 建立 members 表格，包含 name、gender 和 phone 欄位
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
            iid INTEGER PRIMARY KEY AUTOINCREMENT,
            mname TEXT NOT NULL,
            msex TEXT NOT NULL,
            mphone TEXT NOT NULL
            )
        ''')

        # 提交變更並關閉連接
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f'SQLite error: {e}')


def import_data_from_txt(db_filename: str, txt_filename: str) -> None:
    """
    Import data from a text file into the members table.

    Parameters:
    - db_filename (str): The name of the SQLite database file.
    - txt_filename (str): The name of the text file containing data.
    """
    def get_record_count(cursor):
        cursor.execute('SELECT COUNT(*) FROM members')
        count = cursor.fetchone()[0]
        return count

    try:
        with open(txt_filename, 'r', encoding='utf-8') as members_file:
            conn = sqlite3.connect(db_filename)
            cursor = conn.cursor()

            for line in members_file:
                # Assuming each line in the text file is comma-separated: "姓名,性別,手機"
                data = line.strip().split(',')
                name, gender, phone = data[0], data[1], data[2]

                # Insert data into the table
                cursor.execute("INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)", (name, gender, phone))
            # Get the record count before deletion
            records_before_deletion = get_record_count(cursor)
            # Commit changes and close the connection
            conn.commit()
            conn.close()

        return records_before_deletion

    except FileNotFoundError:
        print(f'Error: File {txt_filename} not found.')


def display_menu() -> None:
    """Display the main menu."""
    print('---------- 選單 ----------')
    print('0 / Enter 離開')
    print('1 建立資料庫與資料表')
    print('2 匯入資料')
    print('3 顯示所有紀錄')
    print('4 新增記錄')
    print('5 修改記錄')
    print('6 查詢指定手機')
    print('7 刪除所有記錄')
    print('--------------------------')


def display_all_records(db_filename: str) -> None:
    """
    顯示 members 表中的所有記錄。

    參數：
    - db_filename (str): SQLite 資料庫檔案的名稱。
    """
    try:
        # 連接資料庫
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # 檢查資料庫是否存在且有資料表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='members'")
        table_exists = cursor.fetchone()

        if table_exists:
            # 從 members 表中選取所有記錄
            cursor.execute('SELECT * FROM members')
            records = cursor.fetchall()

            if records:
                print()
                print(f'{"姓名":<9} {"性別":<3} {"手機"}')
                print('-' * 29)

                for record in records:
                    name_width = len(record[1])
                    name_str = f'{record[1].ljust(6 + (6 - name_width))}'
                    gender_str = f'{record[2]:<5}'
                    phone_str = f'{record[3]}'
                    print(f'{name_str} {gender_str}{phone_str}')
                print()
            else:
                print('=> 查無資料\n')
        else:
            print('=> 資料庫或資料表不存在\n')

        # 關閉資料庫連接
        conn.close()
    except sqlite3.Error as e:
        print(f'SQLite 錯誤: {e}')


def add_new_record(db_filename: str, name: str, sex: str, phone: str) -> None:
    """
    Add a new record to the members table.

    Parameters:
    - db_filename (str): The name of the SQLite database file.
    - name (str): The name of the new record.
    - sex (str): The sex of the new record.
    - phone (str): The phone number of the new record.
    """
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)', (name, sex, phone))

        conn.commit()
        conn.close()

        print('=>異動 1 筆記錄\n')

    except sqlite3.Error as e:
        print(f'SQLite error: {e}')


def modify_record(db_filename: str, name_to_modify: str, new_sex: str, new_phone: str) -> None:
    """
    Modify a record in the members table.

    Parameters:
    - db_filename (str): The name of the SQLite database file.
    - name_to_modify (str): The name of the record to be modified.
    - new_sex (str): The new sex for the record.
    - new_phone (str): The new phone number for the record.
    """
    try:
        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM members WHERE mname=?', (name_to_modify,))
            record = cursor.fetchone()

            if record is not None:
                print(f'\n原資料：\n姓名：{record[1]}，性別：{record[2]}，手機：{record[3]}')

                cursor.execute('UPDATE members SET msex=?, mphone=? WHERE mname=?', (new_sex, new_phone, name_to_modify))

                conn.commit()

                cursor.execute('SELECT * FROM members WHERE mname=?', (name_to_modify,))
                modified_record = cursor.fetchone()

                print(f'=>異動 1 筆記錄\n修改後資料：\n姓名：{modified_record[1]}，性別：{modified_record[2]}，手機：{modified_record[3]}\n')
            else:
                print(f'=>找不到姓名為 {name_to_modify} 的記錄\n')

    except sqlite3.Error as e:
        print(f'SQLite error: {e}')


def search_by_phone(db_filename: str, search_phone: str) -> None:
    """
    Search for records with a specific phone number in the members table.

    Parameters:
    - db_filename (str): The name of the SQLite database file.
    - search_phone (str): The phone number to search for.
    """
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM members WHERE mphone=?', (search_phone,))
        records = cursor.fetchall()

        if records:
            print(f'{"姓名":<9} {"性別":<3} {"手機"}')
            print('--------------------------')
            for record in records:
                name_width = len(record[1])
                name_str = f'{record[1].ljust(6 + (6 - name_width))}'
                gender_str = f'{record[2]:<5}'
                phone_str = f'{record[3]}'
                print(f'{name_str} {gender_str}{phone_str}\n')
        else:
            print(f'=>查無符合手機號碼 {search_phone} 的記錄\n')

        conn.close()
    except sqlite3.Error as e:
        print(f'SQLite error: {e}')


def delete_all_records(db_filename: str) -> int:
    """
    Delete all records from the members table and return the count of records after deletion.

    Parameters:
    - db_filename (str): The name of the SQLite database file.
    """

    def get_record_count(cursor):
        cursor.execute('SELECT COUNT(*) FROM members')
        count = cursor.fetchone()[0]
        return count

    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        # Get the record count before deletion
        records_before_deletion = get_record_count(cursor)
        cursor.execute('DELETE FROM members')

        conn.commit()
        conn.close()

        return records_before_deletion

    except sqlite3.Error as e:
        print(f'SQLite error: {e}')
        return -1  # Return -1 or another suitable value to indicate an error


if __name__ == "__main__":
    pass  # 主程式的部分不在 lib.py 中執行
