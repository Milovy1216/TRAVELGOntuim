from flask import Flask
from routes import setup_routes

def create_app():
    app = Flask(__name__)
    setup_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    print("伺服器啟動於 http://localhost:8888")
    app.run(host='0.0.0.0', port=8888, debug=True)