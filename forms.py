from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo
from models import Fcuser


class RegisterForm(FlaskForm):
    # 밸리데이터즈를 통해 데이터 검증
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[
                           DataRequired(), EqualTo('repassword')])  # 이퀄투 안에 리패스워드를 넣어서 이게 패스워드랑 같은 지 판별해주는 기능
    repassword = StringField('repassword', validators=[DataRequired()])


class LoginForm(FlaskForm):
    # 밸리데이터즈를 통해 데이터 검증
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message

        def __call__(self, form, field):
            userid = form['userid'].data  
            password = field.data  # 현재 필드에서 입력한 것
            fcuser = Fcuser.query.filter_by(
                userid=userid).first()  # 유저아이디 여러값을 찾을 건데 그중에 첫번째 값
            if fcuser.password != password:
                raise ValueError('Wrong Password!')

    userid = StringField('userid', validators=[DataRequired()])
    password = StringField('password', validators=[
                           DataRequired(), UserPassword()])
