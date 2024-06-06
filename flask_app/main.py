from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from models import Users, Posts, db
import analiz
import datetime
import os, shutil

path = "D://Универ//прога//pythonProject1//flask_app//static"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '$228$'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    else:
        return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Неправильный логин или пароль')
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['password']
        if not (password == repeat_password):
            flash('Пароли не совпадают')
        else:
            user = Users.query.filter_by(username=username).first()
            if user:
                flash('Пользователь с таким именем уже зарегистрирован')
            else:
                os.mkdir(f"{path}\\{username}")
                hashed_password = generate_password_hash(password)
                new_user = Users(username=username, password=hashed_password)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Пользователь успешно зарегистрирован')
                except:
                    return "Ошибка"
                return redirect(url_for('login'))
    return render_template('register.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'xlsx'


@app.route("/create", methods=['POST', 'GET'])
def create():
    if current_user.is_authenticated:
        if request.method == 'POST':
            if 'file' not in request.files:
                return render_template('create.html')
            UPLOAD_FOLDER = path + "//" + current_user.username
            file = request.files['file']
            if file.filename == '':
                return render_template('create.html')
            if file and allowed_file(file.filename):
                title = request.form['title'].strip()
                content = request.form['content'].strip()
                filename = file.filename
                if not title:
                    now = datetime.datetime.now()
                    title = now.strftime("%d-%m-%Y %H:%M")
                user_id = current_user.id
                new_post = Posts(title=title, content=content, user_id=user_id)
                #filename = secure_filename(file.filename) безопасное извлечение ориг имя файла
                db.session.add(new_post)
                db.session.commit()
                id = new_post.id
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                os.mkdir(f"{path}//{current_user.username}//{id}")
                p = path + '//' + current_user.username + '//' + filename
                photo1 = analiz.test_zero_count_hist(p).savefig('p1.png')
                photo2 = analiz.test_zero_count_diag(p).savefig('p2.png')
                photo3 = analiz.practice_zero_count_hist(p).savefig('p3.png')
                photo4 = analiz.practice_zero_count_diag(p).savefig('p4.png')
                shutil.move(path[:-6] + "//" + 'p1.png', path + '//' + current_user.username + '//' + f'{id}' + '//' + 'p1.png')
                shutil.move(path[:-6] + "//" + 'p2.png', path + '//' + current_user.username + '//' + f'{id}' + '//' + 'p2.png')
                shutil.move(path[:-6] + "//" + 'p3.png', path + '//' + current_user.username + '//' + f'{id}' + '//' +'p3.png')
                shutil.move(path[:-6] + "//" + 'p4.png', path + '//' + current_user.username + '//' + f'{id}' + '//' + 'p4.png')
                os.remove(path + '//' + current_user.username + '//' + filename)
                return redirect(url_for('profile'))
        else:
            return render_template('create.html')
    else:
        return redirect(url_for('login'))


@app.route("/posts/<id_user>/post_del/<id_post>")
def post_delete(id_user, id_post):
    post = Posts.query.get_or_404(id_post)
    try:
        os.remove(path + '//' + current_user.username + '//' + f'{post.id}' + '//' + 'p1.png')
        os.remove(path + '//' + current_user.username + '//' + f'{post.id}' + '//' + 'p2.png')
        os.remove(path + '//' + current_user.username + '//' + f'{post.id}' + '//' + 'p3.png')
        os.remove(path + '//' + current_user.username + '//' + f'{post.id}' + '//' + 'p4.png')
        os.rmdir(path + '//' + current_user.username + '//' + f'{post.id}')
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('profile'))
    except:
        return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        res = db.session.query(Users, Posts).join(Posts, Users.id == Posts.user_id).all()
        res = [node for node in res if node[0].id == current_user.id]
        return render_template('profile.html', posts = res)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/posts/<id_user>/post_show/<id_post>')
def post_show1(id_user, id_post):
    path = "/static" + '/' + current_user.username + '/' + f'{id_post}'
    p1 = path + '/' + 'p1.png'
    p2 = path + '/' + 'p2.png'
    p3 = path + '/' + 'p3.png'
    p4 = path + '/' + 'p4.png'
    print(p1)
    return render_template('show.html', p1=p1, p2=p2, p3=p3, p4=p4)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)