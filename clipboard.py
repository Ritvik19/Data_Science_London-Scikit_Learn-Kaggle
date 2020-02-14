from flask import Flask
from flask import request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import hashlib

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '79e9d3b5d183b6e620e3776f77d95f4b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
admin = Admin(app)

class Clip(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    clip = db.Column(db.Text, nullable=False)
    private = db.Column(db.Boolean, nullable=False, default=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.DateTime, nullable=False)
    password = db.Column(db.String(50), nullable=False, default='')
    key = db.Column(db.String(32), nullable=False)

admin.add_view(ModelView(Clip, db.session))
encrypt_md5 = lambda x: hashlib.md5(str(x).encode()).hexdigest()

def delete_clips():
    for clip in Clip.query.filter(Clip.duration < datetime.today()-timedelta(days=1)).all():
        db.session.delete(clip)
    db.session.commit()

sched = BackgroundScheduler(daemon=True)
sched.add_job(delete_clips, 'interval', hours=24)
sched.start()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.form:
        print('query')
        print(request.form)
        existing_clip = Clip.query.filter_by(key=request.form.get("key")).first()
        if encrypt_md5(request.form.get('password')) == existing_clip.password:    
            data = {
                'title': existing_clip.title, 'clip': existing_clip.clip, 'duration': existing_clip.duration.strftime("%b %d, %Y"),
                'password': ''
            }
            return render_template('clip.html', key=request.form.get("key"), data=data)
        else:
            print(encrypt_md5(request.form.get('password')))
            print(existing_clip.password)
            print('Password Error')
    pnum = request.args.get('page', 1, int)
    return render_template('home.html', clips=Clip.query.filter_by(private=False).order_by(Clip.uid.desc()).paginate(pnum, 5))


@app.route('/clip', methods=['GET', 'POST'])
def clip():
    if request.form:
        print(request.form)
        if request.form.get('submit') == 'Done':
            if len(Clip.query.filter_by(key=request.form.get("key")).all()) == 0:
                new_clip = Clip(title=request.form.get("title"), clip=request.form.get("clip").strip(), 
                            duration=datetime.strptime(request.form.get("duration"), "%b %d, %Y")
                            , password=encrypt_md5(request.form.get("password")), 
                            private=bool(request.form.get("private", False)),
                            key=request.form.get("key"))
                db.session.add(new_clip)
            else:
                existing_clip = Clip.query.filter_by(key=request.form.get("key")).first()
                existing_clip.itle=request.form.get("title")
                existing_clip.clip=request.form.get("clip").strip()
                existing_clip.duration=datetime.strptime(request.form.get("duration"), "%b %d, %Y")
                existing_clip.password = encrypt_md5(request.form.get("password"))
                existing_clip.private=bool(request.form.get("private", False))
            db.session.commit()
        if request.form.get('submit') == 'Delete':
            existing_clip = Clip.query.filter_by(key=request.form.get("key")).first()
            db.session.delete(existing_clip)
            db.session.commit()
        return redirect(url_for('home'))
    query = request.args.get('key', None)
    if query:
        existing_clip = Clip.query.filter_by(key=query).first()
        data = {
            'title': existing_clip.title, 'clip': existing_clip.clip, 'duration': existing_clip.duration.strftime("%b %d, %Y"),
            'password': existing_clip.password
        }
        return render_template('clip.html', key=query, data=data)
    else:
        try:
            key = Clip.query.order_by(Clip.uid.desc()).first().uid + 1
        except Exception as e:
            print(e)
            key = 1
        key = encrypt_md5(key)
        return render_template('clip.html', key=key)

if __name__ == '__main__':
    app.run(debug=True)
