# Flask 웹 애플리케이션을 만들기 위해 필요한 모듈을 가져옵니다.
from flask import Flask, request, redirect
import random

# Flask 애플리케이션을 생성합니다.
app = Flask(__name__)

# 다음 글의 고유 식별자를 나타내는 변수를 초기화합니다.
nextId = 4

# 미리 작성된 글 목록을 나타내는 리스트를 초기화합니다.
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'}
]

# HTML 템플릿을 생성하는 함수를 정의합니다.
def template(contents, content, id=None):
    contextUI = ''
    if id is not None:
        # 글을 수정하거나 삭제할 수 있는 링크를 추가합니다.
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

# 글 목록을 생성하는 함수를 정의합니다.
def getContents():
    liTags = ''
    for topic in topics:
        # 각 글에 대한 링크를 추가합니다.
        liTags = liTags + f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    return liTags


# 홈 페이지를 나타내는 라우터를 설정합니다.
@app.route('/')
def index():
    # 템플릿을 사용하여 홈 페이지를 반환합니다.
    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')

# 특정 글을 읽는 라우터를 설정합니다.
@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        # 주어진 id에 해당하는 글을 찾아서 템플릿을 사용하여 반환합니다.
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)

# 새 글을 생성하는 라우터를 설정합니다.
@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        # GET 요청일 때는 글 작성 폼을 제공합니다.
        content = '''
            <form action="/create/" method="POST"> 
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea> </p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        # POST 요청일 때는 새로운 글을 생성하고 해당 페이지로 리다이렉트합니다.
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/' + str(nextId) + '/'
        nextId = nextId + 1
        return redirect(url)

# 글을 수정하는 라우터를 설정합니다.
@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        # GET 요청일 때는 글 수정 폼을 제공합니다.
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST"> 
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body">{body}</textarea> </p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        # POST 요청일 때는 글을 업데이트하고 해당 페이지로 리다이렉트합니다.
        global nextId
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/' + str(id) + '/'
        return redirect(url)

# 글을 삭제하는 라우터를 설정합니다.
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        # 주어진 id에 해당하는 글을 찾아서 삭제하고 홈 화면으로 리다이렉트합니다.
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

# Flask 애플리케이션을 실행합니다.
app.run(debug=True)
