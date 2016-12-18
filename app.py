from flask import Flask, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from forms import SecretSantaLogin, SecretSantaRegister
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secretsantas.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Santa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Email %r>' % self.email


@app.route('/')
def hello_world():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return '<h1>Welcome Back!</h1>'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = SecretSantaLogin()
    if form.validate_on_submit():
        q = Santa.query.filter_by(email=form.email.data).first()
        if q is None:
            flash('This email is not registered!')
            return render_template('login.html', form=form)
        elif form.password.data != q.password:
            flash('Incorrect password!')
            return render_template('login.html', form=form)
        else:
            return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = SecretSantaRegister()
    if form.validate_on_submit():
        new_user = Santa(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('You have been registered!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
