from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=True)
    username = db.Column(db.String(80), unique=False, nullable=True)
    level = db.Column(db.Integer)

    def __init__(self, id, first_name, last_name=None, username=None):
        self.id = id
        self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if username:
            self.username = username
        self.level = 1

    def __repr__(self):
        return '<User %r>' % self.user_name


class Topic(db.Model):
    __tablename__ = 'topics'
    name = db.Column(db.String(80), primary_key=True)
    books = db.relationship("Book", backref="name")
    courses = db.relationship("Course", backref="name")
    level = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Topic %r>' % self.name


class Book(db.Model):
    __tablename__ = 'books'
    title = db.Column(db.String(80), primary_key=True)
    authors = db.Column(db.ARRAY(db.String(80)), nullable=False)
    topic = db.Column(db.String(80), db.ForeignKey("topics.name"))
    urls = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.name


class Course(db.Model):
    __tablename__ = 'courses'
    title = db.Column(db.String(80), primary_key=True)
    topic = db.Column(db.String(80), db.ForeignKey("topics.name"))
    url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Topic %r>' % self.name
