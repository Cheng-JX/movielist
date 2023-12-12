import click

from datetime import datetime
from movielist import app, db
from movielist.models import User, Movie, Actor, Relation, MovieBox #ActorBox


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'Cheng JX'

    # 添加Movie初始行
    movie_init_data = {'id': 1000, 'Title': '', 'Date': datetime(1900,1,1), 'Country': '', 'Genre': '', 'Year': ''}
    movie_init = Movie(**movie_init_data)
    db.session.add(movie_init)

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
        {'Title': '速度与激情9', 'Date': '2021/05/21', 'Country': '中国', 'Genre': '动作', 'Year': '2021'},
    ]

    # 添加MovieBox初始行
    movie_box_init_data = {'id': 1000, 'Box': 0}
    movie_box_init = MovieBox(**movie_box_init_data)
    db.session.add(movie_box_init)

    # 电影票房数据
    movie_box = [
        {'Box': 56.84},
        {'Box': 50.15},
        {'Box': 46.86},
        {'Box': 42.5},
        {'Box': 36.5},
        {'Box': 33.97},
        {'Box': 31},
        {'Box': 29.12},
        {'Box': 26.7},
        {'Box': 25.47},
        {'Box': 23.9},
        {'Box': 22.37},
        {'Box': 30.10},
        {'Box': 16.02},
        {'Box': 28.29},
        {'Box': 54.13},
        {'Box': 53.48},
        {'Box': 13.92},
    ]

    # 添加Actor初始行
    actor_init_data = {'id': 2000, 'Name': '', 'Gender': '', 'Country': ''}
    actor_init = Actor(**actor_init_data)
    db.session.add(actor_init)

    # 插入演员信息
    actors = [
        {'Name': '吴京', 'Gender': '男', 'Country': '中国'},
        {'Name': '饺子', 'Gender': '男', 'Country': '中国'},
        {'Name': '屈楚萧', 'Gender': '男', 'Country': '中国'},
        {'Name': '郭帆', 'Gender': '男', 'Country': '中国'},
        {'Name': '乔罗素', 'Gender': '男', 'Country': '美国'},
        {'Name': '小罗伯特·唐尼', 'Gender': '男', 'Country': '美国'},
        {'Name': '克里斯·埃文斯', 'Gender': '男', 'Country': '美国'},
        {'Name': '林超贤', 'Gender': '男', 'Country': '中国'},
        {'Name': '张译', 'Gender': '男', 'Country': '中国'},
        {'Name': '黄景瑜', 'Gender': '男', 'Country': '中国'},
        {'Name': '陈思诚', 'Gender': '男', 'Country': '中国'},
        {'Name': '王宝强', 'Gender': '男', 'Country': '中国'},
        {'Name': '刘昊然', 'Gender': '男', 'Country': '中国'},
        {'Name': '文牧野', 'Gender': '男', 'Country': '中国'},
        {'Name': '徐峥', 'Gender': '男', 'Country': '中国'},
        {'Name': '刘伟强', 'Gender': '男', 'Country': '中国'},
        {'Name': '张涵予', 'Gender': '男', 'Country': '中国'},
        {'Name': 'F·加里·格雷', 'Gender': '男', 'Country': '美国'},
        {'Name': '范·迪塞尔', 'Gender': '男', 'Country': '美国'},
        {'Name': '杰森·斯坦森', 'Gender': '男', 'Country': '美国'},
        {'Name': '闫非', 'Gender': '男', 'Country': '中国'},
        {'Name': '沈腾', 'Gender': '男', 'Country': '中国'},
        {'Name': '安东尼·罗素', 'Gender': '男', 'Country': '美国'},
        {'Name': '克里斯·海姆斯沃斯', 'Gender': '男', 'Country': '美国'},
        {'Name': '许诚毅', 'Gender': '男', 'Country': '中国'},
        {'Name': '梁朝伟', 'Gender': '男', 'Country': '中国'},
        {'Name': '白百何', 'Gender': '女', 'Country': '中国'},
        {'Name': '井柏然', 'Gender': '男', 'Country': '中国'},
        {'Name': '管虎', 'Gender': '男', 'Country': '中国'},
        {'Name': '王千源', 'Gender': '男', 'Country': '中国'},
        {'Name': '姜武', 'Gender': '男', 'Country': '中国'},
        {'Name': '宁浩', 'Gender': '男', 'Country': '中国'},
        {'Name': '葛优', 'Gender': '男', 'Country': '中国'},
        {'Name': '范伟', 'Gender': '男', 'Country': '中国'},
        {'Name': '贾玲', 'Gender': '女', 'Country': '中国'},
        {'Name': '张小斐', 'Gender': '女', 'Country': '中国'},
        {'Name': '陈凯歌', 'Gender': '男', 'Country': '中国'},
        {'Name': '徐克', 'Gender': '男', 'Country': '中国'},
        {'Name': '易烊千玺', 'Gender': '男', 'Country': '中国'},
        {'Name': '林诣彬', 'Gender': '男', 'Country': '美国'},
        {'Name': '米歇尔·罗德里格兹', 'Gender': '女', 'Country': '美国'},
    ]

    relations = [
        {'movie_id': 1001, 'actor_id': 2001, 'type': '主演'},
        {'movie_id': 1001, 'actor_id': 2001, 'type': '导演'},
        {'movie_id': 1002, 'actor_id': 2002, 'type': '导演'},
        {'movie_id': 1003, 'actor_id': 2001, 'type': '主演'},
        {'movie_id': 1003, 'actor_id': 2003, 'type': '主演'},
        {'movie_id': 1003, 'actor_id': 2004, 'type': '导演'},
        {'movie_id': 1004, 'actor_id': 2005, 'type': '导演'},
        {'movie_id': 1004, 'actor_id': 2006, 'type': '主演'},
        {'movie_id': 1004, 'actor_id': 2007, 'type': '主演'},
        {'movie_id': 1005, 'actor_id': 2008, 'type': '导演'},
        {'movie_id': 1005, 'actor_id': 2009, 'type': '主演'},
        {'movie_id': 1005, 'actor_id': 2010, 'type': '主演'},
        {'movie_id': 1006, 'actor_id': 2011, 'type': '导演'},
        {'movie_id': 1006, 'actor_id': 2012, 'type': '主演'},
        {'movie_id': 1006, 'actor_id': 2013, 'type': '主演'},
        {'movie_id': 1007, 'actor_id': 2014, 'type': '导演'},
        {'movie_id': 1007, 'actor_id': 2015, 'type': '主演'},
        {'movie_id': 1008, 'actor_id': 2016, 'type': '导演'},
        {'movie_id': 1008, 'actor_id': 2017, 'type': '主演'},
        {'movie_id': 1009, 'actor_id': 2018, 'type': '导演'},
        {'movie_id': 1009, 'actor_id': 2019, 'type': '主演'},
        {'movie_id': 1009, 'actor_id': 2020, 'type': '主演'},
        {'movie_id': 1010, 'actor_id': 2021, 'type': '导演'},
        {'movie_id': 1010, 'actor_id': 2022, 'type': '主演'},
        {'movie_id': 1011, 'actor_id': 2023, 'type': '导演'},
        {'movie_id': 1011, 'actor_id': 2006, 'type': '主演'},
        {'movie_id': 1011, 'actor_id': 2024, 'type': '主演'},
        {'movie_id': 1012, 'actor_id': 2025, 'type': '导演'},
        {'movie_id': 1012, 'actor_id': 2026, 'type': '主演'},
        {'movie_id': 1012, 'actor_id': 2027, 'type': '主演'},
        {'movie_id': 1012, 'actor_id': 2028, 'type': '主演'},
        {'movie_id': 1013, 'actor_id': 2029, 'type': '导演'},
        {'movie_id': 1013, 'actor_id': 2030, 'type': '主演'},
        {'movie_id': 1013, 'actor_id': 2009, 'type': '主演'},
        {'movie_id': 1013, 'actor_id': 2031, 'type': '主演'},
        {'movie_id': 1015, 'actor_id': 2032, 'type': '导演'},
        {'movie_id': 1015, 'actor_id': 2015, 'type': '导演'},
        {'movie_id': 1015, 'actor_id': 2011, 'type': '导演'},
        {'movie_id': 1015, 'actor_id': 2015, 'type': '主演'},
        {'movie_id': 1015, 'actor_id': 2033, 'type': '主演'},
        {'movie_id': 1015, 'actor_id': 2034, 'type': '主演'},
        {'movie_id': 1016, 'actor_id': 2035, 'type': '导演'},
        {'movie_id': 1016, 'actor_id': 2035, 'type': '主演'},
        {'movie_id': 1016, 'actor_id': 2036, 'type': '主演'},
        {'movie_id': 1016, 'actor_id': 2022, 'type': '主演'},
        {'movie_id': 1017, 'actor_id': 2037, 'type': '导演'},
        {'movie_id': 1017, 'actor_id': 2038, 'type': '导演'},
        {'movie_id': 1017, 'actor_id': 2008, 'type': '导演'},
        {'movie_id': 1017, 'actor_id': 2001, 'type': '主演'},
        {'movie_id': 1017, 'actor_id': 2039, 'type': '主演'},
        {'movie_id': 1018, 'actor_id': 2040, 'type': '导演'},
        {'movie_id': 1018, 'actor_id': 2019, 'type': '主演'},
        {'movie_id': 1018, 'actor_id': 2041, 'type': '主演'}
    ]

    # 添加ActorBox初始行
    #actor_box_init_data = {'id': 2000, 'Box': 0}
    #actor_box_init = ActorBox(**actor_box_init_data)
    #db.session.add(actor_box_init)

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

    for box_data in movie_box:
        # 插入电影票房数据
        movie_box = MovieBox(
            Box=box_data['Box']
        )
        db.session.add(movie_box)

    for a in actors:
        actor = Actor(
            Name=a['Name'],
            Gender=a['Gender'],
            Country=a['Country']
        )
        db.session.add(actor)

    for rel_data in relations:
        relation = Relation(
            movie_id=rel_data['movie_id'],
            actor_id=rel_data['actor_id'],
            type=rel_data['type']
        )
        db.session.add(relation)

    db.session.commit()
    click.echo('Done.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')