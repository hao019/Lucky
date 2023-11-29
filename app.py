from pkg.lib import read_all_credentials, create_database_table, import_data_from_txt
from pkg.lib import display_menu, display_all_records, add_new_record, modify_record
from pkg.lib import create_members_table, search_by_phone, delete_all_records


def main():
    # 讀取所有帳號密碼
    credentials_list = read_all_credentials("pass.json")

    # 輸入帳號密碼
    input_username = input("請輸入帳號：")
    input_password = input("請輸入密碼：")

    # 檢查帳密是否正確
    if not any(username == input_username and password == input_password for username, password in credentials_list):
        print("=>帳密錯誤，程式結束\n")
        return
    print()
    # Replace with your actual database filename
    db_filename = "wanghong.db"
    create_members_table(db_filename)
    delete_all_records(db_filename)
    # 帳密正確，顯示選單
    while True:
        display_menu()
        choice = input("請輸入您的選擇 [0-7]: ")

        if choice == "0" or choice.lower() == "enter":
            break
        elif choice == "1":
            # 建立資料庫與資料表
            create_database_table("wanghong.db")
            print("=>資料庫已建立\n")
        elif choice == "2":
            # 匯入資料
            # import_data_from_txt("wanghong.db", "members.txt")
            records_before_deletion = import_data_from_txt("wanghong.db", "members.txt")
            print(f"=> 異動 {records_before_deletion} 筆記錄\n")
        elif choice == "3":
            # 顯示所有紀錄
            display_all_records("wanghong.db")
        elif choice == "4":
            # 新增記錄
            name = input("請輸入姓名: ")
            sex = input("請輸入性別: ")
            phone = input("請輸入手機: ")
            add_new_record("wanghong.db", name, sex, phone)
        elif choice == "5":
            # 修改記錄
            name_to_modify = input("請輸入想修改記錄的姓名: ")
            if not name_to_modify:
                print("=>必須指定姓名才可修改記錄\n")
            else:
                new_sex = input("請輸入要改變的性別: ")
                new_phone = input("請輸入要改變的手機: ")
                modify_record("wanghong.db", name_to_modify, new_sex, new_phone)
        elif choice == "6":
            # 查詢指定手機
            search_phone = input("請輸入想查詢記錄的手機: ")
            search_by_phone(db_filename, search_phone)

        elif choice == "7":
            # 刪除所有記錄
            records_before_deletion = delete_all_records(db_filename)
            delete_all_records(db_filename)
            print(f"=> 異動 {records_before_deletion} 筆記錄\n")
        else:
            print("=>無效的選擇\n")


if __name__ == "__main__":
    main()
