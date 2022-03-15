from flask import Flask
from flask import url_for  # создает скомпонованный URL, такой, какой нам показывает браущер после обновления
from flask import request
from flask import render_template
from markupsafe import escape  # для вставки данных из URL
app = Flask(__name__)


# @app.route('/user/<name>/')
# def show_users_profile(name):
#    return f'User name is: {escape(name)}'


# @app.route('/post/<int:post_id>/')
# def show_post(post_id):
#    return f'Post {post_id}'


@app.route('/')
def index():
    print(url_for('index'))
    return 'index'


# @app.route('/login')
# def login():
#     print(url_for('login'))
#     return 'login'


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == "hehe" and request.form.get('password') == "hehe":
            # лучше использовать request.args.get(NAME) - это безопаснее
            # метод пост получает данные из html шаблона и уже оперирует с ними как с фомами
            # запросе GET же наоборот получаются сразу из строки URL браузера
            return "HEHE"
        else:
            error = 'Invalid username/password'
            return render_template('')
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return '''
           <form method="POST">
               <div><label>Login: <input type="text" name="username"></label></div>
               <div><label>Password: <input type="text" name="password"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/photo', methods=['POST', 'GET'])
def photo():
    if request.method == 'POST':
        file = open('photo/{}'.format(request.form.get('photo')), 'r').read()
        return file
    return '''
           <form method="POST">
               <div><label>Name of the photo: <input type="text" name="photo"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/user/<username>')
def profile(username):
    print(url_for('profile', username=username))
    return render_template('', name=username)  # рендер шаблона HTML


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)  # запуск основного приложения
