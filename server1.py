from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host='localhost',
    user='korea',
    password='1234',
    database='test'
)

# MySQL 커서 생성
cursor = db.cursor()

# 홈 페이지 라우터
@app.route('/')
def index():
    # MySQL에서 회원 목록을 가져옴
    cursor.execute("SELECT * FROM member_flask")
    members = cursor.fetchall()

    return '''
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Member List</title>
            </head>
            <body>
                <h1>Member List</h1>
                <ul>
                    {% for member in members %}
                        <li>
                            <a href="/read/{{ member[0] }}/">
                                {{ member[1] }} ({{ member[2] }})
                            </a>
                        </li>
                    {% endfor %}
                </ul>
                <a href="/create/">Create Member</a>
            </body>
            </html>
    '''

# 회원가입 라우터
@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return '''
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Create Member</title>
            </head>
            <body>
                <h1>Create Member</h1>
                <form action="/create/" method="POST">
                    <p>Email: <input type="text" name="email"></p>
                    <p>Password: <input type="password" name="pw"></p>
                    <p>Name: <input type="text" name="name"></p>
                    <p><input type="submit" value="Create"></p>
                </form>
            </body>
            </html>
        '''
    elif request.method == 'POST':
        member_email = request.form['email']
        member_pw = request.form['pw']
        member_name = request.form['name']

        if not member_email or not member_pw or not member_name:
            return f'Missing required information'

        # MySQL에 회원 정보 삽입
        sql = "INSERT INTO member_flask (member_name, member_email, member_pw) VALUES (%s, %s, %s)"
        cursor.execute(sql, (member_name, member_email, member_pw))
        db.commit()

        return redirect('/')

# 글 읽기 라우터
@app.route('/read/<int:id>/')
def read(id):
    # MySQL에서 특정 회원 정보를 가져옴
    cursor.execute("SELECT * FROM member_flask WHERE id = %s", (id,))
    member = cursor.fetchone()

    return '''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Read Member</title>
        </head>
        <body>
            <h1>Read Member</h1>
            <p>ID: {0}</p>
            <p>Name: {1}</p>
            <p>Email: {2}</p>
            <p>Password: {3}</p>
            <a href="/">Back to Home</a>
        </body>
        </html>
    '''.format(member[0], member[1], member[2], member[3])

# 글 수정 라우터
@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        # MySQL에서 특정 회원 정보를 가져옴
        cursor.execute("SELECT * FROM member_flask WHERE id = %s", (id,))
        member = cursor.fetchone()
        return '''
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Update Member</title>
            </head>
            <body>
                <h1>Update Member</h1>
                <form action="/update/{0}/" method="POST">
                    <p>Email: <input type="text" name="email" value="{1}"></p>
                    <p>Password: <input type="password" name="pw" value="{2}"></p>
                    <p>Name: <input type="text" name="name" value="{3}"></p>
                    <p><input type="submit" value="Update"></p>
                </form>
                <a href="/">Back to Home</a>
            </body>
            </html>
        '''.format(id, member[2], member[3], member[1])
    elif request.method == 'POST':
        member_email = request.form['email']
        member_pw = request.form['pw']
        member_name = request.form['name']

        if not member_email or not member_pw or not member_name:
            return f'Missing required information'

        # MySQL에서 회원 정보 업데이트
        sql = "UPDATE member_flask SET member_name = %s, member_email = %s, member_pw = %s WHERE id = %s"
        cursor.execute(sql, (member_name, member_email, member_pw, id))
        db.commit()

        return redirect('/read/{}'.format(id))

# 글 삭제 라우터
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    # MySQL에서 특정 회원 정보 삭제
    cursor.execute("DELETE FROM member_flask WHERE id = %s", (id,))
    db.commit()

    return redirect('/')

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
