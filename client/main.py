from views import main_menu, login_menu
from api import test_connection

if __name__ == "__main__":
    print("歡迎使用 TRAVELGO!")
    
    if not test_connection():
        print("無法連接到伺服器，請確認伺服器是否啟動")
        exit(1)

    current_user_id = None  # 保存當前登入用戶的 ID

    while True:
        if current_user_id is None:
            current_user_id = login_menu()  # 獲取登入用戶的 ID
            if current_user_id is None:
                continue
        else:
            main_menu(current_user_id)  # 將用戶 ID 傳遞給主選單
