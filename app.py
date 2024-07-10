from flask import Flask, request, jsonify, send_from_directory, render_template
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'pairings.html')

@app.route('/pairings.css')
def css():
    return send_from_directory('.', 'pairings.css')

@app.route('/pairings.js')
def js():
    return send_from_directory('.', 'pairings.js')

@app.route('/pairing_options')
def pairing_options():
    return send_from_directory('.', 'pairing_options.html')

@app.route('/pairing_options.js')
def pairing_options_js():
    return send_from_directory('.', 'pairing_options.js')

@app.route('/newT')
def new_t():
    rounds = request.args.get('rounds', 1)
    return render_template('newT.html', rounds=rounds)

@app.route('/newT.css')
def new_t_css():
    return send_from_directory('.', 'newT.css')

@app.route('/newT.js')
def new_t_js():
    return send_from_directory('.', 'newT.js')

@app.route('/round_robin')
def round_robin():
    return send_from_directory('.', 'round_robin.html')

@app.route('/round_robin.css')
def round_robin_css():
    return send_from_directory('.','round_robin.css')

@app.route('/round_robin.js')
def round_robin_js():
    return send_from_directory('.','round_robin.js')

@app.route('/add_player', methods=['POST'])
def add_player():
    try:
        cid = request.form.get('cid')
        if cid:
            result = subprocess.run(['python3', 'ratings.py', cid], capture_output=True, text=True)
            print(f"Result stdout: {result.stdout}")
            try:
                player_data = json.loads(result.stdout)
                return jsonify(player_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                print(f"Response text: {result.stdout}")
                return jsonify({'error': 'Error parsing player details'}), 500
        else:
            name = request.form.get('name')
            if name:
                manual_details = {
                    'cid': name,
                    'name': name,
                    'official_published_rating': 0,
                    'sex': 'N/A'
                }
                return jsonify(manual_details)
            return jsonify({'error': 'Player not found and no manual entry provided'}), 404
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': 'Unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
