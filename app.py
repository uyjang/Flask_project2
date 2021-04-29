import os
from flask import Flask
from flask import request  # register함수안에 어떤 요청이 들어왔는 지 확인하기 위해서 리퀘스트가 필요
from flask import redirect
from flask import render_template  # 템플릿으로 어떠한 기능을 보낼때 사용
from flask_sqlalchemy import SQLAlchemy
from models import db
from models import Fcuser  # 모델은 클래스만 생성할 수 있음
from flask_wtf.csrf import CSRFProtect  # 사기 위조요청 방지
from forms import RegisterForm, LoginForm
from flask import session  # 세션 사용

app = Flask(__name__)  # name은 모델명이 들어갈 자리

# register.html과 연결 및 그 안에 기능을 추가
# 기본적으로 라우트는 요청에대해서 GET밖에 안돼있음 / 홈페이지만 부르면 get요청 , 등록버튼을 누르면 post요청 처리를 함


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)  # 팝을 쓰게 되면 그 안의 아이디를 꺼내서 삭제를 시킴
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')
        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():  # 포스트요청까지 받고 데이터들이 유효성검사가 됐는 지 한꺼번에 진행
        # if request.method == 'POST':
        #     리퀘스트 안에 폼이라는 변수가 있고 그 폼안에서 하나씩 꺼낸다
        #     userid = request.form.get('userid')
        #     username = request.form.get('username')
        #     password = request.form.get('password')
        #     re_password = request.form.get('re-password')
        fcuser = Fcuser()  # Fcuser()클래스를 일단 비워두고 아래의 데이터를 삽입
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser)  # db안에 위에서 넣은 데이터들을 넣겠다.
        db.session.commit()  # 커밋까지 해야 완료
        print('Success!')

        return redirect('/')

    return render_template('register.html', form=form)


# hello.html과 연결하고 그 안에 기능들을 추가
@app.route('/')  # 괄호안에 경로를 넣으면 그 홈페이지(url?)로 이동하고 밑에 있는 코드나 함수를 실행
def hello():
    userid = session.get('userid', None)
    # hello.html 형식으로 홈페이지를 만들고 이 함수를 html파일에 보낸다
    return render_template('hello.html', userid=userid)


# name라는 기본 글로벌 변수 안에 main을 집어넣어서 인터프리터에서 아래의 코드를 바로 실행하게 한다. 임포트해서 실행하는 것이 아니라...
if __name__ == "__main__":
    # 현재 있는 파일에 절대경로의 디렉토리가 나오게 됨
    basedir = os.path.abspath(os.path.dirname(__file__))
    # sql데이터베이스를 연동하기위해 위에 지정한 변수basedir을 가져온다.
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        dbfile  # sqlalchemy에 필요한 설정값 넣어주기, uri를 통해 주소를 표시하는 것
    # 티어다운은 사용자가 요청을 했을 때 원하는 정보를 줬을 때이고 그게 끝나면 커밋을 한다. 커밋이라는 동작을해서 쌓여진 동작을 데이터베이스에 작동하고 저장됨. 즉 실제 반영하는 느낌
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # 수정사항에대한 트랙을 하겠다라는 뜻인데 구버전에서 만든파일을 신버전으로 돌릴때 오류가 생길 시 트루로 바꾸면 됨
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECREY_KEY'] = 'kalfeinfqlkenf'

    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)  # 위의 세가지 설정값 외에도 상당히 많은 설정값들이 있는데 그 값들을 초기화 해주는 코드
    # 모델에서는 앱을 import하고 앱에서는 models를 import하면 서로순환구조가 되면서 에러가 뜨기때문에 여기에 앱을 넣는 과정(코드) 삽입
    db.app = app
    db.create_all()  # 모델 클래스가 먼저 만들어져있고 그것을 생성한다는 것이니 모델클래스 작성이 완료되면 크리에이트를 진행함
    app.run(host='127.0.0.1', port=5000, debug=True)
    # 이렇게해서 모델을 분리했고 그 모델을 컨트롤러(app.py)에서 설정할 수 있도록 했다.
