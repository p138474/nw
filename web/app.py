# -*- coding: utf8 -*-
from flask import Flask, render_template, request, g, redirect, session, escape
import hashlib
import sqlite3

# render_template : 템플릿을 랜더한다..?
# redirect : 이미 로그인 했을 경우, 다시 원래페이지로 돌아가는 기능
# session : 로그인되었다는 상태 유지

DATABASE = 'database.db'

app = Flask(__name__)
app.secret_key = b'_wlkfjlkdjmnwlslke26k'

def get_db():                   # 데이터베이스를 가져온다
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False, modify=False):
    cur = get_db().execute(query, args)
    if modify:
        try:
            get_db().commit()
            cur.close()
        except:
            return False
        return True
    rv = cur.fetchall()         # 데이터를 적정 수준만큼 끊어서 가져오는게 좋음 (백만개 중 만개씩) ex) 게시판 글
    cur.close()
    return (rv[0] if rv else None) if one else rv       #if one이 거짓이라면 rv를 return
                                                        #if rv가 0이면 첫번째 값, 결과값이 없으면 None

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/login')


@app.route("/")
def hello():
    if 'id' in session:
        return u'로그인 완료 %s <a href="/logout">logout</a>' % escape(session['id'])
    return render_template("login.html")

@app.route("/name")
def name():
    return "yerin"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['id'].strip()
        pw = hashlib.sha1(request.form['pw'].strip()).hexdigest()
        sql = "select * from user where id='%s' and password='%s'" % (id, pw)
        if query_db(sql, one=True):
            # 로그인이 성공한 경우
            session['id'] = id
            return redirect("/")
        else:
            # 로그인이 실패한 경우
            return "<script>alert('login fail');history.back(-1);</script>"

# digest : 메세지 축약, 내용을 간단히 추려 적음

    if 'id' in session:
        return redirect("/")

    return render_template("login.html")

@app.route("/join", methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        id = request.form['id']
        pw = hashlib.sha1(request.form['pw'].strip()).hexdigest()

        sql = "select * from user where id='%s'" % id
        if query_db(sql, one=True):
            return "<script>alert('join fail');history.back(-1);</script>"

        sql = "insert into user(id, password) values('%s', '%s')" % (id, pw)
        query_db(sql, modify=True)

        return redirect("/login")

    if 'id' in session:
        return redirect("/")

    return render_template("join.html")

@app.route("/add")
@app.route("/add/<int:num1>")
@app.route("/add/<int:num1>/<int:num2>")
def add(num1=None, num2=None):
    if num1 is None or num2 is None:
        return "/add/num1/num2"
    return str(num1 + num2)
 
@app.route("/sub/<int:num1>/<int:num2>")
def sub(num1, num2):
    return str(num1 - num2)

@app.route("/multiply/<int:num1>/<int:num2>")
def multiply(num1, num2):
    return str(num1 * num2)

@app.route("/div/<int:num1>/<int:num2>")
def div(num1, num2):
    if num1 == 0 or num2 == 0 :
        return "error"
    return str(num1 / num2)