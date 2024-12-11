from api import (search_spot, search_trip, collect_spot, collect_trip, create_spot, 
                 create_empty_trip, edit_spot, edit_trip_spots, update_profile, 
                 get_friends, add_friend, view_profile, rate_spot, get_spots, login_user, 
                 set_spot_public, view_my_spots, get_my_trips, get_sth_in_profile, 
                 get_random_trips, get_trip_details, add_member_to_trip, no_invite)

def login_menu():
    """
    用戶登入介面
    """
    print("=== 用戶登入 ===")
    
    while True:
        try:
            user_id = input("請輸入帳號 (用戶 ID): ").strip()
            password = input("請輸入密碼: ").strip()

            if not user_id:
                print("ID不能為空，請重新輸入!")
                continue

            if not password:
                print("密碼不能為空，請重新輸入!")
                continue

            print("正在驗證中，請稍候...")
            result = login_user(user_id, password)

            if result["status"] == "success":
                user_id = result["user_id"]
                user_name = get_sth_in_profile(user_id, "user_name")
                print(f"登入成功！用戶 ID: {user_id}")
                if user_name:
                    print(f"歡迎回來，{user_name}!")
                return user_id
            elif result["status"] == "fail":
                print(f"登入失敗:{result['message']}")
            elif result["status"] == "error":
                print(f"伺服器錯誤:{result['message']}")
            else:
                print("未知錯誤，請稍後再試！")
        except Exception as e:
            print(f"發生錯誤:{str(e)}")
            return None


def main_menu(user_id):
    print("\n主頁面")
    print("1. 探索：探索新奇的造訪點與旅程")
    print("2. 典藏：製作與儲存你的造訪點與旅程")
    print("3. 個人檔案")
    print("4. 離開系統")
    choice = input("選擇功能: ")
    if choice == "1":
        explore_menu(user_id)
    elif choice == "2":
        collection_menu(user_id)
    elif choice == "3":
        profile_menu(user_id)
    elif choice == "4":
        print("再見!")
        exit()
    else:
        print("無效選項，請重試。")

#explorePage
def explore_menu(user_id):
    print("\n探索頁面")
    print("1. 探索造訪點：發掘新奇的造訪點")
    print("2. 探索旅程：來場有趣的旅程")
    print("3. 返回主頁面")
    choice = input("選擇功能: ")
    
    if choice == "1":
        explore_spots(user_id)
    elif choice == "2":
        explore_trips(user_id)
    elif choice == "3":
        return
    else:
        print("無效選項，請重試。")

def explore_spots(user_id):
    while True:
        # 顯示推薦造訪點
        results = get_spots()
        print("\n推薦熱門造訪點:")
        for spot in results:
            print(f"ID: {spot['spot_id']}, 名稱: {spot['spot_name']}, "
                  f"地址: {spot['address']}, 平均評分: {spot['ave_rate']}, "
                  f"類別: {spot['category']}")
        
        print("\n選擇操作:")
        print("1. 典藏造訪點")
        print("2. 搜尋造訪點")
        print("3. 返回探索頁面")
        
        choice = input("請選擇: ").strip()
        
        if choice == "1":
            spot_id = input("請輸入要典藏的造訪點 ID: ").strip()
            response = collect_spot(user_id, spot_id)
            if response.get("status") == "success":
                print("典藏成功！")
            else:
                print(f"典藏失敗:{response.get('message')}")
                
        elif choice == "2":
            keyword = input("請輸入關鍵字 (名稱/地區/類別): ").strip()
            results = search_spot(keyword)
            if not results:
                print("找不到相關造訪點")
            else:
                print("\n搜尋結果:")
                for spot in results:
                    print(f"ID: {spot['spot_id']}, 名稱: {spot['spot_name']}, "
                          f"地址: {spot['address']}, 平均評分: {spot['ave_rate']}, "
                          f"類別: {spot['category']}")
        
        elif choice == "3":
            explore_menu(user_id)
            break
        else:
            print("無效選項，請重試。")

def explore_trips(user_id):
    while True:
        # 顯示推薦旅程
        results = get_random_trips()
        print("\n推薦熱門旅程:")
        for trip in results:
            print(f"ID: {trip['trip_id']}, 名稱: {trip['trip_name']}, "
                  f"描述: {trip['description']}")
        
        print("\n選擇操作:")
        print("1. 查看旅程")
        print("2. 典藏旅程")
        print("3. 搜尋旅程")
        print("4. 幹不揪 no invite")
        print("5. 返回探索頁面")
        
        choice = input("請選擇: ").strip()
        
        if choice == "4" or choice.lower() == "no invite":
            response = no_invite(user_id)
            if response.get("status") == "success":
                trips = response.get("trips", [])
                if not trips:
                    print("\n恭喜，你做人非常成功！")
                    continue
                    
                print("\n以下是你的朋友們偷偷約出去玩的旅程：")
                for trip in trips:
                    print(f"ID: {trip['trip_id']}, "
                          f"名稱: {trip['trip_name']}, "
                          f"描述: {trip['description']}")
            else:
                print(f"獲取旅程失敗：{response.get('message')}")
                
        elif choice == "1":
            trip_id = input("請輸入要查看的旅程 ID: ").strip()
            response = get_trip_details(trip_id)
            
            if response.get("status") == "success":
                trip_data = response["data"]
                print(f"\n旅程名稱: {trip_data['trip_name']}")
                print(f"描述: {trip_data['description']}")
                print("\n旅程造訪點:")
                for spot in trip_data["spots"]:
                    print(f"{spot['sequence_number']}. {spot['spot_name']}")
                
                if input("\n是否要典藏此旅程?(y/n): ").lower() == 'y':
                    collect_response = collect_trip(user_id, trip_id)
                    if collect_response.get("status") == "success":
                        print("典藏成功！")
                    else:
                        print(f"典藏失敗:{collect_response.get('message')}")
            else:
                print(f"獲取旅程詳情失敗:{response.get('message')}")

        elif choice == "2":
            trip_id = input("請輸入要典藏的旅程 ID: ").strip()
            response = collect_trip(user_id, trip_id)
            if response.get("status") == "success":
                print("典藏成功！")
            else:
                print(f"典藏失敗:{response.get('message')}")
                
        elif choice == "3":
            keyword = input("請輸入關鍵字: ").strip()
            results = search_trip(keyword)
            if not results:
                print("找不到相關旅程")
            else:
                print("\n搜尋結果:")
                for trip in results:
                    print(f"ID: {trip['trip_id']}, 名稱: {trip['trip_name']}, "
                          f"描述: {trip['description']}")
        
        elif choice == "5":
            explore_menu(user_id)
            break
        else:
            print("無效選項，請重試。")

#collectionPage
def collection_menu(user_id):
    print("\n典藏庫頁面")
    print("1. 編輯造訪點庫")
    print("2. 編輯旅程庫")
    print("3. 返回主頁面")
    choice = input("選擇功能: ")
    if choice == "1":
        edit_spot_menu(user_id)
    elif choice == "2":
        edit_trip_menu(user_id)
    elif choice == "3":
        return
    else:
        print("無效選項，請重試。")

def edit_spot_menu(user_id):
    while True:
        print("\n編輯造訪點庫")
        spots = view_my_spots(user_id)
        if not spots:
            print("您目前沒有任何造訪點")
            return
        print("\n您的造訪點列表:")
        for spot in spots:
            print(f"ID: {spot['spot_id']}, 名稱: {spot['spot_name']}, "
                f"地址: {spot['address']}, 類別: {spot['category']}, 平均評分: {spot['ave_rate']}")
        print("1. 新增造訪點")
        print("2. 編輯我的造訪點")
        print("3. 評價造訪點")
        print("4. 返回典藏庫")
        choice = input("選擇功能: ")

        if choice == "1":
            try:
                user_id = user_id
                spot_name = input("輸入造訪點名稱: ").strip()
                address = input("輸入造訪點地址/地區: ").strip()
                category = input("輸入造訪點類別: ").strip()
                estimate_cost = int(input("輸入預估花費: "))
                estimate_stay_time = int(input("輸入預估停留時間（分鐘）: "))

                response = create_spot(
                    user_id=user_id,
                    spot_name=spot_name,
                    address=address,
                    category=category,
                    estimate_cost=estimate_cost,
                    estimate_stay_time=estimate_stay_time
                )
                print("伺服器回應:", response)
                if response.get("status") == "success":
                    spot_id = response["data"]["spot_id"]
                    while True:
                        choice = input("是否要將此造訪點設為公開？(y/n): ").strip().lower()
                        if choice in ["y", "n"]:
                            break
                        print("請輸入 y 或 n")

                    if choice == "y":
                        public_response = set_spot_public(spot_id)
                        if public_response.get("status") == "success":
                            print("造訪點已設為公開")
                        else:
                            print(f"設定造訪點公開失敗，維持私人:{public_response.get('message')}")
                    else:
                        print("造訪點保持未公開")
                else:
                    print(f"創建造訪點失敗:{response.get('message')}")

            except Exception as e:
                print(f"發生錯誤:{str(e)}")
        elif choice == "2":
            try:
                spot_id = input("\n輸入要編輯的造訪點 ID (或按 Enter 返回): ").strip()
                if not spot_id:
                    continue
                    
                if not any(s['spot_id'] == spot_id for s in spots):
                    print("無效的造訪點 ID")
                    continue
                    
                print("\n選擇要編輯的項目:")
                print("1. 造訪點名稱")
                print("2. 地址")
                print("3. 類別")
                print("4. 預估花費")
                print("5. 預估停留時間")

                edit_choice = input("請選擇 (1-5): ").strip()
                
                field_map = {
                    "1": "spot_name",
                    "2": "address",
                    "3": "category",
                    "4": "estimate_cost",
                    "5": "estimate_stay_time"
                }
                
                if edit_choice not in field_map:
                    print("無效的選擇")
                    continue
                    
                new_value = input("輸入新的值: ").strip()
                if not new_value:
                    print("值不能為空")
                    continue
                    
                print("正在更新...")
                response = edit_spot(
                    user_id=user_id,
                    spot_id=spot_id,
                    keyword=field_map[edit_choice],
                    new_value=new_value
                )
                
                if response and response.get("status") == "success":
                    print("編輯成功！")
                else:
                    print(f"編輯失敗:{response.get('message', '未知錯誤')}")
                    
            except Exception as e:
                print(f"發生錯誤:{str(e)}")
        elif choice == "3":
            spot_id = input("輸入要評價的造訪點 ID: ").strip()
            while True:
                try:
                    rate = int(input("輸入評分 (1-5): "))
                    if 1 <= rate <= 5:
                        break
                    print("評分必須在 1-5 之間")
                except ValueError:
                    print("請輸入有效的數字")
                
            response = rate_spot(user_id, spot_id, rate)
            if response.get("status") == "success":
                print("評分成功！造訪點庫已更新")
            else:
                print(f"評分失敗:{response.get('message')}")
        elif choice == "4":
            collection_menu(user_id)
            break
        else:
            print("無效選項，請重試。")

def edit_trip_menu(user_id):
    while True:
        print("\n編輯旅程庫")
        # 顯示用戶的旅程
        response = get_my_trips(user_id)
        if response.get("status") != "success":
            print(f"獲取旅程失敗:{response.get('message')}")
            continue
            
        trips = response.get("trips", [])
        if not trips:
            print("您目前沒有任何旅程")
            continue
            
        print("\n您的旅程列表:")
        for trip in trips:
            print(f"ID: {trip['trip_id']}, 名稱: {trip['trip_name']}")
        print("\n1. 新增空白旅程")
        print("2. 編輯我的旅程")
        print("3. 加入成員")
        print("4. 返回典藏庫")
        choice = input("選擇功能: ")
        
        if choice == "1":
            # 新增空白旅程
            trip_name = input("請輸入旅程名稱: ").strip()
            if not trip_name:
                print("旅程名稱不能為空")
                continue
                
            description = input("請輸入旅程描述 (可選): ").strip()
            
            response = create_empty_trip(user_id, trip_name, description)
            if response.get("status") == "success":
                print(f"旅程建立成功!ID: {response['data']['trip_id']}")
            else:
                print(f"建立失敗:{response.get('message')}")
                
        elif choice == "2":
            # 顯示用戶的旅程
            response = get_my_trips(user_id)
            if response.get("status") != "success":
                print(f"獲取旅程失敗:{response.get('message')}")
                continue
                
            trips = response.get("trips", [])
            if not trips:
                print("您目前沒有任何旅程")
                continue
                
            print("\n您的旅程列表:")
            for trip in trips:
                print(f"ID: {trip['trip_id']}, 名稱: {trip['trip_name']}, "
                      f"描述: {trip['description']}")
            
            # 選擇要編輯的旅程
            trip_id = input("\n輸入要編輯的旅程 ID (或按 Enter 返回): ").strip()
            if not trip_id:
                continue
                
            # 顯示旅程詳情
            details = get_trip_details(trip_id)
            if details.get("status") != "success":
                print(f"獲取旅程詳情失敗:{details.get('message')}")
                continue
                
            trip_data = details["data"]
            print(f"\n旅程名稱: {trip_data['trip_name']}")
            print(f"描述: {trip_data['description']}")
            print("\n目前造訪點順序:")
            for spot in trip_data.get("spots", []):
                print(f"{spot['sequence_number']}. {spot['spot_name']}")
            while True:
                print("\n選擇操作:")
                print("1. 修改現有造訪點")
                print("2. 新增造訪點")
                print("3. 返回")
                
                edit_choice = input("請選擇: ").strip()
            
                if edit_choice == "1":
                    spots = view_my_spots(user_id)
                    if not spots:
                        print("您目前沒有任何造訪點")
                        return
                    print("\n您的造訪點列表:")
                    for spot in spots:
                        print(f"ID: {spot['spot_id']}, 名稱: {spot['spot_name']}, "
                            f"地址: {spot['address']}, 類別: {spot['category']}, 平均評分: {spot['ave_rate']}")
                    seq_num = input("輸入要修改的序號:").strip()
                    spot_id = input("輸入新的造訪點 ID: ").strip()
                    
                    response = edit_trip_spots(trip_id, spot_id, seq_num, False)
                    if response.get("status") == "success":
                        print("造訪點修改成功！")
                        # 重新獲取最新的行程詳情
                        details = get_trip_details(trip_id)
                        if details.get("status") == "success":
                            trip_data = details["data"]
                            print(f"\n旅程名稱: {trip_data['trip_name']}")
                            print(f"描述: {trip_data['description']}")
                            print("\n目前造訪點順序:")
                            for spot in trip_data.get("spots", []):
                                print(f"{spot['sequence_number']}. {spot['spot_name']}")
                        continue
                    else:
                        print(f"修改失敗:{response.get('message')}") 

                elif edit_choice == "2":
                    spots = view_my_spots(user_id)
                    if not spots:
                        print("您目前沒有任何造訪點")
                        return
                    print("\n您的造訪點列表:")
                    for spot in spots:
                        print(f"ID: {spot['spot_id']}, 名稱: {spot['spot_name']}, "
                            f"地址: {spot['address']}, 類別: {spot['category']}, 平均評分: {spot['ave_rate']}")
                    
                    spot_id = input("輸入要新增的造訪點 ID:").strip()
                    response = edit_trip_spots(trip_id, spot_id, is_new=True)
                    if response.get("status") == "success":
                        print("造訪點新增成功！")
                        details = get_trip_details(trip_id)
                        trip_data = details["data"]
                        print(f"\n旅程名稱: {trip_data['trip_name']}")
                        print(f"描述: {trip_data['description']}")
                        print("\n目前造訪點順序:")
                        for spot in trip_data.get("spots", []):
                            print(f"{spot['sequence_number']}. {spot['spot_name']}")
                        continue
                    else:
                        print(f"新增失敗:{response.get('message')}")
                elif edit_choice == "3":
                    break
                    
        elif choice == "3":
            # 顯示用戶的旅程
            response = get_my_trips(user_id)
            if response.get("status") != "success":
                print(f"獲取旅程失敗:{response.get('message')}")
                continue
                
            trips = response.get("trips", [])
            if not trips:
                print("您目前沒有任何旅程")
                continue
                
            print("\n您的旅程列表:")
            for trip in trips:
                print(f"ID: {trip['trip_id']}, 名稱: {trip['trip_name']}")
            
            trip_id = input("\n請輸入要加入成員的旅程 ID: ").strip()
            
            # 顯示好友列表
            friends_response = get_friends(user_id)
            if friends_response.get("status") != "success":
                print(f"獲取好友列表失敗:{friends_response.get('message')}")
                continue
                
            friends = friends_response.get("data", [])
            if not friends:
                print("您目前沒有好友")
                continue
                
            print("\n您的好友列表:")
            for friend in friends:
                print(f"ID: {friend['id']}, 名稱: {friend['name']}")
                
            friend_id = input("\n請輸入要加入的好友 ID: ").strip()
            
            response = add_member_to_trip(trip_id, user_id, friend_id)
            if response.get("status") == "success":
                print("成員新增成功！")
            else:
                print(f"新增失敗:{response.get('message')}")
                
        elif choice == "4":
            collection_menu(user_id)
            break
        else:
            print("無效選項，請重試。")

#profilePage
def profile_menu(user_id):
    print("\n個人檔案頁面")
    
    # 獲取用戶資料
    user_name = get_sth_in_profile(user_id, "user_name") or "未設定"
    email = get_sth_in_profile(user_id, "email") or "未設定"
    profile_pic = get_sth_in_profile(user_id, "profile_pic") or "未設定"
    
    print(f"用戶名稱: {user_name}")
    print(f"電子郵件: {email}")
    print(f"頭像: {profile_pic}")
    
    print("\n1. 修改個人檔案")
    print("2. 好友列表")
    print("3. 返回主頁面")
    choice = input("選擇功能: ")
    if choice == "1":
        print("\n修改個人檔案")
        new_name = input("輸入新名稱 (空白則保持不變): ").strip()
        new_email = input("輸入新電子郵件 (空白則保持不變): ").strip()
        new_profile_pic = input("輸入新頭像 URL (空白則保持不變): ").strip()

        # 更新名稱
        if new_name:
            update_profile(user_id, "user_name", new_name)

        # 更新電子郵件
        if new_email:
            update_profile(user_id, "email", new_email)

        # 更新頭像
        if new_profile_pic:
            update_profile(user_id, "profile_pic", new_profile_pic)

        print("個人檔已更新")
    elif choice == "2":
        friend_menu(user_id)
    elif choice == "3":
        return
    else:
        print("無效選項，請重試。")

def friend_menu(user_id):
    print("\n好友列表")
    response = get_friends(user_id)
    
    if response.get("status") == "error":
        print(f"錯誤:{response.get('message')}")
        return
        
    friends = response.get("data", [])
    
    if not friends:
        print("您目前沒有好友。")
        return
        
    print("\n您的好友列表:")
    for friend in friends:
        print(f"ID: {friend['id']}, 名稱: {friend['name']}")
    print("\n1. 查看好友檔案")
    print("2. 加入好友")
    print("3. 返回個人檔案頁面")
    choice = input("選擇功能: ")
    if choice == "1":
        view_friends(user_id)
    elif choice == "2":
        friend_id = input("輸入好友的 User ID: ")
        response = add_friend(user_id, friend_id)
        print(response)
    elif choice == "3":
        profile_menu(user_id)
    else:
        print("無效選項，請重試。")

def view_friends(user_id):
    response = get_friends(user_id)
    
    if response.get("status") == "error":
        print(f"錯誤:{response.get('message')}")
        return
        
    friends = response.get("data", [])
    
    if not friends:
        print("您目前沒有好友")
        return
        
    print("\n您的好友列表:")
    for friend in friends:
        print(f"ID: {friend['id']}, 名稱: {friend['name']}")
        
    while True:
        friend_id = input("\n輸入好友 ID 查看檔案，或按 Enter 返回: ").strip()
        if not friend_id:
            break
            
        if any(f['id'] == friend_id for f in friends):
            response = view_profile(friend_id)
            if response.get("status") == "success":
                profile = response.get("profile", {})
                print("\n好友檔案:")
                print(f"用戶名稱: {profile.get('user_name')}")
                print(f"電子郵件: {profile.get('email')}")
                
                print("\n公開造訪點:")
                for spot in response.get("created_spots", []):
                    print(f"- {spot['spot_id']} {spot['spot_name']} ({spot['address']})")
                
                print("\n公開建立旅程:")
                for trip in response.get("created_trips", []):
                    print(f"- {trip['trip_id']} {trip['trip_name']}: {trip['description']}")
                print("\n公開參與旅程:")
                for trip in response.get("participating_trips", []):
                    print(f"- {trip['trip_id']} {trip['trip_name']} {trip['description']}")
                
                input("\n按 Enter 返回...")
            else:
                print(f"獲取檔案失敗:{response.get('message')}")
        else:
            print("無效的好友 ID")

# def view_public_trips():
#     trips = search_trip()
#     if not trips:
#         print("目前沒有公開旅程。")
#         return
#     print("\n公開旅程列表:")
#     for trip in trips:
#         print(f"- {trip['name']} ({trip['region']})")

# def view_public_spots():
#     spots = search_spot()
#     if not spots:
#         print("目前沒有公開造訪點。")
#         return
#     print("\n公開造訪點列表:")
#     for spot in spots:
#         print(f"- {spot['name']} ({spot['location']})")
