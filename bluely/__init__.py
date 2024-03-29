# 构造文件

import os
import click
from flask import Flask 
from flask import render_template
from bluelog.settings import config
from bluelog.extensions import bootstrap, db, moment, ckeditor, mail
from blueprints import admin,auth,blog

def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_extensions(app)
    register_logging(app)
    register_shell_context(app)
    register_template_context(app)

    return app



def register_logging(app): #注册日志处理器
    pass

def register_extensions(app):#注册扩展（扩展初始化）
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(mail)
    moment.init_app(moment)

def register_blueprints(app):#注册蓝本
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp,url_prefix='/auth')

def register_shell_context(app):#注册shell上下文处理函数
    @app.register_shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_template_context(app):#注册模版上下文处理函数
    pass

def register_errors(app):#注册错误处理函数

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'),400
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.thml'),404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):#注册自定义shell命令
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
