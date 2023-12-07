import click

from datetime import datetime
from movielist import app, db
from movielist.models import User, Movie


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