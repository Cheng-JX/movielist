from flask import Flask, render_template

name = 'Cheng JX'
movies = [
    {'ID': '1001', 'Title': '战狼2', 'Date': '2017/7/27', 'Country': '中国', 'Genre': '战争', 'Year': '2017'},
    {'ID': '1002', 'Title': '哪吒之魔童降世', 'Date': '2019/7/26', 'Country': '中国', 'Genre': '动画', 'Year': '2019'},
    {'ID': '1003', 'Title': '流浪地球', 'Date': '2019/2/5', 'Country': '中国', 'Genre': '科幻', 'Year': '2019'},
    {'ID': '1004', 'Title': '复仇者联盟4', 'Date': '2019/4/24', 'Country': '美国', 'Genre': '科幻', 'Year': '2019'},
    {'ID': '1005', 'Title': '红海行动', 'Date': '2018/2/16', 'Country': '中国', 'Genre': '战争', 'Year': '2018'},
    {'ID': '1006', 'Title': '唐人街探案2', 'Date': '2018/2/16', 'Country': '中国', 'Genre': '喜剧', 'Year': '2018'},
    {'ID': '1007', 'Title': '我不是药神', 'Date': '2018/7/5', 'Country': '中国', 'Genre': '喜剧', 'Year': '2018'},
    {'ID': '1008', 'Title': '中国机长', 'Date': '2019/9/30', 'Country': '中国', 'Genre': '剧情', 'Year': '2019'},
    {'ID': '1009', 'Title': '速度与激情8', 'Date': '2017/4/14', 'Country': '美国', 'Genre': '动作', 'Year': '2017'},
    {'ID': '1010', 'Title': '西虹市首富', 'Date': '2018/7/27', 'Country': '中国', 'Genre': '喜剧', 'Year': '2018'},
    {'ID': '1011', 'Title': '复仇者联盟3', 'Date': '2018/5/11', 'Country': '美国', 'Genre': '科幻', 'Year': '2018'},
    {'ID': '1012', 'Title': '捉妖记2', 'Date': '2018/2/16', 'Country': '中国', 'Genre': '喜剧', 'Year': '2018'},
    {'ID': '1013', 'Title': '八佰', 'Date': '2020/08/21', 'Country': '中国', 'Genre': '战争', 'Year': '2020'},
    {'ID': '1014', 'Title': '姜子牙', 'Date': '2020/10/01', 'Country': '中国', 'Genre': '动画', 'Year': '2020'},
    {'ID': '1015', 'Title': '我和我的家乡', 'Date': '2020/10/01', 'Country': '中国', 'Genre': '剧情', 'Year': '2020'},
    {'ID': '1016', 'Title': '你好，李焕英', 'Date': '2021/02/12', 'Country': '中国', 'Genre': '喜剧', 'Year': '2021'},
    {'ID': '1017', 'Title': '长津湖', 'Date': '2021/09/30', 'Country': '中国', 'Genre': '战争', 'Year': '2021'},
    {'ID': '1018', 'Title': '速度与激情9', 'Date': '2021/05/21', 'Country': '中国', 'Genre': '动作', 'Year': '2021'}
]

app = Flask(__name__)
@app.route('/')
def index():
    return  render_template('index.html', name=name, movies=movies)