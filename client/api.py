from flask import Flask, request, jsonify
import requests

BASE_URL = "http://localhost:8888"

def login_user(user_id, password):
    """
    登入用戶
    :param user_id: 用戶 ID
    :param password: 密碼
    :return: 伺服器回應
    """
    try:
        response = requests.post(f"{BASE_URL}/login", json={
            "user_id": user_id,
            "password": password
        })
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"status": "fail", "message": "用戶 ID 或密碼錯誤"}
        else:
            return {"status": "error", "message": f"伺服器錯誤: {response.status_code}"}
            
    except Exception as e:
        return {"status": "error", "message": f"連接錯誤: {str(e)}"}

def test_connection():
    try:
        response = requests.get(f"{BASE_URL}/ping")
        if response.status_code == 200:
            print("成功連接到伺服器")
            return True
    except Exception as e:
        print(f"連接失敗: {str(e)}")
        return False
    
def get_spots():
    response = requests.get(f"{BASE_URL}/spots/get")
    return response.json()

def search_spot(keyword):
    response = requests.get(f"{BASE_URL}/search/spots", params={"keyword": keyword})
    return response.json()

def view_my_spots(user_id):
    response = requests.get(f"{BASE_URL}/view/my_spots", params={"user_id": user_id})
    return response.json()

def view_my_trips(user_id):
    response = requests.get(f"{BASE_URL}/view/my_trips", params={"user_id": user_id})
    return response.json()

def search_trip(keyword):
    response = requests.get(f"{BASE_URL}/search/trips", params={"keyword": keyword})
    return response.json()

def collect_spot(user_id, spot_id):
    response = requests.post(f"{BASE_URL}/spot/collect", json={
        "user_id": user_id,
        "spot_id": spot_id
    })
    return response.json()

def collect_trip(user_id, trip_id):
    response = requests.post(f"{BASE_URL}/trip/collect", json={
        "user_id": user_id,
        "trip_id": trip_id
    })
    return response.json()

def create_spot(user_id, spot_name, address, category, estimate_cost, estimate_stay_time):
    response = requests.post(f"{BASE_URL}/spot/create", json={
        "user_id": user_id,
        "spot_name": spot_name,
        "address": address,
        "category": category,
        "estimate_cost": estimate_cost,
        "estimate_stay_time": estimate_stay_time
    })
    return response.json()

def set_spot_public(spot_id):
    response = requests.post(f"{BASE_URL}/spot/set_public", json={
        "spot_id": spot_id
    })
    return response.json()

def edit_spot(user_id, spot_id, keyword, new_value):
    try:
        response = requests.put(
            f"{BASE_URL}/spots/edit",
            json={
                "user_id": user_id,
                "spot_id": spot_id,
                "keyword": keyword,
                "new_value": new_value
            }
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "message": f"伺服器錯誤: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"請求失敗: {str(e)}"
        }

def rate_spot(user_id, spot_id, rate):
    response = requests.post(f"{BASE_URL}/spot/rate", json={
        "user_id": user_id,
        "spot_id": spot_id,
        "rate": rate
    })
    return response.json()

def update_ave_rate(spot_id):
    response = requests.post(f"{BASE_URL}/spot/update_ave_rate", json={
        "spot_id": spot_id
    })
    return response.json()

# def create_trip(user_id, trip_name, region):
    response = requests.post(f"{BASE_URL}/trip/create", json={
        "user_id": user_id,
        "trip_name": trip_name,
        "region": region
    })
    return response.json()

def edit_trip(user_id, trip_id, keyword, new_value):
    response = requests.put(f"{BASE_URL}/trip/edit", json={
        "user_id": user_id,
        "trip_id": trip_id,
        "keyword": keyword,
        "new_value": new_value
    })
    return response.json()

def add_user_to_trip(trip_id, user_id):
    response = requests.post(f"{BASE_URL}/trip/add_user", json={
        "trip_id": trip_id,
        "user_id": user_id
    })
    return response.json()

def get_sth_in_profile(user_id, keyword):
    try:
        response = requests.get(
            f"{BASE_URL}/profile/get",
            params={
                "user_id": user_id,
                "keyword": keyword
            }
        )
        
        if response.status_code == 200:
            return response.json().get("data")
        else:
            print(f"獲取資料失敗: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"請求失敗: {str(e)}")
        return None

def update_profile(user_id, keyword, new_value):
    response = requests.put(f"{BASE_URL}/profile/update", json={
        "user_id": user_id,
        "keyword": keyword,
        "new_value": new_value
    })
    return response.json()

def get_friends(user_id):
    """
    獲取用戶的好友列表
    :param user_id: 用戶 ID
    :return: 好友列表
    """
    try:
        response = requests.get(
            f"{BASE_URL}/friends",
            params={"user_id": user_id}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "message": f"伺服器錯誤: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"請求失敗: {str(e)}"
        }

def add_friend(user_id, friend_id):
    response = requests.post(f"{BASE_URL}/friends/add", json={
        "user_id": user_id, 
        "friend_id": friend_id
    })
    return response.json()

def view_profile(user_id):
    response = requests.get(f"{BASE_URL}/profile/view", params={"user_id": user_id})
    return response.json()

def get_random_trips():
    response = requests.get(f"{BASE_URL}/trips/get")
    return response.json()

def get_trip_details(trip_id):
    response = requests.get(f"{BASE_URL}/trips/details/{trip_id}")
    return response.json()

def get_my_trips(user_id):
    response = requests.get(f"{BASE_URL}/trips/my", params={"user_id": user_id})
    return response.json()

def create_empty_trip(user_id, trip_name, description=""):
    response = requests.post(f"{BASE_URL}/trips/create_empty", json={
        "user_id": user_id,
        "trip_name": trip_name,
        "description": description
    })
    return response.json()

def edit_trip_spots(trip_id, spot_id, sequence_number=None, is_new=False):
    response = requests.post(f"{BASE_URL}/trips/edit_spots", json={
        "trip_id": trip_id,
        "spot_id": spot_id,
        "sequence_number": sequence_number,
        "is_new": is_new
    })
    return response.json()

def add_member_to_trip(trip_id, user_id, friend_id):
    response = requests.post(f"{BASE_URL}/trips/add_member", json={
        "trip_id": trip_id,
        "user_id": user_id,
        "friend_id": friend_id
    })
    return response.json()

def no_invite(user_id):
    """
    獲取所有參與者都是好友但自己未參與的旅程
    """
    try:
        response = requests.get(
            f"{BASE_URL}/trips/no_invite",
            params={"user_id": user_id}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "message": f"伺服器錯誤: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"請求失敗: {str(e)}"
        }