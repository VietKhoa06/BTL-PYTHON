from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)
CSV_FILE = 'cầu thủ thi đấu trên 90ph.csv'

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return None

@app.route('/api/player', methods=['GET'])
def get_player_stats():
    player_name = request.args.get('name')

    if not player_name:
        return jsonify({"error": "Vui lòng cung cấp tên cầu thủ qua tham số 'name'."}), 400

    df = load_data()
    if df is None:
        return jsonify({"error": f"Không tìm thấy file dữ liệu {CSV_FILE}."}), 500
    result = df[df['Player'].str.lower() == player_name.strip().lower()]
    if result.empty:
        return jsonify({"message": f"Không tìm thấy cầu thủ có tên: {player_name}"}), 404
    player_data = result.to_dict(orient='records')[0]

    return jsonify({
        "status": "success",
        "data": player_data
    })

@app.route('/api/players/all', methods=['GET'])
def get_all_players():
    df = load_data()
    if df is not None:
        players = df['Player'].tolist()
        return jsonify({"total": len(players), "players": players})
    return jsonify({"error": "Data not found"}), 500

if __name__ == '__main__':
    print("Server đang khởi chạy tại http://127.0.0.1:5000")
    app.run(debug=True)