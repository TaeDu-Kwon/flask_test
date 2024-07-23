from flask import Flask,request, redirect, url_for
import pymysql
import random
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

def get_db_all_value():
    sql = "select * from new_table"
    cursor.execute(sql)
    db_all_value = cursor.fetchall()

    return db_all_value

def count_rows():    
    # SQL COUNT 명령문
    sql = "SELECT COUNT(*) FROM new_table"
    
    cursor.execute(sql)
    result = cursor.fetchone()
    row_count = result[0]
    return row_count
    

def template(contents, content):
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href = "/"> WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">Create</a></li>
            </ul>
        </body>
    </html>
    '''

def getContents():

    db_all_value = get_db_all_value()
    litags = ""

    for value in db_all_value:
        litags = litags + f'<li><a href="/read/{value[0]}">{value[1]}</a></li>'

    # for topic in topics:
    #     litags = litags + f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    
    return litags

@app.route("/")
def index():
    return template(getContents(),'<h2>Welcom</h2>Hello WEB')

@app.route("/read/<int:id>/")
def read(id):
    title = ''
    body = ''

    db_all_value = get_db_all_value()

    for value in db_all_value:
        if id == value[0]:
            title = value[1]
            body = value[2]

    return template(getContents(),f'<h2>{title}</h2>{body}')

@app.route("/random")
def random_page():
    return str(random.random())

@app.route("/create/",methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # 폼에서 데이터 가져오기
        title = request.form["title"]
        body = request.form["body"]

        get_table_count = count_rows()

        # SQL 삽입 명령문
        sql = "INSERT INTO new_table (id, name, value, value2) VALUES (%s,%s, %s,%s)"
        data = (get_table_count,title, body,"")
        
        try:
            # 데이터 삽입
            cursor.execute(sql, data)
            # 변경사항을 커밋
            DB.commit()
            return redirect(url_for("create_success"))
        except Exception as e:
            # 에러 발생 시 롤백
            DB.rollback()
            return f"Failed to insert data into database. Error: {e}"
        finally:
            # 커서와 연결 종료
            cursor.close()
            DB.close()
    content = '''
        <form action="/create/" method="POST">
            <p><input type="text" name = "title" placeholder="title"></p>
            <p><textarea name = "body" placeholder="body"></textarea></p>
            <p><input type = "submit" value="create"></p>
        </form>
    '''
    
    return template(getContents(),content)
    
@app.route("/create/success")
def create_success():
    return "Data inserted successfully!"

app.run(debug=True)