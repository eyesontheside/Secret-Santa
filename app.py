from flask import Flask, render_template, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from forms import SecretSantaLogin, SecretSantaRegister
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secretsantas.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class Santa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, authenticated):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.authenticated = authenticated

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<Email %r>' % self.email

@login_manager.user_loader
def user_loader(user_id):
    return Santa.query.filter_by(email=user_id).first()

@app.route('/')
def hello_world():
    return redirect(url_for('login'))

@app.route('/home')
@login_required
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
            login_user(q, remember=True)
            return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('login'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = SecretSantaRegister()
    if form.validate_on_submit():
        new_user = Santa(form.first_name.data, form.last_name.data, form.email.data, form.password.data, False)
        db.session.add(new_user)
        db.session.commit()
        flash('You have been registered!')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
