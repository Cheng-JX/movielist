import os
import sys
import click

from flask import Flask, render_template
from flask import request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import login_required, logout_user
from flask_login import login_required, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev' # 等同于 app.secret_key = 'dev'
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
login_manager = LoginManager(app) # 实例化扩展类


class User(db.Model, UserMixin): # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(20)) # 名字
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  #将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)
    # 返回布尔值
class Movie(db.Model): # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True, unique=True) # 主键
    Title = db.Column(db.String(255), nullable = False) # 电影标题
    Date = db.Column(db.DateTime) # 上映日期
    Country = db.Column(db.String(10)) # 电影国家
    Genre = db.Column(db.String(10)) # 电影类型
    Year = db.Column(db.String(4)) # 电影年份

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'Cheng JX'
    movies = [
        {'Title': '战狼2', 'Date': '2017/7/27', 'Country': '中国', 'Genre': '战争', 'Year': '2017'},
        {'Title': '哪吒之魔童降世', 'Date': '2019/7/26', 'Country': '中国', 'Genre': '动画', 'Year': '2019'},
        {'Title': '流浪地球', 'Date': '2019/2/5', 'Country': '中国', 'Genre': '科幻', 'Year': '2019'},
        {'Title': '复仇者联盟4', 'Date': '2019/4/24', 'Country': '美国', 'Genre': '科幻', 'Year': '2019'},
        {'Title': '红海行动', 'Date': '2018/2/16', 'Country': '中国', 'Genre': '战争', 'Year': '2018'},
        {'Title': '唐人街探案2', 'Date': '2018/2/16', 'Country': '中国', 'Genre': '喜剧', 'Year': '2018'},
        {'Title': '我不是药神', 'Date': '2018/7/5', 'Country': '中国', 'Genre': '喜剧', 'Year': '2018'},
        {'Title': '中国机长', 'Date': '2019/9/30', 'Country': '中国', 'Genre': '剧情', 'Year': '2019'},
        {'Title': '速度与激情8', 'Date': '2017/4/14', 'Country': '美国', 'Genre': '动作', 'Year': '2017'},
        {'Title': '西虹市首富', 'Date': '2018/7/27', 'Country': '中国', 'Genre': '喜剧', 'Year': '2018'},
        {'Title': '复仇者联盟3', 'Date': '2018/5/11', 'Country': '美国', 'Genre': '科幻', 'Year': '2018'},
        {'Title': '捉妖记2', 'Date': '2018/2/16', 'Country': '中国', 'Genre': '喜剧', 'Year': '2018'},
        {'Title': '八佰', 'Date': '2020/08/21', 'Country': '中国', 'Genre': '战争', 'Year': '2020'},
        {'Title': '姜子牙', 'Date': '2020/10/01', 'Country': '中国', 'Genre': '动画', 'Year': '2020'},
        {'Title': '我和我的家乡', 'Date': '2020/10/01', 'Country': '中国', 'Genre': '剧情', 'Year': '2020'},
        {'Title': '你好，李焕英', 'Date': '2021/02/12', 'Country': '中国', 'Genre': '喜剧', 'Year': '2021'},
        {'Title': '长津湖', 'Date': '2021/09/30', 'Country': '中国', 'Genre': '战争', 'Year': '2021'},
        {'Title': '速度与激情9', 'Date': '2021/05/21', 'Country': '中国', 'Genre': '动作', 'Year': '2021'}
    ]

    user = User(name=name)
    db.session.add(user)

    for m in movies:
        movie = Movie(
            Title=m['Title'],
            Date=datetime.strptime(m['Date'], '%Y/%m/%d'),
            Country=m['Country'],
            Genre=m['Genre'],
            Year=m['Year']
        )
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop: # 判断是否输入了选项
        db.drop_all()
        db.create_all()
    click.echo('Initialized database.') # 输出提示信息

@app.context_processor
def inject_user(): # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user) # 需要返回字典，等同于return {'user': user}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页

        title = request.form.get('title')
        year = request.form.get('year')
        country = request.form.get('country')
        genre = request.form.get('genre')
        date_str = request.form.get('date')

        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 255 or len(country) > 10 or len(genre) > 10:
            flash('Invalid input.')
            return redirect(url_for('index'))

        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None

        # 保存数据到数据库
        movie = Movie(Title=title, Year=year, Country=country, Genre=genre, Date=date)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    return render_template('404.html'), 404 # 返回模板和状态码

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        country = request.form['country']
        genre = request.form['genre']
        date_str = request.form['date']

        # 验证输入
        if not title or not year or len(year) > 4 or len(title) > 255 or len(country) > 10 or len(genre) > 10:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        date = datetime.strptime(date_str, '%Y/%m/%d') if date_str else None

        # 更新电影记录
        movie.Title = title
        movie.Year = year
        movie.Country = country
        movie.Genre = genre
        movie.Date = date

        # 提交更改到数据库
        db.session.commit()

        flash('Item updated.')
        return redirect(url_for('index'))

    # 使用电影详细信息呈现编辑页面
    return render_template('edit.html', movie=movie)

@app.route('/movie/delete/<int:movie_id>', methods=['POST']) #限定只接受 POST 请求
@login_required # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id) # 获取电影记录
    db.session.delete(movie) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index')) # 重定向回主页

@app.cli.command()
@click.option('--username', prompt=True, help='The username usedto login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password) # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password) # 设置密码
        db.session.add(user)

    db.session.commit() # 提交数据库会话
    click.echo('Done.')


@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
    return user # 返回用户对象

login_manager.login_view = 'login'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user) # 登入用户
            flash('Login success.')
            return redirect(url_for('index')) # 重定向到主页

        flash('Invalid username or password.') # 如果验证失败，显示错误消息
        return redirect(url_for('login')) # 重定向回登录页面

    return render_template('login.html')

@app.route('/logout')
@login_required # 用于视图保护，后面会详细介绍
def logout():
    logout_user() # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index')) # 重定向回首页

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')