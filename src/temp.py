# import requests
# from bs4 import BeautifulSoup
#
# request = requests.get('https://news.ycombinator.com/news')
# content = request.content
# soup = BeautifulSoup(content, "html.parser")
# table = soup.find("table", {"class": "itemlist"})
#
# data = table.get_text()
# match = data.split("\n\n")
# match = match[1:len(match) - 1]
#
# list_item = []
#
# for i in range(0, len(match)):
#     ite = match[i].split("\n")
#
#     if ite[0] == '':
#         ite.pop(0)
#
#     item = {}
#
#     # FIRST PART
#     # --------------------------------------------
#     pos1 = 0
#
#     # get index
#     pos2 = ite[0].find(".")
#     item['index'] = ite[0][pos1:pos2].strip()
#     ite[0] = ite[0][pos2 + 2:]
#     print(ite[0])
#
#     # get site
#     if ite[0].find(')') != -1:
#         pos1 = ite[0].rindex('(') + 1
#         pos2 = len(ite[0]) - 1
#
#         item['site'] = ite[0][pos1:pos2].strip()
#     else:
#         item['site'] = None
#
#     # get story
#     pos2 = pos1 - 2
#     pos1 = 0
#     item['story'] = ite[0][pos1:pos2]
#
#     # SECOND PART
#     # --------------------------------------------
#     pos1 = 0
#     pos2 = len(ite[0])
#
#     # get point
#     if ite[1].find('point') != -1:
#         pos2 = ite[1].find(' ')
#         item['point'] = ite[1][pos1:pos2].strip()
#     else:
#         item['point'] = None
#
#     # get user
#     if ite[1].find('by') != -1:
#         pos1 = ite[1].find('by') + 3
#         ite[1] = ite[1][pos1:]
#         pos1 = ite[1].find('by') + 1
#         pos2 = ite[1].find(' ')
#
#         item['user'] = ite[1][pos1:pos2]
#     else:
#         item['user'] = None
#     # get age
#     if ite[1].find('ago') != -1:
#         ite[1] = ite[1][pos2 + 1:]
#
#         pos1 = 0
#         pos2 = ite[1].find('|')
#         item['age'] = ite[1][pos1:pos2].strip()
#
#     else:
#         item['age'] = None
#
#     # get hide
#     if ite[1].find('hide') != -1:
#         ite[1] = ite[1][ite[1].find('|') + 1:].strip()
#         item['hide'] = 'hide'
#     else:
#         item['hide'] = None
#
#     # get comments
#     ite[1] = ite[1][ite[1].find('|') + 2:len(ite[1])].strip()
#
#     if ite[1].find('comment') != -1:
#         pos1 = 0
#         pos2 = ite[1].find(' ') - 8
#         item['comment'] = ite[1][pos1:pos2].strip()
#
#     elif ite[1].find('discuss') != -1:
#         item['comment'] = 'discuss'
#     else:
#         item['comment'] = None
#
#     list_item.append(item)
from flask import Flask, render_template
import requests
from parsel import Selector
import datetime

app = Flask('__name__')

app.config['DEBUG'] = True

url = 'https://news.ycombinator.com/news'
text = requests.get(url).text
sel = Selector(text=text)


def check_page():
    html = 'https://news.ycombinator.com/news'
    text1 = requests.get(html).text
    sel1 = Selector(text=text1)
    s2 = sel1.xpath(".//descendant-or-self::tr/@class").get()
    i = 2
    while str(s2).strip() != "None":
        print(html)
        print(str(i))
        html = 'https://news.ycombinator.com/news' + "?p=" + str(i)
        text1 = requests.get(html).text
        sel1 = Selector(text=text1)
        s2 = sel1.xpath(".//descendant-or-self::tr/@class").get()
        i += 1


check_page()

# # insert
# ex = News()
# db.session.add(ex)
# db.session.commit()
#
# # update
# ex = News.query.filter_by(id=1).first()
# ex.news_id = "123456"
# db.session.commit()
#
# # delete
# ex = News.query.filter_by(id=1).first()
# db.session.delete(ex)
# db.session.commit()


# text = requests.get(url).text
#     sel = Selector(text=text)
#
#     s1 = sel.xpath('.//table[@class="itemlist"]').get()
#     sel = Selector(text=s1)
#
#     list_item = []
#     for e in sel.css('tr'):
#
#         test = e.xpath(".//descendant-or-self::tr/@class").get()
#
#         if test == "morespace":
#             break
#
#         if test != "spacer":
#             if test == "athing":
#                 item = {
#                     # 'link_item': link_item,
#                     # 'link_hide': link_hide
#                 }
#
#                 # getting id
#                 Id = e.xpath(".//descendant-or-self::tr/@id").get()
#                 link_item = "https://news.ycombinator.com/item?id=" + str(Id).strip()
#                 link_hide = "https://news.ycombinator.com/hide?id=" + str(Id).strip() + "&go=news"
#                 link_vote = "https://news.ycombinator.com/vote?id=" + str(Id).strip() + "&how=up&go=news"
#                 item['link_item'] = link_item
#                 item['link_hide'] = link_hide
#                 item['link_vote'] = link_vote
#                 # print(link_hide)
#
#                 # getting rank
#                 rank = e.xpath(".//td/span[@class='rank']/text()").get()
#                 item['rank'] = rank[:len(rank) - 1]
#
#                 # getting links
#                 links = e.xpath(".//td/a[@class='storylink']/@href").get()
#                 if "http" not in str(links):
#                     links = "https://news.ycombinator.com/" + str(links)
#                 if links is not None:
#                     item['link'] = links
#                 else:
#                     item['link'] = None
#
#                 # getting title
#                 titles = e.xpath(".//td/a[@class='storylink']/text()").get()
#                 if titles is not None:
#                     item['title'] = titles
#                 else:
#                     item['title'] = None
#
#                 # getting domain
#                 domains = e.xpath(""".//td/span[@class='sitebit comhead']
#                                     /a/span[@class='sitestr']/text()""").get()
#                 item['site'] = "https://news.ycombinator.com/from?site=" + str(domains).strip()
#
#                 if domains is not None:
#                     item['domain'] = domains
#                 else:
#                     item['domain'] = None
#
#             if test is None:
#                 # getting points
#                 p1 = e.xpath(".//td[@class='subtext']/span[@class='score']/text()").get()
#                 if p1 is not None:
#                     item['point'] = int(str(p1).split()[0])
#                 else:
#                     item['point'] = None
#
#                 # getting authors
#                 users = e.xpath(".//td[@class='subtext']/a[@class='hnuser']/text()").get()
#                 item['link_user'] = "https://news.ycombinator.com/user?id=" + str(users).strip()
#
#                 if users is not None:
#                     item['user'] = users
#                 else:
#                     item['user'] = None
#
#                 # getting hide
#                 hide = e.xpath(".//td[@class='subtext']/a[2]/text()").get()
#
#                 if hide is not None:
#                     item['hide'] = hide.split()[0]
#                 else:
#                     item['hide'] = None
#
#                 # getting comments
#                 comments = e.xpath(".//td[@class='subtext']/a[3]/text()").get()
#
#                 if comments is not None:
#                     item['comment'] = comments.split()[0]
#                 else:
#                     item['comment'] = None
#
#                 # getting time
#                 t = e.xpath(".//td[@class='subtext']/span[@class='age']/a/text()").get()
#                 h = int(str(t).split()[0])
#                 # change hours to datetime
#                 time = datetime.datetime.now() - datetime.timedelta(hours=h)
#
#                 if time is not None:
#                     item['time'] = datetime.datetime.now() - time
#                 else:
#                     item['time'] = None
#
#                 list_item.append(item)

# App File


def check_page():
    html = 'https://news.ycombinator.com/news'
    text1 = requests.get(html).text
    sel1 = Selector(text=text1)
    s2 = sel1.xpath(".//descendant-or-self::tr/@class").get()
    i = 2
    while str(s2).strip() != "None":
        print(html)
        print(str(i))
        html = 'https://news.ycombinator.com/news' + "?p=" + str(i)
        text1 = requests.get(html).text
        sel1 = Selector(text=text1)
        s2 = sel1.xpath(".//descendant-or-self::tr/@class").get()
        i += 1


url = 'https://news.ycombinator.com/news'
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
            link_item = "https://news.ycombinator.com/item?id=" + str(Id).strip()
            link_hide = "https://news.ycombinator.com/hide?id=" + str(Id).strip() + "&go=news"
            link_vote = "https://news.ycombinator.com/vote?id=" + str(Id).strip() + "&how=up&go=news"
            item['link_item'] = link_item
            item['link_hide'] = link_hide
            item['link_vote'] = link_vote
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

            list_item.append(item)