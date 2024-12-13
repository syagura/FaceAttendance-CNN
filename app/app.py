from flask import Flask, render_template, request, url_for, session, redirect, make_response
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os 
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_session import Session
import secrets
from threading import Lock
from flask_socketio import SocketIO, emit


app = Flask(__name__)

app.secret_key = 'secretkeyhere'

socketio = SocketIO(app)
thread = None
thread_lock = Lock()
scheduler = BackgroundScheduler()

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")

app.config['MYSQL_HOST'] = {DB_HOST}
app.config['MYSQL_USER'] = {DB_USERNAME}
app.config['MYSQL_PASSWORD'] = {DB_PASSWORD}
app.config['MYSQL_DB'] = {DB_NAME}

app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

mysql = MySQL(app)
users = []

def get_user_by_sid(sid):
    for user in users:
        if user['sid'] == sid:
            return user
    print(f"No user found for sid: {sid}")
    return None

@app.before_request
def before_request():
    if 'session_id' in request.cookies:
        sid = request.cookies.get('session_id')
        user_data = get_user_by_sid(sid)
        if user_data:
            print(f"User Data: {user_data}")
            session['id'] = user_data.get('id')
            session['username'] = user_data.get('username')
            session['role'] = user_data.get('role')
        else:
            print("No user data found.")
            session.clear() 

@app.route('/', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST' and 'NIP-NIM' in request.form and 'password' in request.form:
        session.pop('user_id', None)
        user_id = request.form['NIP-NIM']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM lecturer WHERE nip = % s \
                    AND password = % s', (user_id, password))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['nip']
            session['username'] = account['lecture_name']
            session['role'] = account['role']
            sid = secrets.token_hex(16)
            session['sid'] = sid
            users.append({'id' : session['id'], 'username' : session['username'], 'role' : session['role'], 'sid':sid})
            print(f'{users}')

            response = make_response(redirect(url_for('home')))
            response.set_cookie('session_id', sid)
            return response
            
        else:
            cur.execute('SELECT * FROM student WHERE nim = % s\
                        AND password = % s', (user_id, password))
            account = cur.fetchone()
            if account:
                session['loggedin'] = True
                session['id'] = account['nim']
                session['username'] = account['student_name']
                session['role'] = account['role']
                sid = secrets.token_hex(16)
                session['sid'] = sid
                users.append({'id' : session['id'], 'username' : session['username'], 'role' : session['role'], 'sid':sid})
                print(f'{users}')

                response = make_response(redirect(url_for('home')))
                response.set_cookie('session_id', sid)
                return response
            else:
                msg = 'Logged in failed please check NIM or password !'

    return render_template('auth/login.html', title='Login', msg=msg)

@app.route('/dashboard/')
def home():
    if 'loggedin' in session:
        account = {
            'id' : session['id'],
            'username' : session['username'],
            'role': session['role']
        }
        if account['role'] == 'lecture':
            username = account['username']
            return render_template('lecture/home.html',  username=username)
        else:
            username = account['username']
            return render_template('student/home.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/jadwal/')
def history():
    if 'loggedin' in session:
        account = {
            'id' : session['id'],
            'username' : session['username'],
            'role': session['role']
        }
        if account['role'] == 'lecture':
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM schedule INNER JOIN lesson ON schedule.lesson_id = lesson.lesson_id WHERE schedule.lecture_id = %s', (account['id'],))
            schedule = cur.fetchall()
            return render_template('lecture/schedule.html', active='attendance', schedule=schedule)

        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM student_shcedule WHERE student_id = %s',(account['id'],))
            schedule = cur.fetchall()
            data = []
            for schedule_row in schedule:
                cur.execute('SELECT * FROM schedule INNER JOIN lesson ON schedule.lesson_id = lesson.id_mk WHERE schedule_id = %s', (schedule_row['schedule_id'],))
                join_data = cur.fetchall()
                data.extend(join_data)
            return render_template('student/schedule.html', active='attendance', data=data)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    socketio.run(app,debug=True)