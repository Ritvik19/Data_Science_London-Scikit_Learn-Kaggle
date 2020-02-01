from flask import Flask
from flask import request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = '79e9d3b5d183b6e620e3776f77d95f4b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

class Clip(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    clip = db.Column(db.Text, nullable=False)
    private = db.Column(db.Boolean, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f''


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/clip', methods=['GET', 'POST'])
def clip():
    if request.form:
        print(request.form)
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
    return render_template('clip.html')

if __name__ == '__main__':
    app.run(debug=True)
