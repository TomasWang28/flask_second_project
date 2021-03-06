from flask import Flask,render_template,request,url_for,make_response,abort,redirect
from werkzeug.routing import  BaseConverter
from werkzeug.utils import secure_filename
from flask_script import Manager
from os import path


class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex=items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

manager = Manager(app)

@app.route('/')
def index():
    response = make_response(render_template('index.html', title='welcome'))
    response.set_cookie('username','')
    return response

@app.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'User %s' % user_id

@app.route('login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
    else:
        username=request.args['username']
    return render_template('login.html', method=request.method)

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f = request.files['file']
        basepath=path.abspath(path.dirname(__file__))
        upload_path=path.join(basepath,'static','upload')
        f.save(upload_path+'/'+secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@manager.command()
def dev():
    from livereload import Server
    live_server=Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()