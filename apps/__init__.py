from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from os import *
from .views import init_views

basedir = path.abspath(path.dirname(__file__))
bootstrap = Bootstrap()
nav = Nav()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + path.join(basedir, 'sqlitedb/data.sqlite')
    #留疑点这点不明白
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    nav.register_element('top', Navbar(u'devops运维平台',
                                       View(u'主页', 'index'),
                                       View(u'关于', 'webs'),
                                       View(u'服务', 'server'),
                                       View(u'项目', 'devops'),
                                       ))
    nav.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    init_views(app)
    return app
