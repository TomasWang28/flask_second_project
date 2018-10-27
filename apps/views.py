from flask import Flask, render_template,request
from markdown import markdown
from functools import reduce
from apps.form import LoginForm
from flask_script import Manager

def init_views(app):
    @app.route('/login',methods=['GET','POST'])
    def login():
        form = LoginForm()
        #flash(u'登录成功')
        return render_template('login.html', title="登录", form=form)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    # @app.errorhandler(500)
    # def internal_server_error(e):
    #     return render_template('500.html'), 500

    @app.route('/')
    def index():
        return render_template('index.html', title='Welcome',
                               body='## tomas')


    @app.route('/webs')
    def webs():
        return 'Webs'


    @app.route('/server')
    def server():
        return 'Server'


    @app.route('/devops')
    def devops():
        return 'Devops'



    # 向模板中注册md的方法
    @app.template_filter('md')
    def markdown_to_html(txt):
        return markdown(txt)


    # 读取markdown文件的方法
    def read_md(filename):
        with open(filename, 'r', encoding='UTF-8') as md_file:
            content = reduce(lambda x, y: x + y, md_file.readlines())
            return content

    #内容处理函数
    @app.context_processor
    def inject_methods():
        return dict(read_md=read_md)

    #向模板里注册函数
    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

