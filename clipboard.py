from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from forms import *

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '79e9d3b5d183b6e620e3776f77d95f4b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

@app.route('/', methods=['GET', 'POST'])
def home():
    form = ViewForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        key = form.key.data
    return render_template('home.html', form=form)

@app.route('/clip')
def clip():
    form = ClipForm()
    
    return render_template('clip.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
