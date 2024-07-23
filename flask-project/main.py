from flask import Flask, request, redirect, url_for, render_template
import pymysql
app = Flask(__name__)

CONNECT = {
    "Host" : "127.0.0.1",
    "Port" : 3306,
    "User" : "root",
    "Password" : "eoneoneon",
    "DB_Name" : "test_db" 
}

DB= pymysql.connect(host = CONNECT["Host"], port = CONNECT["Port"], user=CONNECT["User"], password=CONNECT["Password"], db=CONNECT["DB_Name"], charset='utf8')
cursor = DB.cursor()

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login/')
def login():
    return render_template("login.html")

app.run(debug=True)