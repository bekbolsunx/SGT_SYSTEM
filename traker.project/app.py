### STUDENT TRACKER SYSTEM

from flask import Flask, request, redirect, url_for, flash, render_template, session
from flask_sqlalchemy import SQLAlchemy
import statistics
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

#  User and Grade models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_name = db.Column(db.String(100))
    grade = db.Column(db.String(10))
    date = db.Column(db.String(50))
    teacher_name = db.Column(db.String(100))

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def add_log(user_id, action):
    log = Log(user_id=user_id, action=action)
    db.session.add(log)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            add_log(user.id, 'Logged in')
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/student_board')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    add_log(session['user_id'], 'Viewed student board')
    user = User.query.get(session['user_id'])
    grades = Grade.query.filter_by(user_id=user.id).all()
    grade_values = [float(grade.grade) for grade in grades if grade.grade.isdigit()]
    average_grade = statistics.mean(grade_values) if grade_values else 0

    return render_template('student_board.html', user=user, grades=grades, average_grade=average_grade)

@app.route('/admin')
def admin_panel():
    add_log(-1, 'Viewed admin panel')
    return render_template('admin_panel.html')


@app.route('/add_user')
def add_user_page():
    add_log(-1, 'Viewed add user page')
    return render_template('add_student.html')

@app.route('/api/add_user', methods=['POST'])
def add_user():
    new_user = User(
        username=request.form['username'],
        password=request.form['password'],
        email=request.form['email'],
        phone=request.form['phone'],
        address=request.form['address']
    )
    add_log(-1, 'Added new user ' + request.form['username'])
    db.session.add(new_user)
    db.session.commit()
    flash('User added successfully!')
    return redirect(url_for('admin_panel'))


@app.route("/add_grade")
def add_grade_page():
    add_log(-1, 'Viewed add grade page')
    return render_template('add_grade.html')

@app.route('/all_students')
def all_students():
    add_log(-1, 'Viewed all students page')
    users = User.query.all()
    return render_template('all_students.html', users=users)

@app.route('/api/add_grade', methods=['POST'])
def add_grade():
    new_grade = Grade(
        user_id=request.form['user_id'],
        course_name=request.form['course_name'],
        grade=request.form['grade'],
        date=request.form['date'],
        teacher_name=request.form['teacher_name']
    )
    add_log(-1, 'Added new grade ' + request.form['course_name'])
    db.session.add(new_grade)
    db.session.commit()
    flash('Grade added successfully!')
    return redirect(url_for('admin_panel'))

@app.route('/api/logs', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    list = [{"user_id": log.user_id, "action": log.action, "timestamp": log.timestamp} for log in logs]
    return {'logs': list}

@app.route("/login", methods=["POST"])
def login_admin():
    username = str(request.json.get("username"))
    password = str(request.json.get("password"))
    conn = sqlite3.connect("mysite/students.db")
    c = conn.cursor()
    c.execute(
        "SELECT * FROM user WHERE username = ? AND password = ?",
        (username, password),
    )
    user = c.fetchone()
    session['user_id'] = user[0]
    conn.close()
    add_log(user[0], 'Logged in')
    return {"success":True, "user": user}

@app.route("/dashboard")
def dashboard_student():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    grades = Grade.query.filter_by(user_id=user.id).all()
    add_log(session['user_id'], 'Viewed student board')
    return render_template("student_board.html", user=user, grades=grades)


@app.route('/logout')
def logout():
    add_log(session['user_id'], 'Logged out')
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)













# from flask import Flask, request, redirect, url_for, flash, render_template, session
# from flask_sqlalchemy import SQLAlchemy
# import statistics
# import sqlite3
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
# app.config['SECRET_KEY'] = 'your_secret_key'
# db = SQLAlchemy(app)

# # Define the User and Grade models
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=True)
#     phone = db.Column(db.String(20), nullable=True)
#     address = db.Column(db.String(200), nullable=True)

# class Grade(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     course_name = db.Column(db.String(100))
#     grade = db.Column(db.String(10))
#     date = db.Column(db.String(50))
#     teacher_name = db.Column(db.String(100))
    
# class Log(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     action = db.Column(db.String(100))
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# with app.app_context():
#     db.create_all()
    
# def add_log(user_id, action):
#     log = Log(user_id=user_id, action=action)
#     db.session.add(log)
#     db.session.commit()

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             add_log(user.id, 'Logged in')
#             session['user_id'] = user.id
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid credentials')
#     return render_template('login.html')

# @app.route('/student_board')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     add_log(session['user_id'], 'Viewed student board')
#     user = User.query.get(session['user_id'])
#     grades = Grade.query.filter_by(user_id=user.id).all()
#     grade_values = [float(grade.grade) for grade in grades if grade.grade.isdigit()]
#     average_grade = statistics.mean(grade_values) if grade_values else 0

#     return render_template('student_board.html', user=user, grades=grades, average_grade=average_grade)

# @app.route('/admin')
# def admin_panel():
#     add_log(session['user_id'], 'Viewed admin panel')   
#     return render_template('admin_panel.html')


# @app.route('/add_user')
# def add_user_page():
#     add_log(session['user_id'], 'Viewed add user page')
#     return render_template('add_student.html')

# @app.route('/api/add_user', methods=['POST'])
# def add_user():
#     new_user = User(
#         username=request.form['username'],
#         password=request.form['password'],
#         email=request.form['email'],
#         phone=request.form['phone'],
#         address=request.form['address']
#     )
#     add_log(session['user_id'], 'Added new user ' + request.form['username'])
#     db.session.add(new_user)
#     db.session.commit()
#     flash('User added successfully!')
#     return redirect(url_for('admin_panel'))

# # @app.route('/manage_users')
# # def manage_users():
# #     return render_template('manage_users.html')

# @app.route("/add_grade")
# def add_grade_page():
#     add_log(session['user_id'], 'Viewed add grade page')
#     return render_template('add_grade.html')

# @app.route('/all_students')
# def all_students():
#     add_log(session['user_id'], 'Viewed all students page')
#     users = User.query.all()
#     return render_template('all_students.html', users=users)

# @app.route('/api/add_grade', methods=['POST'])
# def add_grade():
#     new_grade = Grade(
#         user_id=request.form['user_id'],
#         course_name=request.form['course_name'],
#         grade=request.form['grade'],
#         date=request.form['date'],
#         teacher_name=request.form['teacher_name']
#     )
#     add_log(session['user_id'], 'Added new grade ' + request.form['course_name'])
#     db.session.add(new_grade)
#     db.session.commit()
#     flash('Grade added successfully!')
#     return redirect(url_for('admin_panel'))

# @app.route('/api/logs', methods=['GET'])
# def get_logs():
#     logs = Log.query.all()
#     list = [{"user_id": log.user_id, "action": log.action, "timestamp": log.timestamp} for log in logs]
#     return {'logs': list}

# @app.route("/login", methods=["POST"])
# def login_admin():
#     username = str(request.json.get("username"))
#     password = str(request.json.get("password"))
#     conn = sqlite3.connect("instance/students.db")
#     c = conn.cursor()
#     c.execute(
#         "SELECT * FROM user WHERE username = ? AND password = ?",
#         (username, password),
#     )
#     user = c.fetchone()
#     session['user_id'] = user[0]
#     conn.close()
#     add_log(user[0], 'Logged in')
#     return {"success":True, "user": user}

# @app.route("/dashboard")
# def dashboard_student():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     user = User.query.get(session['user_id'])
#     grades = Grade.query.filter_by(user_id=user.id).all()
#     add_log(session['user_id'], 'Viewed student board')
#     return render_template("student_board.html", user=user, grades=grades)


# @app.route('/logout')
# def logout():
#     add_log(session['user_id'], 'Logged out')
#     session.pop('user_id', None)
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for, flash
# from user_management import add_user, authenticate_user


# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if add_user(username, password):
#             flash('Registration successful! Please login.', 'success')
#             return redirect(url_for('login'))
#         else:
#             flash('Username already exists!', 'error')
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if authenticate_user(username, password):
#             flash('Login successful!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid username or password', 'error')
#     return render_template('login.html')

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')



# #for debugging purposes
# if __name__ == '__main__':
#     app.run(debug=True)
