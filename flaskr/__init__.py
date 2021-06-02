from flask import Flask
from flaskr.models import db_setup, User, Job, JobStatus
from flask_cors import CORS
from flask_login import LoginManager


# app = Flask(__name__)
#
# app = Flask(__name__)
# moment = Moment(app)
# db = db_setup(app)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, template_folder='templates')
    db_setup(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # CORS
    CORS(app, resources={'/': {'origins': '*'}})

    # after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    return app

# @app.route('/register')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
