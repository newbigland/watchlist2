import os
import sys
import click

from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'  # windows系统
else:
    prefix = 'sqlite:////'  # macOS,Linux系统

# 实例化一个flask对象app
app = Flask(__name__)  # 实参为什么是__name__
# 给app对象添加配置
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 实例化一个ORM对象，用于操作数据库,参数是配置过的app
db = SQLAlchemy(app)


@app.route('/default')
@app.route('/home')
def hello():
    return "<h1>Hello Totoro!</h1><img src='http://helloflask.com/totoro.gif'>"


@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name


@app.route("/test")
def test_url_for():
    print(url_for('hello'))  # /index，生成的url是和函数最近的装饰器url规则字符串
    print(url_for("user_page", name="chen"))  # /user/chen, url规则有变量，要传参数值给变量
    print(url_for("user_page", name="xxww", city="bj"))  # /user/xxww?city=bj, 多余的参数city作为查询字符串附加在url后面

    return "test"  # 视图函数需要返回字符串给浏览器，否则报错


# name = "cxw"
# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'A Perfect World', 'year': '1993'},
#     {'title': 'Leon', 'year': '1994'},
#     {'title': 'Mahjong', 'year': '1996'},
#     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     {'title': 'King of Comedy', 'year': '1999'},
#     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     {'title': 'WALL-E', 'year': '2008'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]


@app.route("/")
def index():
    user = User.query.first()
    movies = Movie.query.all()
    # 左边的关键字参数my_name,movies是模板文件index.html中使用的变量名，右边的my_name，movies是变量指向的实际对象
    # render_template返回渲染好的模板内容
    return render_template('index.html', user=user, movies=movies)


# 定义一个模型类表示数据库中的一张表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.cli.command()  # 把函数名initdb注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """ initialize the database """
    if drop:  # 如果输入了选项
        db.drop_all()
    db.create_all()
    click.echo("initialized database.")  # 输出提示信息


@app.cli.command()
def forge():
    """ generate fake data. """
    db.create_all()

    name = "cxw"
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo("Done.")
