from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request, Blueprint

bp = Blueprint('movie', __name__, url_prefix='/movie')

client = MongoClient('localhost', 27017)
db = client.dbjungle


# HTML 화면 보여주기 
@bp.route('/')
def root():
    return render_template('views/movie_views.html')


# API 역할을 하는 부분
@bp.route('/api/list', methods=['GET'])
def start_list():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!
    mystars = list(db.mystar.find({}, {'_id':False}).sort('like', -1))
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'stars_list':mystars})


@bp.route('/api/like', methods=['POST'])
def like_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    star = db.mystar.find_one({'name':name_receive})
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = star['like']+1
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!
    db.mystar.update_one({'name':name_receive},{'$set':{'like':new_like}})
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


@bp.route('/api/delete', methods=['POST'])
def delete_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.mystar.delete_one({'name':name_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': 'delete 연결되었습니다!'})

