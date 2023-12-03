from datetime import datetime
from flask import Flask, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Init. the Flask app
app = Flask(__name__)

# Config. database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///watching-history.db"
# Init. database
db = SQLAlchemy(app)


# Create a model for database
class WatchingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    season = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    episode = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Return a string when create a new element
    def __repr__(self):
        return "<Watching History %r>" % self.id


# Route to display the watching history
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # 收到資料
        history_title = request.form["title"]
        history_season = request.form["season"]
        history_value = request.form["value"]
        history_episode = request.form["episode"]
        history_progress = request.form["progress"]

        # 資料轉換為WatchingHistory class
        new_history = WatchingHistory(
            title=history_title,
            season=history_season,
            value=history_value,
            episode=history_episode,
            progress=history_progress,
        )

        try:
            # 資料加入
            db.session.add(new_history)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding the history"
    else:
        # 獲取所有資料
        history = WatchingHistory.query.order_by(WatchingHistory.date_created).all()
        # 傳資料到index.html
        return render_template("index.html", history=history)

@app.route('/delete/<int:id>')
def delete(id):
    # 從資料庫取得該task
    history_to_delete = WatchingHistory.query.get_or_404(id)

    try:
        # 刪除該task
        db.session.delete(history_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting the history'

@app.route('/update/<int:id>', methods=['GET', 'POST'])    
def update(id):
    # 從資料庫取得該history
    history = WatchingHistory.query.get_or_404(id)

    if request.method == 'POST':
        # 取得用戶輸入的資料
        history.title = request.form['title']
        history.season = request.form['season']
        history.value = request.form['value']
        history.episode = request.form['episode']
        history.progress = request.form['progress']
        
        try:
            # 更新資料庫
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your history'
    else:
        return render_template('update.html', history=history)

if __name__ == "__main__":
    app.run(debug=True)
