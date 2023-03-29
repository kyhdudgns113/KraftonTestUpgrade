from flask import Blueprint, render_template, request, url_for, jsonify, redirect
from views.auth_views import login_required

bp = Blueprint('root', __name__)

@bp.route('/')
def root():
    return render_template('views/root_views.html', data_list = [
        ['memo', '나홀로 링크 메모장'], 
        ['movie', '마이 페이보릿 무비스타'],
        ['memo2', '나홀로 작성 메모장']
        ])
    

@bp.route('/goto', methods=('GET', 'POST'))
@login_required
def goto():
    where = request.args['where']

    if request.method == 'POST':
        if where == 'memo':
            return redirect(url_for('memo.root'))
        elif where == 'movie':
            return redirect(url_for('movie.root'))
        elif where == 'memo2':
            return redirect(url_for('memo2.root'))
        else:
            return '그런 페이지는 없습니다.'
    else:
        return render_template('views/root_views.html')