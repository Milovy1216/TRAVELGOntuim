from flask import request, jsonify
from flask import Flask
from database import (
    search_spot_in_db, search_trip_in_db, 
    collect_spot_in_db, collect_trip_in_db,
    create_spot_in_db, edit_spot_in_db,
    create_trip_in_db, edit_trip_in_db,
    add_user_to_trip_in_db, update_profile_in_db,
    get_friends_in_db, add_friend_in_db,
    view_profile_in_db, get_random_spots_in_db,
    set_spot_public_in_db,check_login_in_db,
    view_my_spot_in_db, view_my_trip_in_db,
    rate_spot_in_db, update_ave_rate_in_db,
    get_sth_in_profile_in_db,
    get_random_trips_in_db, get_trip_details_in_db,
    get_my_trips_in_db, create_empty_trip_in_db,
    edit_trip_spots_in_db, add_member_to_trip_in_db,
    no_invite_in_db
)

app = Flask(__name__)

def setup_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        """
        登入路由，驗證用戶 ID 和密碼
        """
        try:
            # 獲取請求中的 JSON 數據
            data = request.json
            user_id = data.get("user_id")
            password = data.get("password")

            # 檢查參數是否完整
            if not user_id or not password:
                return jsonify({"status": "fail", "message": "缺少用戶 ID 或密碼"}), 400

            # 調用資料庫檢查函數
            result = check_login_in_db(user_id, password)
            if result["status"] == "success":
                return jsonify(result), 200
            else:
                return jsonify(result), 401
        except Exception as e:
            return jsonify({"status": "error", "message": f"伺服器錯誤: {e}"}), 500

    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({"message": "pong"})
    
    @app.route('/spots/get', methods =['GET'])
    def get_spot():
        results = get_random_spots_in_db()
        return jsonify(results)

    @app.route('/search/spots', methods=['GET'])
    def search_spots():
        keyword = request.args.get('keyword')
        if not keyword:
            return jsonify({"error": "Missing keyword parameter"}), 400
        results = search_spot_in_db(keyword)
        return jsonify(results)
    
    @app.route('/view/my_spots', methods=['GET'])
    def view_my_spots():
        user_id = request.args.get('user_id')
        results = view_my_spot_in_db(user_id)
        return jsonify(results)
    
    @app.route('/view/my_trips', methods=['GET'])
    def view_my_trips():
        user_id = request.args.get('user_id')
        results = view_my_trip_in_db(user_id)
        return jsonify(results)
    
    @app.route('/search/trips', methods=['GET'])
    def search_trips():
        keyword = request.args.get('keyword')
        if not keyword:
            return jsonify({"error": "Missing keyword parameter"}), 400
        results = search_trip_in_db(keyword)
        return jsonify(results)

    @app.route('/spot/collect', methods=['POST'])
    def collect_spot():
        data = request.json
        user_id = data.get('user_id')
        spot_id = data.get('spot_id')
        result = collect_spot_in_db(user_id, spot_id)
        return jsonify(result)

    @app.route('/trip/collect', methods=['POST'])
    def collect_trip():
        data = request.json
        user_id = data.get('user_id')
        trip_id = data.get('trip_id')
        result = collect_trip_in_db(user_id, trip_id)
        return jsonify(result)

    @app.route('/spot/create', methods=['POST'])
    def create_spot():
        data = request.json
        result = create_spot_in_db(
            data.get('user_id'),
            data.get('spot_name'),
            data.get('address'),
            data.get('category'),
            data.get('estimate_cost'),
            data.get('estimate_stay_time')
        )
        return jsonify(result)

    @app.route('/spot/set_public', methods=['POST'])
    def set_spot_public():
        data = request.json
        spot_id = data.get('spot_id')
        result = set_spot_public_in_db(spot_id)
        return jsonify(result)
    
    @app.route('/spot/rate', methods=['POST'])
    def rate_spot():
        data = request.json
        user_id = data.get('user_id')
        spot_id = data.get('spot_id')
        rate = data.get('rate')
        result = rate_spot_in_db(spot_id, user_id, rate)
        return jsonify(result)
    
    @app.route('/spot/update_ave_rate', methods=['POST'])
    def update_ave_rate():
        data = request.json
        spot_id = data.get('spot_id')
        result = update_ave_rate_in_db(spot_id)
        return jsonify(result)
    
    @app.route('/spots/edit', methods=['PUT'])
    def edit_spot():
        try:
            data = request.json
            if not data:
                return jsonify({
                    "status": "error",
                    "message": "未收到資料"
                }), 400
                
            result = edit_spot_in_db(
                data.get('user_id'),
                data.get('spot_id'),
                data.get('keyword'),
                data.get('new_value')
            )
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"伺服器錯誤: {str(e)}"
            }), 500

    @app.route('/trips/create', methods=['POST'])
    def create_trip():
        data = request.json
        result = create_trip_in_db(
            data.get('user_id'),
            data.get('trip_name'),
            data.get('description')
        )
        return jsonify(result)

    @app.route('/trips/edit', methods=['PUT'])
    def edit_trip():
        try:
            data = request.json
            result = edit_trip_in_db(
                data.get('user_id'),
                data.get('trip_id'),
                data.get('keyword'),
                data.get('new_value')
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"伺服器錯誤: {str(e)}"
            }), 500

    @app.route('/trips/add_user', methods=['POST'])
    def add_user_to_trip():
        data = request.json
        result = add_user_to_trip_in_db(
            data.get('current_user_id'),
            data.get('trip_id'),
            data.get('target_user_id')
        )
        return jsonify(result)
    
    @app.route('/profile/get', methods=['GET'])
    def get_sth_in_profile():
        try:
            user_id = request.args.get('user_id')
            keyword = request.args.get('keyword')
            
            if not user_id or not keyword:
                return jsonify({
                    "status": "error",
                    "message": "Missing required parameters"
                }), 400
                
            result = get_sth_in_profile_in_db(user_id, keyword)
            return jsonify({
                "status": "success",
                "data": result
            })
            
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"伺服器錯誤: {str(e)}"
            }), 500

    @app.route('/profile/update', methods=['PUT'])
    def update_profile():
        data = request.json
        result = update_profile_in_db(
            data.get('user_id'),
            data.get('keyword'),
            data.get('new_value')
        )
        return jsonify(result)

    @app.route('/friends', methods=['GET'])
    def get_friends():
        user_id = request.args.get('user_id')
        result = get_friends_in_db(user_id)
        return jsonify(result)

    @app.route('/friends/add', methods=['POST'])
    def add_friend():
        data = request.json
        result = add_friend_in_db(
            data.get('user_id'),
            data.get('friend_id')
        )
        return jsonify(result)

    @app.route('/profile/view', methods=['GET'])
    def view_profile():
        try:
            user_id = request.args.get('user_id')
            if not user_id:
                return jsonify({"status": "error", "message": "Missing user_id parameter"}), 400
            
            result = view_profile_in_db(user_id)
            return jsonify(result)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"伺服器錯誤: {str(e)}"
            }), 500

    @app.route('/trips/get', methods=['GET'])
    def get_random_trips():
        results = get_random_trips_in_db()
        return jsonify(results)

    @app.route('/trips/details/<trip_id>', methods=['GET'])
    def get_trip_details(trip_id):
        result = get_trip_details_in_db(trip_id)
        return jsonify(result)

    @app.route('/trips/my', methods=['GET'])
    def get_my_trips():
        user_id = request.args.get('user_id')
        result = get_my_trips_in_db(user_id)
        return jsonify(result)

    @app.route('/trips/create_empty', methods=['POST'])
    def create_empty_trip():
        data = request.json
        result = create_empty_trip_in_db(
            data.get('user_id'),
            data.get('trip_name'),
            data.get('description', '')
        )
        return jsonify(result)

    @app.route('/trips/edit_spots', methods=['POST'])
    def edit_trip_spots():
        data = request.json
        result = edit_trip_spots_in_db(
            data.get('trip_id'),
            data.get('spot_id'),
            data.get('sequence_number'),
            data.get('is_new', False)
        )
        return jsonify(result)

    @app.route('/trips/add_member', methods=['POST'])
    def add_member_to_trip():
        data = request.json
        result = add_member_to_trip_in_db(
            data.get('trip_id'),
            data.get('user_id'),
            data.get('friend_id')
        )
        return jsonify(result)

    @app.route('/trips/no_invite', methods=['GET'])
    def no_invite():
        user_id = request.args.get('user_id')
        result = no_invite_in_db(user_id)
        return jsonify(result)