import re
from sqlalchemy import or_, and_
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

from movielist import app, db
from movielist.models import User, Movie, Actor, Relation, MovieBox #ActorBox

def split_keywords(keyword):
    # 使用正则表达式将中文拆成一个个文字，英文以空格为界拆成单词
    # 这里使用 Unicode 范围对中文进行匹配
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', keyword)
    english_words = re.findall(r'\b\w+\b', keyword)

    return chinese_chars + english_words




# 增加条目函数（Movie类、Actor类）
# ...（其他导入语句）

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        if 'submit_movie' in request.form:
            # 处理电影信息添加
            title = request.form.get('title')
            year = request.form.get('year')
            country = request.form.get('country')
            genre = request.form.get('genre')
            date_str = request.form.get('date')

            if not title or not year or not country or not genre or len(year) > 4 or len(title) > 255 or len(country) > 10 or len(genre) > 10:
                flash('无效输入。')
                return redirect(url_for('index'))

            try:
                date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None
            except ValueError:
                flash('无效的日期格式。请使用YYYY-MM-DD。')
                return redirect(url_for('index'))

            # 将电影数据保存到数据库
            movie = Movie(Title=title, Year=year, Country=country, Genre=genre, Date=date)
            db.session.add(movie)
            db.session.commit()

            flash('电影已添加。')

        elif 'submit_box' in request.form:
            # 处理票房添加
            title = request.form.get('title')
            box = request.form.get('box')

            if not title or not box:
                flash('无效输入。')
                return redirect(url_for('index'))

            try:
                box = float(box)
                if box < 0:
                    raise ValueError("票房必须是非负数。")
            except ValueError:
                flash(f'无效输入。')
                return redirect(url_for('index'))

            movie = Movie.query.filter_by(Title=title).first()

            if not movie:
                flash('找不到电影。')
                return redirect(url_for('index'))

            # 将票房数据保存到数据库
            movie_box = MovieBox(id=movie.id, Box=box)
            db.session.add(movie_box)
            db.session.commit()

            flash('已为电影添加票房。')

        return redirect(url_for('index'))

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)


@app.route('/sort/<option>')
def sort(option):
    if option == 'default':
        movies = Movie.query.order_by(Movie.id).all()
    elif option == 'date':
        movies = Movie.query.order_by(Movie.Date.desc(), Movie.id).all()
    elif option == 'box':
        movies = Movie.query.join(MovieBox, MovieBox.id == Movie.id).order_by(MovieBox.Box.desc(), Movie.id).all()
    else:
        flash('无效的排序选项。')
        return redirect(url_for('index'))

    return render_template('index.html', user=current_user, movies=movies)


@app.route('/actor', methods=['GET', 'POST'])
def actor():
    if request.method == 'POST':
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页

        name = request.form.get('name')
        gender = request.form.get('gender')
        country = request.form.get('country')

        # 验证数据
        if not name or not gender or not country or len(name) > 50 or len(gender) > 2 or len(country) > 50:
            flash('Invalid input.')
            return redirect(url_for('actor'))

        # 保存数据到数据库
        actor = Actor(Name=name, Gender=gender, Country=country)
        db.session.add(actor)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('actor'))

    user = User.query.first()
    actors = Actor.query.all()
    return render_template('actor.html', user=user, actors=actors)



# 编辑函数
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':

        if 'submit_m' in request.form:
            # 处理电影信息添加
            title = request.form.get('title')
            year = request.form.get('year')
            country = request.form.get('country')
            genre = request.form.get('genre')
            date_str = request.form.get('date')

            # 验证输入
            if not title or not year or not country or not genre or len(year) > 4 or len(title) > 255 or len(country) > 10 or len(genre) > 10:
                flash('无效的输入。')
                return redirect(url_for('edit', movie_id=movie_id))

            try:
                # 尝试将日期字符串转换为 datetime 对象
                date = datetime.strptime(date_str, '%Y/%m/%d') if date_str else None
            except ValueError:
                # 转换失败，日期格式不正确
                flash('无效的日期格式。')
                return redirect(url_for('index'))

            # 更新电影记录
            movie.Title = title
            movie.Year = year
            movie.Country = country
            movie.Genre = genre
            movie.Date = date

            # 提交更改到数据库
            db.session.commit()

            flash('电影信息已更新。')
            return redirect(url_for('index'))

        elif 'submit_b' in request.form:
            # 处理票房编辑
            box = request.form.get('box')

            if box:
                try:
                    box = float(box)
                    if box < 0:
                        raise ValueError("票房必须是非负数。")
                except ValueError:
                    flash(f'无效输入。')
                    return redirect(url_for('edit', movie_id=movie_id))

                # 查询电影票房记录
                movie_box = MovieBox.query.filter_by(id=movie.id).first()

                if not movie_box:
                    # 如果不存在票房记录，创建新的票房记录
                    movie_box = MovieBox(id=movie.id, Box=box)
                    db.session.add(movie_box)
                else:
                    # 如果存在票房记录，更新票房值
                    movie_box.Box = box

                # 提交更改到数据库
                db.session.commit()

                flash('电影票房已更新。')
                return redirect(url_for('index'))

    # 使用电影详细信息和关系呈现编辑页面
    return render_template('edit.html', movie=movie)


# 定义演员编辑页面的路由
@app.route('/actor/edit/<int:actor_id>', methods=['GET', 'POST'])
@login_required
def actor_edit(actor_id):
    actor = Actor.query.get_or_404(actor_id)

    if request.method == 'POST':
        # 处理编辑演员表单的提交请求
        name = request.form['name']
        gender = request.form['gender']
        country = request.form['country']

        # 验证输入
        if not name or not gender or not country or len(name) > 50 or len(gender) > 2 or len(country) > 50:
            flash('无效的输入。')
            return redirect(url_for('actor_edit', actor_id=actor_id))

        # 更新演员记录
        actor.Name = name
        actor.Gender = gender
        actor.Country = country

        # 提交更改到数据库
        db.session.commit()

        flash('演员信息已更新。')
        return redirect(url_for('actor'))

    # 使用演员详细信息和关系呈现编辑页面
    return render_template('actor_edit.html', actor=actor)



# 删除函数
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    # 删除电影相关的票房记录
    movie_box = MovieBox.query.filter_by(id=movie_id).first()
    if movie_box:
        db.session.delete(movie_box)

    # 删除所有与电影相关的关联记录
    try:
        relations_to_delete = Relation.query.filter_by(movie_id=movie_id).all()
        for relation in relations_to_delete:
            db.session.delete(relation)
        db.session.commit()
    except:
        pass  # 不执行任何处理，直接通过

    # 更新所有关联记录中的 actor_id
    relations_to_update = Relation.query.filter(Relation.movie_id > movie_id).all()
    for relation in relations_to_update:
        relation.movie_id -= 1

    db.session.delete(movie)

    # 更新movie_id
    movies_to_update = Movie.query.filter(Movie.id > movie_id).all()
    for movie in movies_to_update:
        movie.id -= 1
    db.session.commit()
    flash('已删除选择电影。')
    return redirect(url_for('index'))

@app.route('/actor/delete/<int:actor_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)  # 获取演职人员记录

    # 删除所有与演员相关的关联记录
    try:
        relations_to_delete = Relation.query.filter_by(actor_id=actor_id).all()
        for relation in relations_to_delete:
            db.session.delete(relation)
        db.session.commit()
    except:
        pass  # 不执行任何处理，直接通过

    # 更新所有关联记录中的 actor_id
    relations_to_update = Relation.query.filter(Relation.actor_id > actor_id).all()
    for relation in relations_to_update:
        relation.actor_id -= 1

    db.session.delete(actor)  # 删除对应的记录

    # 更新actor_id
    actors_to_update = Actor.query.filter(Actor.id > actor_id).all()
    for actor in actors_to_update:
        actor.id -= 1

    db.session.commit()  # 提交数据库会话
    flash('已删除选择人员。')
    return redirect(url_for('actor'))  # 重定向回演职人员主页



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
        keyword_conditions = or_(
            Movie.Country == keyword,
            Movie.Genre == keyword,
            Movie.Year == keyword,
        )

        # 合并条件
        # 合并条件，只要有一个匹配上即可
        movie_conditions = or_(
            *title_conditions,
            *keyword_conditions
        )

        actor_conditions = or_(
            Actor.Name == keyword,
            Actor.Country == keyword
        )

        movie_results = Movie.query.filter(movie_conditions).all()
        actor_results = Actor.query.filter(actor_conditions).all()

        # 获取用户选择的排序选项，默认为默认顺序
        sort_option = request.form.get('sort_option', 'default')

        # 对搜索结果进行排序
        movie_results = sort_movie_results(movie_results, sort_option)

        return render_template('search_results.html', keyword=keyword, movie_results=movie_results, actor_results=actor_results, sort_option=sort_option)

    return render_template('search_results.html')  # 渲染搜索页面的表单

def sort_movie_results(movie_results, sort_option):
    if sort_option == 'default':
        return movie_results
    elif sort_option == 'date':
        return sorted(movie_results, key=lambda x: x.Date, reverse=True)
    elif sort_option == 'box':
        # 获取电影票房信息
        movie_box_mapping = {box.id: box.Box for box in MovieBox.query.all()}
        # 使用 get 方法获取票房值，如果不存在，默认为 0
        return sorted(movie_results, key=lambda x: movie_box_mapping.get(x.id, 0), reverse=True)
    else:
        # 如果选项无效，返回未排序的结果
        flash('无效的排序选项。')
        return movie_results



@app.route('/movie_detail/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get(movie_id)

    # 根据类型查询导演和主演
    director_relations = Relation.query.filter_by(movie_id=movie_id, type='导演').all()
    main_actor_relations = Relation.query.filter_by(movie_id=movie_id, type='主演').all()

    directors = [relation.actor for relation in director_relations]
    main_actors = [relation.actor for relation in main_actor_relations]

    # 查询电影票房信息
    movie_box = MovieBox.query.filter_by(id=movie_id).first()

    return render_template('movie_detail.html', movie=movie, directors=directors, main_actors=main_actors, movie_box=movie_box)

@app.route('/actor_detail/<int:actor_id>')
def actor_detail(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        return render_template('error.html', error='演员未找到')

    # 查询演员作为主演和导演的电影
    main_actor_relations = Relation.query.filter_by(actor_id=actor_id, type='主演').all()
    director_relations = Relation.query.filter_by(actor_id=actor_id, type='导演').all()

    main_actor_movies = [relation.movie for relation in main_actor_relations]
    director_movies = [relation.movie for relation in director_relations]

    return render_template('actor_detail.html', actor=actor, main_actor_movies=main_actor_movies, director_movies=director_movies)




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
