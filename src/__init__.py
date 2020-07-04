# from flask import Flask, render_template
# import requests
# from parsel import Selector
# import datetime
#
# app = Flask('__name__', template_folder="templates")
#
# app.config['DEBUG'] = True
#
# url = 'https://news.ycombinator.com/news'
# text = requests.get(url).text
# sel = Selector(text=text)
#
# list_item = []
#
# s1 = sel.xpath('.//table[@class="itemlist"]').get()
# sel = Selector(text=s1)
#
# for e in sel.css('tr'):
#
#     test = e.xpath(".//descendant-or-self::tr/@class").get()
#
#     if test == "morespace":
#         break
#
#     if test != "spacer":
#         if test == "athing":
#             item = {}
#
#             # getting rank
#             rank = e.xpath(".//td/span[@class='rank']/text()").get()
#             item['rank'] = rank[:len(rank) - 1]
#
#             # getting links
#             links = e.xpath(".//td/a[@class='storylink']/@href").get()
#             if "http" not in str(links):
#                 links = "https://news.ycombinator.com/" + str(links)
#             if links is not None:
#                 item['link'] = links
#             else:
#                 item['link'] = None
#
#             # getting title
#             titles = e.xpath(".//td/a[@class='storylink']/text()").get()
#             if titles is not None:
#                 item['title'] = titles
#             else:
#                 item['title'] = None
#
#             # getting domain
#             domains = e.xpath(""".//td/span[@class='sitebit comhead']
#                                 /a/span[@class='sitestr']/text()""").get()
#
#             if domains is not None:
#                 item['domain'] = domains
#             else:
#                 item['domain'] = None
#
#         if test is None:
#             # getting points
#             p1 = e.xpath(".//td[@class='subtext']/span[@class='score']/text()").get()
#             if p1 is not None:
#                 item['point'] = int(str(p1).split()[0])
#             else:
#                 item['point'] = None
#
#             # getting authorss
#             users = e.xpath(".//td[@class='subtext']/a[@class='hnuser']/text()").get()
#
#             if users is not None:
#                 item['user'] = users
#             else:
#                 item['user'] = None
#
#             # getting comments
#             comments = e.xpath(".//td[@class='subtext']/a[3]/text()").get()
#
#             if comments is not None:
#                 item['comment'] = comments.split()[0]
#             else:
#                 item['comment'] = None
#
#             # getting time
#             t = e.xpath(".//td[@class='subtext']/span[@class='age']/a/text()").get()
#             h = int(str(t).split()[0])
#             # change hours to datetime
#             time = datetime.datetime.now() - datetime.timedelta(hours = h)
#
#             if time is not None:
#                 item['time'] = time.strftime("%b %d %Y %H:%M:%S")
#             else:
#                 item['time'] = None
#
#             list_item.append(item)
#
# # print(list_item)
#
#
# @app.route('/')
# def home():
#     return render_template('index.html', list_item=list_item)
#
