from flask import Flask, render_template,request
from livereload import Server
from markdown import markdown
from functools import reduce
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html', title='<h1>Hello world</h1>',
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


@app.context_processor
def inject_methods():
    return dict(read_md=read_md)

@app.template_test('current_link')
def is_current_link(link):
    return link == request.path


if __name__ == '__main__':
    # 监测文件变动并更新页面
    live_server = Server(app.wsgi_app)
    live_server.watch("**/*.*")
    live_server.serve(open_url=True)
    #app.run()
