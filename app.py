import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URI = os.environ.get("mongodb+srv://Syahrial:syahrial15@cluster0.xp8a6wl.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get('dbsparta')

client = MongoClient('mongodb+srv://Syahrial:syahrial15@cluster0.xp8a6wl.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=["GET"])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({},{'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form['sample_give']
    # print(sample_receive)
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    today = datetime.now()
    
    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    mytime = today.strftime('%Y-%m-%d %H.%M.%S')
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)

    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    doc = {
        'time': mytime,
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'POST request complete!!!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)