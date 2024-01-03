from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchinghistory import app, db
from watchinghistory.models import User, WatchingHistory

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] # Get username from form
        password = request.form['password'] # Get password from form

        if not username or not password:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success')
            return redirect(url_for('index'))
        
        # If username or password is wrong
        flash('Invalid username or password')

        # Back to login page
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required # Protect this route
def logout():
    logout_user()
    flash('Logout success')
    return redirect(url_for('index'))


# Route to display the watching history
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # 檢查登入狀態
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
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
        # 檢查登入狀態
        if not current_user.is_authenticated:
            flash('Please login to see the history')
            return redirect(url_for('login'))
        # 獲取所有資料
        history = WatchingHistory.query.order_by(WatchingHistory.date_created).all()
        # 傳資料到index.html
        return render_template("index.html", history=history)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    # 從資料庫取得該task
    history_to_delete = WatchingHistory.query.get_or_404(id)

    try:
        # 刪除該task
        db.session.delete(history_to_delete)
        db.session.commit()
        flash('History deleted')
        return redirect('/')
    except:
        return 'There was an issue deleting the history'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required    
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
            flash('History updated')
            return redirect('/')
        except:
            return 'There was an issue updating your history'
    else:
        return render_template('update.html', history=history)