import flask
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('start.html')

@app.route('/world')
def world():
    return render_template('world.html')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')