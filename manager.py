from flask_script import Manager
from livereload import Server
from apps import create_app,db
from flask_migrate import Migrate,MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


# 监测文件变动并更新页面
@manager.command
def dev():
    live_server=Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)

@manager.command
def test():
    pass


@manager.command
def deploy():
    from apps.models import Role
    #upgrade()
    Role.seed()


if __name__ == '__main__':
    manager.run()

#app.run()