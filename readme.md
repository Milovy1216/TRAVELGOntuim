TRAVELGO!
簡介
TRAVELGO是一個旅遊規劃與分享的平台，分為客戶端和伺服器端，幫助用戶探索景點、典藏行程，並與好友互動。

**安裝指南**：
由.venv開啟終端機，執行下列三行程式碼，安裝flask,duckdb等需要的物件：
pip install flask
pip install duckdb
pip install requests

確保 Python 版本為 3.8 以上。
**檔案結構**：
client/ 客戶端

```main.py```
主程式入口，負責管理主頁面與其他子頁面之間的流轉邏輯。
使用 views.py 定義的頁面函式顯示功能選項，並呼叫 api.py 傳送請求到伺服器。
```views.py```
包含所有用戶可見的頁面邏輯，如主頁、探索頁、典藏頁和個人檔案頁。
每個頁面會呼叫 api.py 來執行伺服器互動，並將結果顯示給用戶。
```api.py```
封裝所有與伺服器的 HTTP 請求邏輯。
提供易於使用的函式，例如 get_() 或 add_to_collection()。


server/ 伺服器端

```server.py```
啟動伺服器，負責將請求分派給對應的路由（由 routes.py 定義）。
```database.py```
負責與 DuckDB 資料庫互動，包括初始化資料庫、執行查詢和回傳結果。
```routes.py```
定義伺服器的 API 路由，處理探索、典藏、個人檔案等請求。
路由函式會呼叫 database.py 完成資料庫操作。

data/
存放與資料庫以及其初始化相關的檔案

**操作說明**：
執行server/server.py，確認開啟伺服器端後，到client/main.py執行程式，之後便可跟隨終端機上顯示指令進行。
提供其中一組user的帳密為：
user_id:U1
password:j2~{W!)Fx5