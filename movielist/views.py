import re
from sqlalchemy import or_, and_
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

from movielist import app, db
from movielist.models import User, Movie

def split_keywords(keyword):
    # 使用正则表达式将中文拆成一个个文字，英文以空格为界拆成单词
    # 这里使用 Unicode 范围对中文进行匹配
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', keyword)
    english_words = re.findall(r'\b\w+\b', keyword)

    return chinese_chars + english_words

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

        try:
            # 尝试将日期字符串转换为 datetime 对象
            date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None
        except ValueError:
            # 转换失败，日期格式不正确
            flash('请按照YYYY-MM-DD的格式输入日期')
            return redirect(url_for('index'))

        # 保存数据到数据库
        movie = Movie(Title=title, Year=year, Country=country, Genre=genre, Date=date)
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


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


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get('keyword')

        if not keyword:
            flash('请输入搜索关键字。')
            return redirect(url_for('index'))

        # 对Title进行中文或英文的字符串拆解
        title_conditions = [
            Movie.Title.ilike(f"%{char}%") for char in split_keywords(keyword)
        ]

        # 其他字段进行精确搜索
        keyword_conditions = [
            Movie.Country == keyword,
            Movie.Genre == keyword,
            Movie.Year == keyword,
        ]

        # 合并条件
        # 合并条件，只要有一个匹配上即可
        conditions = or_(
            *title_conditions,
            *keyword_conditions
        )

        results = Movie.query.filter(conditions).all()

        if not results:
            flash(f'未找到与"{keyword}"相关的电影。')
            return render_template('not_found.html')

        return render_template('search_results.html', keyword=keyword, results=results)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))
