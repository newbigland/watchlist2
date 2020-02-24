from flask import Flask, url_for

app = Flask(__name__)  # 实参为什么是__name__


@app.route('/')
@app.route('/home')
@app.route('/index')
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



