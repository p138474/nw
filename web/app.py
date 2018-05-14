from flask import Flask, render_template, request, g
import hashlib
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)

def get_db():
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
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def hello():
    return render_template("login.html")

@app.route("/name")
def name():
    return "yerin"

@app.route("/login", methods=['POST'])
def login():
    id = request.form['id']
    pw = request.form['pw']
    # if id in users:
    #     if users[id] == hashlib.sha1(pw).hexdigest():
    #         return "login OK"
    #     else:
    #         return "login FAIL"
    # else:
    #     return "login FAIL"

@app.route("/join", methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        id = request.form['id']
        pw = hashlib.sha1(request.form['pw'].strip()).hexdigest()
        sql = "insert into user(id, password) values('%s', '%s')" % (id, pw)
        query_db(sql, modify=True)
        # if id not in users:
        #    users[id] = hashlib.sha1(pw).hexdigest()
        # else:
        #    return "duplicate!!!!"        
        return "join OK"
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