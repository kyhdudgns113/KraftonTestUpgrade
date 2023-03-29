from flask import Flask, render_template, jsonify, request, Blueprint
from pymongo import MongoClient

import requests
from bs4 import BeautifulSoup
from bson import ObjectId

bp = Blueprint('memo2', __name__, url_prefix='/memo2')

client = MongoClient('localhost', 27017)
db = client.dbjungle


## HTML을 주는 부분
@bp.route('/')
def root():
   return render_template('views/memo2_views.html')


@bp.route('/memo', methods=['GET'])
def read_articles():
    result = list(db.memos.find({}).sort('like', -1))

    #   bson.ObjectID 형태의 id 를 string 형태로 바꾸어준다.
    #   바꾸지 않으면 json 화 시키지 못한다.
    for memo in result:
        ids = str(memo["_id"])
        memo["_id"] = ids
        
    return jsonify({'result':'success', 'articles':result})

@bp.route('/memo', methods=['POST'])
def post_article():
    receive_title = request.form['give_title']
    receive_comment = request.form['give_comment']
    default_like = 0

    article = {'title':receive_title, 'comment':receive_comment, 'like':default_like}

    new_obj = db.memos.insert_one(article)
    id = str(new_obj.inserted_id)

    return jsonify({'result': 'success', 'id':id})

@bp.route('/memo/delete', methods=['POST'])
def delete_article():
    receive_id = ObjectId(request.form['give_id'])
    db.memos.delete_one({'_id':receive_id})

    return jsonify({'result': 'success'})


@bp.route('/memo/modify', methods=['POST'])
def modify_article():

    receive_id = ObjectId(request.form['give_id'])
    receive_title = request.form['give_title']
    receive_comment = request.form['give_comment']

    db.memos.update_one({'_id':receive_id}, {"$set": {'title':receive_title, 'comment':receive_comment}})
    
    return jsonify({'result': 'success'})


@bp.route('/memo/like', methods=['POST'])
def like_article():
    receive_id = ObjectId(request.form['give_id'])
    new_like = db.memos.find_one({'_id':receive_id})['like'] + 1

    db.memos.update_one({'_id':receive_id}, {"$set": {'like':new_like}})
    
    return jsonify({'result': 'success'})
