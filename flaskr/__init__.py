# создаем объект класса Flask с определенными параметрами и возвращаем его

import os
from . import db, auth, blog, personalPage
from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # secret key for accessing
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),  # way to database
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)  # setting default configuration
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)  # setting some more config

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)  # рагистрируем шаблоны
    app.register_blueprint(blog.bp)
    app.register_blueprint(personalPage.pg)
    app.add_url_rule('/', endpoint='index')  # ассоциирует первый объект со вторым

    return app
