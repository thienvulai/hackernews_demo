import requests
import os
import datetime

from flask import Flask, render_template, request
from parsel import Selector
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from Hackerank_news.config import DATABASE_URI


app = Flask('__name__')

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class News(db.Model):
    __tablename__ = 'News'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_id = db.Column(db.String(100))
    rank = db.Column(db.Integer)
    title = db.Column(db.String(1000))
    link = db.Column(db.String(1000))
    domain = db.Column(db.String(1000))
    point = db.Column(db.String(1000))
    user = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)
    hide = db.Column(db.String(10))
    comment = db.Column(db.String(1000))

    def __init__(self, news_id, rank, title, link, domain, point, user, date_created, hide, comment):
        # self.id = id_d
        self.news_id = news_id
        self.rank = rank
        self.title = title
        self.link = link
        self.domain = domain
        self.point = point
        self.user = user
        self.date_created = date_created
        self.hide = hide
        self.comment = comment

    def __repr__(self):
        return '<News %r>' % self.news_id


def get_data():
    data = News.query.order_by(asc("rank")).all()
    list_news = []

    for d in data:
        item = {}

        item['rank'] = d.rank
        link_item = "https://news.ycombinator.com/item?id=" + str(d.news_id).strip()
        link_hide = "https://news.ycombinator.com/hide?id=" + str(d.news_id).strip() + "&go=news"
        link_vote = "https://news.ycombinator.com/vote?id=" + str(d.news_id).strip() + "&how=up&go=news"
        item['link_item'] = link_item
        item['link_hide'] = link_hide
        item['link_vote'] = link_vote

        if "http" not in str(d.link):
            item['link'] = "https://news.ycombinator.com/" + str(d.link)
        else:
            item['link'] = d.link

        item['title'] = d.title

        item['domain'] = d.domain
        item['site'] = "https://news.ycombinator.com/from?site=" + str(d.domain).strip()
        item['point'] = d.point
        item['user'] = d.user
        item['link_user'] = "https://news.ycombinator.com/user?id=" + str(d.user).strip()
        item['date_created'] = datetime.datetime.now() - d.date_created
        item['hide'] = d.hide
        item['comment'] = d.comment

        list_news.append(item)

    # print(list_news)
    return list_news


def update_data(html):
    text1 = requests.get(html).text
    sel1 = Selector(text=text1)
    s2 = sel1.xpath(".//descendant-or-self::tr/@class").get()
    i = 2
    while str(s2).strip() != "None":
        update_page(html)
        html = 'https://news.ycombinator.com/news' + "?p=" + str(i)
        text1 = requests.get(html).text
        sel1 = Selector(text=text1)
        s2 = sel1.xpath(".//descendant-or-self::tr/@class").get()
        i += 1


def save_to_db(new_news):

    temp_news = News.query.filter_by(news_id=new_news.news_id).first()

    if temp_news:
        temp_news.rank = int(new_news.rank)
        temp_news.title = new_news.title
        temp_news.link = new_news.link
        temp_news.domain = new_news.domain
        temp_news.point = new_news.point
        temp_news.user = new_news.user
        temp_news.date_created = new_news.date_created
        temp_news.hide = new_news.hide
        temp_news.comment = new_news.comment
        db.session.commit()
    else:
        db.session.add(new_news)
        db.session.commit()


def update_page(url):
    text = requests.get(url).text
    sel = Selector(text=text)

    s1 = sel.xpath('.//table[@class="itemlist"]').get()
    sel = Selector(text=s1)

    list_item = []
    for e in sel.css('tr'):

        test = e.xpath(".//descendant-or-self::tr/@class").get()

        # link_item = "https://news.ycombinator.com/item?id=" + str(id).strip()
        # link_hide = "https://news.ycombinator.com/hide?id=" + str(id).strip() + "&go=news"

        if test == "morespace":
            break

        if test != "spacer":
            if test == "athing":
                item = {
                    # 'link_item': link_item,
                    # 'link_hide': link_hide
                }

                # getting id
                Id = e.xpath(".//descendant-or-self::tr/@id").get()
                item['news_id'] = Id
                # print(link_hide)

                # getting rank
                rank = e.xpath(".//td/span[@class='rank']/text()").get()
                item['rank'] = rank[:len(rank) - 1]

                # getting links
                links = e.xpath(".//td/a[@class='storylink']/@href").get()
                if "http" not in str(links):
                    links = "https://news.ycombinator.com/" + str(links)
                if links is not None:
                    item['link'] = links
                else:
                    item['link'] = None

                # getting title
                titles = e.xpath(".//td/a[@class='storylink']/text()").get()
                if titles is not None:
                    item['title'] = titles
                else:
                    item['title'] = None

                # getting domain
                domains = e.xpath(""".//td/span[@class='sitebit comhead']
                                    /a/span[@class='sitestr']/text()""").get()

                if domains is not None:
                    item['domain'] = domains
                else:
                    item['domain'] = None

            if test is None:
                # getting points
                p1 = e.xpath(".//td[@class='subtext']/span[@class='score']/text()").get()
                if p1 is not None:
                    item['point'] = int(str(p1).split()[0])
                else:
                    item['point'] = -1

                # getting authors
                users = e.xpath(".//td[@class='subtext']/a[@class='hnuser']/text()").get()

                if users is not None:
                    item['user'] = users
                else:
                    item['user'] = None

                # getting hide
                hide = e.xpath(".//td[@class='subtext']/a[2]/text()").get()

                if hide is not None:
                    item['hide'] = hide.split()[0]
                else:
                    item['hide'] = None

                # getting comments
                comments = e.xpath(".//td[@class='subtext']/a[3]/text()").get()

                if comments is not None:
                    item['comment'] = comments.split()[0]
                else:
                    item['comment'] = None

                # getting time
                t = e.xpath(".//td[@class='subtext']/span[@class='age']/a/text()").get()
                h = int(str(t).split()[0])
                # change hours to datetime
                time = datetime.datetime.now() - datetime.timedelta(hours=h)

                if time is not None:
                    item['date_created'] = time#datetime.datetime.now() - time
                else:
                    item['date_created'] = None

                list_item.append(item)

    for i in range(0, len(list_item)):
        # print(News.query.filter_by(news_id=list_item[i]['news_id']).first())
        new_news = News(
            news_id=list_item[i]['news_id'],
            rank=int(list_item[i]['rank']),
            title=list_item[i]['title'],
            link=list_item[i]['link'],
            domain=list_item[i]['domain'],
            point=list_item[i]['point'],
            user=list_item[i]['user'],
            date_created=list_item[i]['date_created'],
            hide=list_item[i]['hide'],
            comment=list_item[i]['comment']
        )
        save_to_db(new_news)


@app.route('/')
def home():

    # update_page('https://news.ycombinator.com/news?p=16')
    update_data('https://news.ycombinator.com/news')
    return render_template('index.html', list_item=get_data())


@app.route('/send_news', methods=['GET', 'POST'])
def send_news():
    if request.method == 'POST':
        lst_news = News.query.filter(News.rank <= 10).order_by(asc("rank")).all()

        message = Mail(
            from_email='vuthlai84@gmail.com',
            to_emails='khoaanh.ph@gmail.com',
            subject='10 latest hacker news',
            html_content= render_template('latest_news.html', list_item=lst_news))

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    return render_template('send_news.html')


if __name__ == '__main__':
    app.run()
