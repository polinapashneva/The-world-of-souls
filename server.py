import flask
import requests
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user

from data import db_session
from data.loginform import LoginForm
from data.registerform import RegisterForm
from data.users import User

from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    session = db_session.create_session()
    for user in session.query(User).all():
        print(user)
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template('start.html', names=names)


@app.route('/world')
def world():
    return render_template('world.html')


@app.route('/edem')
def edem():
    return render_template('edem.html')


@app.route('/earth')
def earth():
    m = ['30.314997,59.938784,vkbkm', '111.095329,70.983309,vkbkm', '144.158095,63.988118,vkbkm',
         '-70.203879,-6.370066,vkbkm', '-122.235129,73.023610,vkbkm', '123.858621,-27.540349,vkbkm']
    map_request = (f"https://static-maps.yandex.ru/1.x/?ll=90.0,90.0&z=0&size=600,450&bbox=0.0,83.0~82.0,0.0&pt={'~'.join(m)}&l=map")
    response = requests.get(map_request)
    map_file = "static/img/map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)
    mpf = Image.open("static/img/map.jpg")
    mp = mpf.crop((0, 100, 525, 450))
    mp.save("static/img/map.png")
    return render_template('earth.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()