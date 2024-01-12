from flask import Flask
from cs50 import SQL
import os

lib_stores_db = SQL("sqlite:///lib_stores.db")

def create_app():
    
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = "ADSFJ kjsd fadfasdfkJ FKAJSDFLKAJSFQ209843IU23J !@#$@#%kqewfdcx2POIEWUJ"
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024
    
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static/imgs/tmp_profile')
    
    # initialize upload folder
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # register the routes created in routes.py
    from .routes import all_routes
    
    app.register_blueprint(all_routes)

    return app