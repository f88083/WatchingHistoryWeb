from flask import Flask, render_template, request, jsonify
import json

# Init. the Flask app
app = Flask(__name__)

# Path to the JSON file
JSON_FILE_PATH = 'data/watching_history.json'

# Load initial watching history from the JSON file if it exists
def load_watching_history():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

watching_history = load_watching_history()

# Route to display the watching history
@app.route('/')
def index():
    return render_template('index.html', history=watching_history)

# Route to add a new entry to the watching history
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    category = request.form['category']
    progress = int(request.form['progress'])

    new_entry = {'title': title, 'category': category, 'progress': progress}
    watching_history.append(new_entry)

    # Save updated watching history to the JSON file
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(watching_history, file, indent=2)

    return jsonify({'success': True, 'history': watching_history})

if __name__ == '__main__':
    app.run(debug=True)