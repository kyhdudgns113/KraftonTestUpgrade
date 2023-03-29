from flask import Flask
from pymongo import MongoClient

import config

client = MongoClient('localhost', 27017)
db = client.dbjungle

def create_app():
   app = Flask(__name__)

   app.config.from_object(config)

   from views import root_views, memo_views, movie_views, memo2_views, auth_views
   
   app.register_blueprint(root_views.bp)
   app.register_blueprint(memo_views.bp)
   app.register_blueprint(movie_views.bp)
   app.register_blueprint(memo2_views.bp)
   app.register_blueprint(auth_views.bp)

   return app

if __name__ == '__main__':
   app = create_app()
   app.run('0.0.0.0',port=5000,debug=True)