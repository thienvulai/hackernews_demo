from src.app import db


class News(db.Model):
    __tablename__ = 'News'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_id = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(1000))
    link = db.Column(db.String(1000))
    domain = db.Column(db.String(1000))
    point = db.Column(db.Integer)
    user = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)
    hide = db.Column(db.String(10))
    comment = db.Column(db.String(1000))

    def __init__(self, id_d, news_id, title, link, domain, point, user, date_created, hide, comment):
        self.id = id_d
        self.news_id = news_id
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
