import duckdb
from datetime import datetime, timedelta

DB_FILE = "server/data/travelgo"

# query = """
#     CREATE INDEX idx_spot_is_public ON "Spot" (is_public);
#     CREATE INDEX idx_spot_spot_id ON "Spot" (spot_id);
#     CREATE INDEX idx_spot_create_by ON "Spot" (create_by);
#     CREATE INDEX idx_spot_iliike_search ON "Spot" USING GIN (spot_name gin_trgm_ops, address gin_trgm_ops, category gin_trgm_ops);


#     CREATE UNIQUE INDEX idx_password_user_id_password ON "Password" (user_id, password);

#     CREATE INDEX idx_trip_create_by ON "Trip" (create_by);
#     CREATE INDEX idx_trip_trip_id ON "Trip" (trip_id);
#     CREATE INDEX idx_trip_is_public ON "Trip" (is_public);
#     CREATE INDEX idx_trip_iliike_search ON "Trip" USING GIN (trip_name gin_trgm_ops);

#     CREATE INDEX idx_participatein_trip_id ON "ParticipateIn" (trip_id);
#     CREATE INDEX idx_participatein_participant_id ON "ParticipateIn" (participant_id);

#     CREATE INDEX idx_friendship_user1_user2 ON "Friendship" (user_id1, user_id2);
#     CREATE INDEX idx_friendship_user2_user1 ON "Friendship" (user_id2, user_id1);

#     CREATE UNIQUE INDEX idx_user_user_id ON "User" (user_id);
#     """
# with duckdb.connect(DB_FILE) as conn:
#     results = conn.execute(query).fetchall()

def check_login_in_db(user_id, password):
    """
    核對用戶 ID 和密碼是否正確
    :param user_id: 用戶 ID
    :param password: 用戶輸入的密碼
    :return: 字典，包含驗證結果和相關訊息
    """
    try:
        # 定義 SQL 查詢，使用參數化查詢避免 SQL 注入
        query = """
        SELECT user_id, password
        FROM "Password"
        WHERE user_id = ? AND password = ?
        """
        
        # 連接資料庫並執行查詢
        with duckdb.connect(DB_FILE) as conn:
            results = conn.execute(query, (user_id, password)).fetchall()

        # 如果有結果，表示用戶名和密碼正確
        if results:
            return {"status": "success", "message": "登入成功", "user_id": results[0][0]}
        else:
            return {"status": "fail", "message": "用戶 ID 或密碼錯誤"}
    
    except Exception as e:
        # 捕獲資料庫錯誤並返回錯誤訊息
        return {"status": "error", "message": f"Database error: {e}"}

def get_random_spots_in_db(count=20):
    """
    隨機從資料庫中選取指定數量的景點。
    """
    try:
        # 確保 count 是正整數
        count = max(1, count)
        
        # 隨機選取景點的 SQL 查詢
        query = """
        SELECT spot_id, spot_name, address, ave_rate, category
        FROM "Spot"
        WHERE is_public = TRUE
        ORDER BY RANDOM()
        LIMIT ?;
        """
        with duckdb.connect(DB_FILE) as conn:
            results = conn.execute(query, [count]).fetchall()
        
        # 將結果轉換為字典列表
        return [
            {
                "spot_id": row[0],
                "spot_name": row[1],
                "address": row[2],
                "ave_rate": row[3],
                "category": row[4],
            }
            for row in results
        ]
    except Exception as e:
        return {"status": "error", "message": f"Database error: {e}"}

def search_spot_in_db(keyword):
    query = f"""
    SELECT * FROM spot
    WHERE (spot_name ILIKE '%{keyword}%'
       OR address ILIKE '%{keyword}%'
       OR category ILIKE '%{keyword}%')
       AND is_public = TRUE
    LIMIT 20;
    """
    with duckdb.connect(DB_FILE) as conn:
        results = conn.execute(query).fetchall()
    return [{"spot_id": row[0], "spot_name": row[1], "ave_rate": row[2], "address": row[3], "category": row[4],} for row in results]

def view_my_spot_in_db(user_id):
    query = """
    SELECT s.spot_id, s.spot_name, s.ave_rate, s.address, s.category
    FROM "Spot" s
    WHERE s.create_by = ?
    ORDER BY s.spot_id;
    """
    
    with duckdb.connect(DB_FILE) as conn:
        results = conn.execute(query, [user_id]).fetchall()
    
    return [{
        "spot_id": row[0],
        "spot_name": row[1],
        "ave_rate": row[2],
        "address": row[3],
        "category": row[4]
    } for row in results]

def detail_trip_in_db(trip_id):
    query = f"""
    SELECT * FROM trip
    """

def view_my_trip_in_db(user_id):
    query = f"""
    SELECT trip.trip_id, trip.trip_name, trip.description
    FROM "Trip" AS trip
    WHERE trip.create_by = '{user_id}'
    UNION
    SELECT trip.trip_id, trip.trip_name, trip.description
    FROM "ParticipateIn" AS participate
    INNER JOIN "Trip" AS trip ON participate.trip_id = trip.trip_id
    WHERE participate.participant_id = '{user_id}';
    """
    
    with duckdb.connect(DB_FILE) as conn:
        results = conn.execute(query).fetchall()
    
    # 返回格式化的結果
    return [{"trip_id": row[0], "trip_name": row[1], "description": row[2]} for row in results]

def search_trip_in_db(keyword):
    query = f"""
    SELECT * FROM trip
    WHERE trip_name ILIKE '%{keyword}%'
       AND is_public = TRUE
    LIMIT 20;
    """
    with duckdb.connect(DB_FILE) as conn:
        results = conn.execute(query).fetchall()
    return [{"trip_id": row[0], "trip_name": row[1], "description": row[2]} for row in results]

def collect_trip_in_db(user_id, trip_id):
    """
    典藏行程，創建新的行程副本
    """
    try:
        with duckdb.connect(DB_FILE) as conn:
            # 1. 獲取原行程資訊
            trip_query = """
            SELECT trip_name, description
            FROM "Trip"
            WHERE trip_id = ?;
            """
            trip_info = conn.execute(trip_query, [trip_id]).fetchone()
            
            if not trip_info:
                return {
                    "status": "error",
                    "message": "行程不存在"
                }
            
            # 2. 生成新的 trip_id
            new_id_query = """
            SELECT MAX(CAST(SUBSTR(trip_id, 2) AS INT))
            FROM "Trip";
            """
            max_id = conn.execute(new_id_query).fetchone()[0]
            new_trip_id = f"T{max_id + 1 if max_id else 1}"
            
            # 3. 創建新行程
            create_date = datetime.now().strftime('%Y-%m-%d')
            insert_query = """
            INSERT INTO "Trip" (trip_id, trip_name, description, is_public, create_date, create_by, host)
            VALUES (?, ?, ?, FALSE, ?, ?, ?);
            """
            conn.execute(insert_query, [
                new_trip_id,
                trip_info[0],
                trip_info[1],
                create_date,
                user_id,
                user_id
            ])
            
            # 4. 複製景點列表
            copy_spots_query = """
            INSERT INTO "SpotInTrip" (trip_id, spot_id, sequence_number)
            SELECT ?, spot_id, sequence_number
            FROM "SpotInTrip"
            WHERE trip_id = ?;
            """
            conn.execute(copy_spots_query, [new_trip_id, trip_id])
            
            return {
                "status": "success",
                "message": "行程典藏成功",
                "data": {
                    "new_trip_id": new_trip_id
                }
            }
            
    except Exception as e:
        print(f"Error collecting trip: {str(e)}")
        return {
            "status": "error",
            "message": f"典藏行程失敗: {str(e)}"
        }

def collect_spot_in_db(user_id, keyword):
    try:
        # 1. 檢查指定的 spot_id 是否存在
        query = f"""
        SELECT spot_id, spot_name
        FROM "Spot"
        WHERE spot_id = '{keyword}'
        LIMIT 1;
        """
        
        with duckdb.connect(DB_FILE) as conn:
            result = conn.execute(query).fetchone()
        
        if not result:
            return {"status": "error", "message": "Spot not found"}
        
        # 2. 當前時間（collect_date）
        collect_date = datetime.now().strftime('%Y-%m-%d')  # 當下日期
        
        # 3. 將 spot_id 和 user_id 插入 SpotCollect
        insert_query = f"""
        INSERT INTO "SpotCollect" (user_id, spot_id, collect_date)
        VALUES ('{user_id}', '{keyword}', '{collect_date}');
        """
        
        with duckdb.connect(DB_FILE) as conn:
            # 執行插入操作
            conn.execute(insert_query)
        
        # 4. 返回成功
        return {"status": "success", "message": "Spot collected successfully"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_spot_in_db(user_id, spot_name, address, category, estimate_cost, estimate_stay_time, is_public=False):
    try:
        # 1. 檢查必要參數
        if not all([user_id, spot_name, address, category]):
            return {"status": "error", "message": "Missing required parameters"}

        with duckdb.connect(DB_FILE) as conn:
            # 2. 獲取的 spot_id
            query = "SELECT MAX(CAST(SUBSTR(spot_id, 2) AS INT)) FROM \"Spot\";"
            result = conn.execute(query).fetchone()
            new_spot_id = f"S{result[0] + 1 if result[0] is not None else 1}"

            # 2. ave_rate
            ave_rate = 5
            # 3. 當前時間
            create_date = datetime.now().strftime('%Y-%m-%d')

            # 4. 準備 SQL 語句，使用參數化查詢
            insert_query = """
            INSERT INTO "Spot" 
            (spot_id, spot_name, address, ave_rate, category, estimate_cost, estimate_stay_time, is_public, create_by, create_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            
            # 5. 執行插入
            conn.execute(insert_query, [
                new_spot_id,
                spot_name,
                address,
                ave_rate,
                category,
                estimate_cost,
                estimate_stay_time,
                is_public,
                user_id,
                create_date
            ])

            # 6. 返回成功訊息
            return {
                "status": "success",
                "message": f"Spot {new_spot_id} created successfully",
                "data": {
                    "spot_id": new_spot_id,
                    "spot_name": spot_name,
                    "is_public": is_public
                }
            }

    except duckdb.Error as e:
        print(f"Database error: {str(e)}")  # 添加日誌
        return {"status": "error", "message": f"Database error: {str(e)}"}
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # 添加日誌
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}

def set_spot_public_in_db(spot_id):
    try:
        query = f"""
        UPDATE "Spot"
        SET is_public = TRUE
        WHERE spot_id = ?;
        """
        with duckdb.connect(DB_FILE) as conn:
            conn.execute(query, [spot_id])
            
        return {
            "status": "success",
            "message": f"Spot {spot_id} is now public",
            "data": {"spot_id": spot_id, "is_public": True}
        }
    
    except Exception as e:
        print(f"Error setting spot public: {str(e)}")  # 記錄錯誤
        return {"status": "error", "message": f"Failed to set spot public: {str(e)}"}

# 分景點，新增至 Comment 表
def rate_spot_in_db(spot_id, user_id, rate):
    try:
        # 檢查評分範圍
        if not (1 <= rate <= 5):
            return {
                "status": "error",
                "message": "評分必須在 1-5 之間"
            }
            
        with duckdb.connect(DB_FILE) as conn:
            # 檢查是否已經評分過
            check_query = """
            SELECT COUNT(*) FROM "Comment"
            WHERE spot_id = ? AND user_id = ?;
            """
            exists = conn.execute(check_query, [spot_id, user_id]).fetchone()[0]
            
            if exists:
                # 更新現有評分
                update_query = """
                UPDATE "Comment"
                SET rate = ?, comment_date = ?
                WHERE spot_id = ? AND user_id = ?;
                """
            else:
                # 新增評分
                update_query = """
                INSERT INTO "Comment" (spot_id, user_id, rate, comment_date)
                VALUES (?, ?, ?, ?);
                """
            
            comment_date = datetime.now().strftime('%Y-%m-%d')
            conn.execute(update_query, 
                [rate, comment_date, spot_id, user_id] if exists else 
                [spot_id, user_id, rate, comment_date]
            )
            
            # 立即更新平均評分
            update_ave_rate_in_db(spot_id)
            
            return {
                "status": "success",
                "message": "評分成功"
            }
            
    except Exception as e:
        print(f"Rate spot error: {str(e)}")  # 記錄錯誤
        return {
            "status": "error",
            "message": f"評分失敗: {str(e)}"
        }

# 更新景點平均評分，更新 Spot 表的 ave_rate 欄位，根據 Comment 表的 rate 欄位
def update_ave_rate_in_db(spot_id):
    try:
        with duckdb.connect(DB_FILE) as conn:
            # 計算平均評分
            avg_query = """
            SELECT COALESCE(AVG(CAST(rate AS FLOAT)), 0)
            FROM "Comment"
            WHERE spot_id = ?;
            """
            avg_rate = conn.execute(avg_query, [spot_id]).fetchone()[0]
            
            # 更新景點評分
            update_query = """
            UPDATE "Spot"
            SET ave_rate = ?
            WHERE spot_id = ?;
            """
            conn.execute(update_query, [avg_rate, spot_id])
            
            return {
                "status": "success",
                "message": "平均評分已更新",
                "data": {"spot_id": spot_id, "ave_rate": avg_rate}
            }
            
    except Exception as e:
        print(f"Update average rate error: {str(e)}")  # 記錄錯誤
        return {
            "status": "error",
            "message": f"更新平均評分失敗: {str(e)}"
        }

def edit_spot_in_db(user_id, spot_id, keyword, new_value):
    try:
        # 檢查參數
        if not all([user_id, spot_id, keyword, new_value]):
            return {
                "status": "error",
                "message": "缺少必要參數"
            }

        # 允許修改的欄位
        allowed_fields = {
            "spot_name": "text",
            "address": "text",
            "category": "text",
            "estimate_cost": "integer",
            "estimate_stay_time": "integer"
        }

        # 檢查欄位是否允許修改
        if keyword not in allowed_fields:
            return {
                "status": "error",
                "message": f"不允許修改欄位: {keyword}"
            }

        with duckdb.connect(DB_FILE) as conn:
            # 檢查權限
            check_query = """
            SELECT COUNT(*)
            FROM "Spot"
            WHERE spot_id = ? AND create_by = ?;
            """
            exists = conn.execute(check_query, [spot_id, user_id]).fetchone()[0]

            if not exists:
                return {
                    "status": "error",
                    "message": "無權限編輯此景點或景點不存在"
                }

            # 根據欄位類型處理值
            if allowed_fields[keyword] == "integer":
                try:
                    new_value = int(new_value)
                except ValueError:
                    return {
                        "status": "error",
                        "message": f"{keyword} 必須是數字"
                    }

            # 更新資料
            update_query = f"""
            UPDATE "Spot"
            SET {keyword} = ?
            WHERE spot_id = ? AND create_by = ?;
            """
            
            conn.execute(update_query, [new_value, spot_id, user_id])
            
            return {
                "status": "success",
                "message": "更新成功",
                "data": {
                    "spot_id": spot_id,
                    "updated_field": keyword,
                    "new_value": new_value
                }
            }
            
    except Exception as e:
        print(f"Edit spot error: {str(e)}")  # 記錄錯誤
        return {
            "status": "error",
            "message": f"編輯失敗: {str(e)}"
        }

def create_trip_in_db(user_id, trip_name, description):
    try:
        # 1. 取最新的 trip_id
        query = "SELECT MAX(CAST(SUBSTR(trip_id, 2) AS INT)) FROM \"Trip\";"
        with duckdb.connect(DB_FILE) as conn:
            result = conn.execute(query).fetchone()
        
        # 如果資料表為空，從 T1 開始
        new_trip_id = f"T{result[0] + 1}" if result[0] is not None else "T1"
        
        # 2. 當前時間（create_date 和 collect_date）
        current_date = datetime.now().strftime('%Y-%m-%d')

        # 3. 插入新的 Trip 資料
        insert_query = f"""
        INSERT INTO "Trip" (trip_id, trip_name, description, is_public, create_date, create_by, host)
        VALUES ('{new_trip_id}', '{trip_name}', '{description}', FALSE, '{current_date}', '{user_id}', '{user_id}');
        """
        
        with duckdb.connect(DB_FILE) as conn:
            conn.execute(insert_query)

        # 4. 詢問使用者是否公開此行程
        is_public_input = input("Do you want to make this trip public? (y/n): ").strip().lower()

        # 5. 更新 is_public 欄位
        if is_public_input == 'y':
            update_query = f"""
            UPDATE "Trip"
            SET is_public = TRUE
            WHERE trip_id = '{new_trip_id}';
            """
            with duckdb.connect(DB_FILE) as conn:
                conn.execute(update_query)

        # 6. 返回成功訊息
        return {"status": "success", "message": f"Trip {new_trip_id} created successfully, is_public: {is_public_input == 'y'}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def edit_trip_in_db(user_id, trip_id, keyword, new_value):
    try:
        # 1. 確認使用者是否為 Trip 的創建者或參與者
        query_check_permission = f"""
        SELECT COUNT(*)
        FROM "Trip" t
        LEFT JOIN "ParticipateIn" p ON t.trip_id = p.trip_id
        WHERE t.trip_id = '{trip_id}' AND (t.create_by = '{user_id}' OR p.participant_id = '{user_id}');
        """
        
        with duckdb.connect(DB_FILE) as conn:
            permission = conn.execute(query_check_permission).fetchone()
        
        if permission[0] == 0:
            return {"status": "error", "message": "You do not have permission to edit this trip"}

        # 2. 更新指定的 Trip 屬性
        update_query = f"""
        UPDATE "Trip"
        SET {keyword} = '{new_value}'
        WHERE trip_id = '{trip_id}';
        """
        
        with duckdb.connect(DB_FILE) as conn:
            conn.execute(update_query)
        
        # 3. 返回成功訊息
        return {"status": "success", "message": f"Trip {trip_id} updated successfully, {keyword} changed to {new_value}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def add_user_to_trip_in_db(current_user_id, trip_id, target_user_id=None):
    try:
        # 如果沒有輸入 target_user_id，則使用 current_user_id
        if not target_user_id:
            target_user_id = current_user_id
        
        # 1. 檢查 trip_id 是否存在
        query_check_trip = f"""
        SELECT COUNT(*)
        FROM "Trip"
        WHERE trip_id = '{trip_id}';
        """
        
        with duckdb.connect(DB_FILE) as conn:
            trip_exists = conn.execute(query_check_trip).fetchone()[0]
        
        if trip_exists == 0:
            return {"status": "error", "message": "Trip not found"}

        # 2. 檢查使用者是否已經參與該 Trip
        query_check_participation = f"""
        SELECT COUNT(*)
        FROM "ParticipateIn"
        WHERE trip_id = '{trip_id}' AND participant_id = '{target_user_id}';
        """
        
        with duckdb.connect(DB_FILE) as conn:
            already_participating = conn.execute(query_check_participation).fetchone()[0]
        
        if already_participating > 0:
            return {"status": "error", "message": f"User {target_user_id} is already participating in trip {trip_id}"}

        # 3. 插入新的參與紀錄
        insert_query = f"""
        INSERT INTO "ParticipateIn" (trip_id, participant_id)
        VALUES ('{trip_id}', '{target_user_id}');
        """
        
        with duckdb.connect(DB_FILE) as conn:
            conn.execute(insert_query)

        # 4. 返回成功訊息
        return {"status": "success", "message": f"User {target_user_id} added to trip {trip_id} successfully"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_sth_in_profile_in_db(user_id, keyword):
    try:
        # 檢查允許的欄位
        allowed_fields = ["user_name", "email", "profile_pic"]
        if keyword not in allowed_fields:
            return None
            
        with duckdb.connect(DB_FILE) as conn:
            query = f"""
            SELECT {keyword}
            FROM "User"
            WHERE user_id = ?;
            """
            result = conn.execute(query, [user_id]).fetchone()
            
            return result[0] if result else None
            
    except Exception as e:
        print(f"Database error in get_sth_in_profile: {str(e)}")
        return None

def update_profile_in_db(user_id, keyword, new_value):
    try:
        # 確認 keyword 是否為允許的欄位
        allowed_keywords = ["user_name", "email", "profile_pic"]
        if keyword not in allowed_keywords:
            return {"status": "error", "message": f"Invalid field '{keyword}' for profile update"}

        # 更新指定的欄位
        update_query = f"""
        UPDATE "User"
        SET {keyword} = '{new_value}'
        WHERE user_id = '{user_id}';
        """
        
        with duckdb.connect(DB_FILE) as conn:
            conn.execute(update_query)
        
        # 返回成功訊息
        return {"status": "success", "message": f"Profile updated successfully, {keyword} changed to {new_value}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_friends_in_db(user_id):
    try:
        # SQL 查詢：檢索好友名單
        query = """
        SELECT u.user_id, u.user_name
        FROM "User" u
        JOIN "Friendship" f ON 
            (f.user_id1 = ? AND f.user_id2 = u.user_id)
            OR (f.user_id2 = ? AND f.user_id1 = u.user_id)
        Order by u.user_id;
        """
        
        with duckdb.connect(DB_FILE) as conn:
            results = conn.execute(query, [user_id, user_id]).fetchall()
        
        # 將結果格式化為列表
        friends_list = [
            {
                "id": str(row[0]),  # 確保 ID 是字串
                "name": row[1]
            } 
            for row in results
        ]
        
        return {
            "status": "success",
            "data": friends_list
        }
    
    except Exception as e:
        print(f"Error in get_friends_in_db: {str(e)}")  # 記錄錯誤
        return {
            "status": "error",
            "message": f"無法獲取友列表: {str(e)}"
        }

def add_friend_in_db(current_user_id, target_user_id):
    try:
        # 確保 user_id 排序：比較小的 user_id1，大的在 user_id2
        user_id1, user_id2 = sorted([current_user_id, target_user_id])
        
        # 1. 檢查該好友關係是否已存在
        query_check_relation = f"""
        SELECT COUNT(*)
        FROM "Friendship"
        WHERE user_id1 = '{user_id1}' AND user_id2 = '{user_id2}';
        """
        
        with duckdb.connect(DB_FILE) as conn:
            relation_exists = conn.execute(query_check_relation).fetchone()[0]
        
        if relation_exists > 0:
            return {"status": "error", "message": "This friendship relation already exists"}
        
        # 2. 插入新的好友關係
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 當下的時間
        insert_query = f"""
        INSERT INTO "Friendship" (user_id1, user_id2, friend_begin_date)
        VALUES ('{user_id1}', '{user_id2}', '{create_time}');
        """
        
        with duckdb.connect(DB_FILE) as conn:
            conn.execute(insert_query)
        
        # 3. 返回成功訊息
        return {"status": "success", "message": f"Friendship created between {user_id1} and {user_id2}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def view_profile_in_db(user_id):
    try:
        with duckdb.connect(DB_FILE) as conn:
            # 1. 查詢個人檔案
            profile_query = """
            SELECT user_name, email
            FROM "User"
            WHERE user_id = ?;
            """
            profile_result = conn.execute(profile_query, [user_id]).fetchone()
            
            if not profile_result:
                return {
                    "status": "error",
                    "message": "用戶不存在"
                }

            # 2. 查詢該用戶創建的公開景點
            spots_query = """
            SELECT spot_id, spot_name, address
            FROM "Spot"
            WHERE create_by = ? AND is_public = TRUE;
            """
            spots = conn.execute(spots_query, [user_id]).fetchall()
            
            # 3. 查詢該用戶創建的公開行程
            trips_query = """
            SELECT trip_id, trip_name, description
            FROM "Trip"
            WHERE create_by = ? AND is_public = TRUE;
            """
            trips = conn.execute(trips_query, [user_id]).fetchall()
            
            # 4. 查詢該用戶參與的公開行程
            participating_query = """
            SELECT t.trip_id, t.trip_name, t.description
            FROM "ParticipateIn" p
            JOIN "Trip" t ON p.trip_id = t.trip_id
            WHERE p.participant_id = ? AND t.is_public = TRUE;
            """
            participating = conn.execute(participating_query, [user_id]).fetchall()

            return {
                "status": "success",
                "profile": {
                    "user_name": profile_result[0],
                    "email": profile_result[1]
                },
                "created_spots": [
                    {
                        "spot_id": row[0],
                        "spot_name": row[1],
                        "address": row[2]
                    } for row in spots
                ],
                "created_trips": [
                    {
                        "trip_id": row[0],
                        "trip_name": row[1],
                        "description": row[2]
                    } for row in trips
                ],
                "participating_trips": [
                    {
                        "trip_id": row[0],
                        "trip_name": row[1],
                        "description": row[2]
                    } for row in participating
                ]
            }
    
    except Exception as e:
        print(f"Error in view_profile_in_db: {str(e)}")  # 記錄錯誤
        return {
            "status": "error",
            "message": f"獲取用戶檔案失敗: {str(e)}"
        }

def no_invite_in_db(user_id):
    try:
        with duckdb.connect(DB_FILE) as conn:
            # 1. 查詢使用者的所有好友
            friends_query = f"""
            SELECT DISTINCT 
                CASE 
                    WHEN user_id1 = '{user_id}' THEN user_id2
                    WHEN user_id2 = '{user_id}' THEN user_id1
                END AS friend_id
            FROM "Friendship"
            WHERE user_id1 = '{user_id}' OR user_id2 = '{user_id}';
            """
            friends = conn.execute(friends_query).fetchall()
            friend_ids = {row[0] for row in friends}  # 使用集合存儲好友 ID
            
            if not friend_ids:
                return {"status": "success", "message": "你還沒有好友"}

            # 2. 查詢行程的參與者，加入檢查 host 不是該使用者的條件
            trips_query = f"""
            SELECT DISTINCT t.trip_id, t.trip_name, t.description
            FROM "Trip" t
            JOIN "ParticipateIn" p ON t.trip_id = p.trip_id
            WHERE t.host != '{user_id}'  -- 新增：排除使用者是 host 的行程
            AND NOT EXISTS (
                SELECT 1
                FROM "ParticipateIn" p_inner
                WHERE p_inner.trip_id = t.trip_id
                AND p_inner.participant_id = '{user_id}'  -- 排除使用者參與的行程
            )
            AND NOT EXISTS (
                SELECT 1
                FROM "ParticipateIn" p_inner
                WHERE p_inner.trip_id = t.trip_id
                AND p_inner.participant_id NOT IN (
                    SELECT DISTINCT 
                        CASE 
                            WHEN user_id1 = '{user_id}' THEN user_id2
                            WHEN user_id2 = '{user_id}' THEN user_id1
                        END AS friend_id
                    FROM "Friendship"
                    WHERE user_id1 = '{user_id}' OR user_id2 = '{user_id}'
                )
            );
            """
            trips = conn.execute(trips_query).fetchall()

        # 3. 如果沒有符合條件的行程
        if not trips:
            return {"status": "success", "message": "恭喜，你做人非常成功！"}
        
        # 4. 返回符合條件的行程
        result = {
            "status": "success",
            "trips": [{"trip_id": row[0], "trip_name": row[1], "description": row[2]} for row in trips]
        }
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}
    

def get_random_trips_in_db(count=20):
    """
    隨機從資料庫中選取指定數量的公開行程。
    """
    try:
        query = """
        SELECT trip_id, trip_name, description
        FROM "Trip"
        WHERE is_public = TRUE
        ORDER BY RANDOM()
        LIMIT ?;
        """
        
        with duckdb.connect(DB_FILE) as conn:
            results = conn.execute(query, [count]).fetchall()
            
        return [{
            "trip_id": row[0],
            "trip_name": row[1],
            "description": row[2]
        } for row in results]
        
    except Exception as e:
        print(f"Error getting random trips: {str(e)}")
        return []

def get_trip_details_in_db(trip_id):
    """
    獲取行程詳細資訊，包括景點列表
    """
    try:
        with duckdb.connect(DB_FILE) as conn:
            # 獲取行程基本資訊
            trip_query = """
            SELECT trip_id, trip_name, description, create_by
            FROM "Trip"
            WHERE trip_id = ?;
            """
            trip_info = conn.execute(trip_query, [trip_id]).fetchone()
            
            if not trip_info:
                return {
                    "status": "error",
                    "message": "行程不存在"
                }
            
            # 獲取行程中的景點
            spots_query = """
            SELECT s.spot_name, st.sequence_number
            FROM "SpotInTrip" st
            JOIN "Spot" s ON st.spot_id = s.spot_id
            WHERE st.trip_id = ?
            ORDER BY st.sequence_number;
            """
            spots = conn.execute(spots_query, [trip_id]).fetchall()
            
            return {
                "status": "success",
                "data": {
                    "trip_id": trip_info[0],
                    "trip_name": trip_info[1],
                    "description": trip_info[2],
                    "create_by": trip_info[3],
                    "spots": [
                        {
                            "spot_name": row[0],
                            "sequence_number": row[1]
                        } for row in spots
                    ]
                }
            }
            
    except Exception as e:
        print(f"Error getting trip details: {str(e)}")
        return {
            "status": "error",
            "message": f"獲取行程詳情失敗: {str(e)}"
        }

def get_my_trips_in_db(user_id):
    """
    獲取用戶主辦或參與的所有行程
    """
    try:
        query = """
        SELECT DISTINCT t.trip_id, t.trip_name, t.description
        FROM "Trip" t
        WHERE t.host = ?
        UNION
        SELECT t.trip_id, t.trip_name, t.description
        FROM "Trip" t
        JOIN "ParticipateIn" p ON t.trip_id = p.trip_id
        WHERE p.participant_id = ?
        ORDER BY trip_id;
        """
        
        with duckdb.connect(DB_FILE) as conn:
            results = conn.execute(query, [user_id, user_id]).fetchall()
            
        return {
            "status": "success",
            "trips": [{
                "trip_id": row[0],
                "trip_name": row[1],
                "description": row[2]
            } for row in results]
        }
        
    except Exception as e:
        print(f"Error getting user trips: {str(e)}")
        return {
            "status": "error",
            "message": f"獲取行程失敗: {str(e)}"
        }

def create_empty_trip_in_db(user_id, trip_name, description=""):
    try:
        with duckdb.connect(DB_FILE) as conn:
            # 生成新的 trip_id
            query = """
            SELECT MAX(CAST(SUBSTR(trip_id, 2) AS INT))
            FROM "Trip";
            """
            result = conn.execute(query).fetchone()
            new_trip_id = f"T{result[0] + 1 if result[0] else 1}"
            
            # 插入新行程
            create_date = datetime.now().strftime('%Y-%m-%d')
            insert_query = """
            INSERT INTO "Trip" 
            (trip_id, trip_name, description, is_public, create_date, create_by, host)
            VALUES (?, ?, ?, FALSE, ?, ?, ?);
            """
            
            conn.execute(insert_query, [
                new_trip_id,
                trip_name,
                description,
                create_date,
                user_id,
                user_id
            ])
            
            return {
                "status": "success",
                "message": "行程建立成功",
                "data": {"trip_id": new_trip_id}
            }
            
    except Exception as e:
        print(f"Error creating trip: {str(e)}")
        return {
            "status": "error",
            "message": f"建立行程失敗: {str(e)}"
        }

def edit_trip_spots_in_db(trip_id, spot_id, sequence_number=None, is_new=False):
    try:
        with duckdb.connect(DB_FILE) as conn:
            if is_new:
                # 獲取最大序號
                max_seq_query = """
                SELECT COALESCE(MAX(sequence_number), 0)
                FROM "SpotInTrip"
                WHERE trip_id = ?;
                """
                max_seq = conn.execute(max_seq_query, [trip_id]).fetchone()[0]
                new_seq = max_seq + 1
                
                # 新增景點
                insert_query = """
                INSERT INTO "SpotInTrip" (trip_id, spot_id, sequence_number)
                VALUES (?, ?, ?);
                """
                conn.execute(insert_query, [trip_id, spot_id, new_seq])
            else:
                # 修改現有景點
                update_query = """
                UPDATE "SpotInTrip"
                SET spot_id = ?
                WHERE trip_id = ? AND sequence_number = ?;
                """
                conn.execute(update_query, [spot_id, trip_id, sequence_number])
            
            return {
                "status": "success",
                "message": "行程景點更新成功"
            }
            
    except Exception as e:
        print(f"Error editing trip spots: {str(e)}")
        return {
            "status": "error",
            "message": f"更新行程景點失敗: {str(e)}"
        }

def add_member_to_trip_in_db(trip_id, user_id, friend_id):
    try:
        with duckdb.connect(DB_FILE) as conn:
            # 檢查是否為行程主辦人
            host_check = """
            SELECT COUNT(*)
            FROM "Trip"
            WHERE trip_id = ? AND host = ?;
            """
            is_host = conn.execute(host_check, [trip_id, user_id]).fetchone()[0] > 0
            
            if not is_host:
                return {
                    "status": "error",
                    "message": "只有行程主辦人可以新增成員"
                }
            
            # 檢查是否已經是成員
            member_check = """
            SELECT COUNT(*)
            FROM "ParticipateIn"
            WHERE trip_id = ? AND participant_id = ?;
            """
            is_member = conn.execute(member_check, [trip_id, friend_id]).fetchone()[0] > 0
            
            if is_member:
                return {
                    "status": "error",
                    "message": "該用戶已經是行程成員"
                }
            
            # 新增成員
            insert_query = """
            INSERT INTO "ParticipateIn" (trip_id, participant_id)
            VALUES (?, ?);
            """
            conn.execute(insert_query, [trip_id, friend_id])
            
            return {
                "status": "success",
                "message": "成員新增成功"
            }
            
    except Exception as e:
        print(f"Error adding member to trip: {str(e)}")
        return {
            "status": "error",
            "message": f"新增成員失敗: {str(e)}"
        }