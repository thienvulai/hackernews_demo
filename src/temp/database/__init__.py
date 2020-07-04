from src.models import News
from src.app import db
import requests
from parsel import Selector
import datetime


def get_data():
    data = News.query.all()
    list_news = []
    item = {}

    for d in data:
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
        item['date_created'] = d.date_created
        item['hide'] = d.hide
        item['comment'] = d.comment

        list_news.append(item)

    return list_news


def update_data():
    html = 'https://news.ycombinator.com/news'
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


def update_page(url):
    text = requests.get(url).text
    sel = Selector(text=text)

    s1 = sel.xpath('.//table[@class="itemlist"]').get()
    sel = Selector(text=s1)

    for e in sel.css('tr'):
        test = e.xpath(".//descendant-or-self::tr/@class").get()

        if test == "morespace":
            break

        if test != "spacer":
            item = {}
            if test == "athing":
                # getting id
                Id = e.xpath(".//descendant-or-self::tr/@id").get()
                item['news_id'] = Id

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
                item['site'] = "https://news.ycombinator.com/from?site=" + str(domains).strip()

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
                    item['point'] = None

                # getting authors
                users = e.xpath(".//td[@class='subtext']/a[@class='hnuser']/text()").get()
                item['link_user'] = "https://news.ycombinator.com/user?id=" + str(users).strip()

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
                    item['time'] = datetime.datetime.now() - time
                else:
                    item['time'] = None

            new_news = News(
                id=item['id_d'],
                news_id=item['news_id'],
                title=item['title'],
                link=item['link'],
                domain=item['domain'],
                point=int(item['point']),
                user=item['user'],
                date_created=item['date_created'],
                hide=item['hide'],
                comment=item['comment']
            )
            db.session.add(new_news)
            db.session.commit()
