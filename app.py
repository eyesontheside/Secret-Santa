from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hard to guess string'
bootstrap = Bootstrap(app)

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
