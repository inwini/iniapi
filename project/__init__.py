
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    csrf.init_app(app)
    
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_static_assets
       
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
   
        db.create_all()

        if app.config['FLASK_ENV'] == 'development':
            compile_static_assets(app)

        return app
