import duckdb

# 資料庫文件的路徑
DB_FILE = "data/travelgo"

# 測試資料庫連接和簡單查詢
def test_database_connection():
    try:
        # 連接到資料庫
        conn = duckdb.connect(DB_FILE)
        print("成功連接到資料庫！")

        # 執行簡單查詢來測試連接是否成功
        query = "SELECT * FROM Password LIMIT 5;"  # 隨便選擇一個存在的表格（例如：Spot）
        result = conn.execute(query).fetchall()

        if result:
            print("成功執行查詢：")
            for row in result:
                print(row)
        else:
            print("查詢結果為空。")

        # 關閉連接
        conn.close()

    except Exception as e:
        print(f"資料庫連接或查詢失敗: {e}")

if __name__ == "__main__":
    test_database_connection()
