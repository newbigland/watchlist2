from flask import Flask, url_for, render_template

app = Flask(__name__)  # 实参为什么是__name__


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


my_name = "cxw"
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


@app.route("/")
def index():
    # 左边的关键字参数my_name,movies是模板文件index.html中使用的变量名，右边的my_name，movies是变量指向的实际对象
    # render_template返回渲染好的模板内容
    return render_template('index.html', my_name=my_name, movies=movies)
