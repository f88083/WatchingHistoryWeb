from flask import Flask, render_template, request, jsonify
import json

# Init. the Flask app
app = Flask(__name__)

# List to store the viewing history
viewing_history = []

# Route to display the viewing history
@app.route('/')
def index():
    return render_template('index.html', history=viewing_history)

# Route to add a new entry to the viewing history
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    category = request.form['category']
    progress = int(request.form['progress'])

    new_entry = {'title': title, 'category': category, 'progress': progress}
    viewing_history.append(new_entry)

    return jsonify({'success': True, 'history': viewing_history})

if __name__ == '__main__':
    app.run(debug=True)