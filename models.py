from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # 여러 변수나 클래스를 쓰게 되는데 그때 필요한 최상위 변수
# db라는 변수를 통해서 db에 값도 넣고 모델도 만들고 다 사용함


class Fcuser(db.Model):  # 클래스 Test를 db.Model로 지정함으로써 이 클래스를 이용해 데이터베이스를 관리한다
    __tablename__ = 'fcuser'  # 내부에 데이터가 들어갈때 사용할 테이블의 테이블명
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))
