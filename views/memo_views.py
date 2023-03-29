from flask import Flask, render_template, jsonify, request, Blueprint, url_for
from werkzeug.utils import redirect
import requests

from bson import ObjectId
from bs4 import BeautifulSoup

from pymongo import MongoClient

bp = Blueprint('memo', __name__, url_prefix='/memo')

client = MongoClient('localhost', 27017)
db = client.dbjungle

## HTML을 주는 부분
@bp.route('/')
def root():
   return render_template('views/memo_views.html')
   

@bp.route('/html', methods=['GET'])
def read_articles():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.articles.find({}))
    for article in result:
        ids = str(article["_id"])
        article["_id"] = ids

    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'articles':result})

## API 역할을 하는 부분
@bp.route('/html', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    # 2. meta tag를 스크래핑하기
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_title = og_title['content']
    url_description = og_description['content']
    url_image = og_image['content']

    article = {'url': url_receive, 'title': url_title, 'desc': url_description, 'image': url_image,
               'comment': comment_receive}

    # 3. mongoDB에 데이터를 넣기
    db.articles.insert_one(article)

    return jsonify({'result': 'success'})

@bp.route('/delete', methods=['POST'])
def delete_article():
    id_receive = ObjectId(request.form['give_id'])
    db.articles.delete_one({'_id':id_receive})
    return jsonify({'result': 'success'})


@bp.route('/modify', methods=['POST'])
def modify_article():

    receive_id = ObjectId(request.form['give_id'])
    receive_comment = request.form['give_comment']
    print(receive_comment)
    db.articles.update_one({'_id':receive_id}, {"$set": {'comment':receive_comment}})
    
    return jsonify({'result': 'success'})