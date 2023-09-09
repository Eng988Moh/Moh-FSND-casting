import json
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    with app.app_context():
        db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # Add some initial data
    actors = [
        Actor(name='Cate Blanchett', age=52, gender='Female'),
        Actor(name='Ryan Gosling', age=41, gender='Male'),
        Actor(name='Julia Roberts', age=54, gender='Female'),
        Actor(name='Michael B. Jordan', age=34, gender='Male'),
        Actor(name='Charlize Theron', age=46, gender='Female'),
        Actor(name='Hugh Jackman', age=53, gender='Male'),
        Actor(name='Anne Hathaway', age=39, gender='Female'),
        Actor(name='Idris Elba', age=49, gender='Male'),
        Actor(name='Kate Winslet', age=46, gender='Female'),
        Actor(name='Joaquin Phoenix', age=47, gender='Male'),
        Actor(name='Emma Stone', age=33, gender='Female'),
        Actor(name='Matt Damon', age=51, gender='Male'),
        Actor(name='Amy Adams', age=47, gender='Female'),
        Actor(name='Chris Evans', age=40, gender='Male'),
        Actor(name='Viola Davis', age=56, gender='Female')
    ]
    for actor in actors:
        actor.insert()

    movies = [
        Movie(title='Carol ', release_date='2015-11-27'),
        Movie(title='Pulp Fiction', release_date='2023-07-21'),
        Movie(title='runaway bride', release_date='1999-07-30'),
        Movie(title='creed 3', release_date='2023-03-03'),
        Movie(title='atomic blonde', release_date='2017-07-26'),
        Movie(title='logan', release_date='2017-03-03'),
        Movie(title='the devil wears prada',
              release_date='2006-06-30'),
        Movie(title='the suicide squad',
              release_date='2021-07-21'),
        Movie(title='avatar 2', release_date='2022-12-16'),
        Movie(title='joker', release_date='2019-10-04'),
        Movie(title='the amazing spider-man 2', release_date='2014-05-01'),
        Movie(title='oppenheimer', release_date='2023-07-21'),
        Movie(title='Man of Steel', release_date='2013-07-14'),
        Movie(title='avengers endgame', release_date='2019-04-26'),
        Movie(title='the woman king', release_date='2022-09-16')
    ]
    for movie in movies:
        movie.insert()


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
