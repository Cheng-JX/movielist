import os
import sys
import click

from flask import Flask, render_template
from flask import request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev' # 等同于 app.secret_key = 'dev'
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

class User(db.Model): # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(20)) # 名字
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
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id) # 获取电影记录
    db.session.delete(movie) # 删除对应的记录
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index')) # 重定向回主页