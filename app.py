from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True    )
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Email %r>' % self.email

class SecretSantaForm(Form):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'

@app.route('/home')
def home():
    return '<h1>Welcome Back!</h1>'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = SecretSantaForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))

    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
