from flask import Flask, jsonify
from config import EMP_FILE_PATH
from app.core.parser import parse_emp

app = Flask(__name__)

@app.route("/")
def index():
    data = parse_emp(EMP_FILE_PATH)
    return jsonify(data)

if __name__ == "__main__":
    from config import FLASK_PORT, FLASK_DEBUG
    app.run(debug=FLASK_DEBUG, port=FLASK_PORT)
