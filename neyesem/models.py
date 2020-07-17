from flask_login import UserMixin
from . import db
import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Meal(db.Model):
    __tablename__ = "meal"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    ingredients = db.Column(db.String(240),nullable=False)
    cuisine = db.Column(db.String(120))
    image = db.Column(db.String(120))

    def get_all_ingredients(self):
        return self.ingredients.split(',')

    def get_all_ingredients_with_comma(self):
        return self.ingredients

    def get_meal_name(self):
        return self.name

class Suprise(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    meal_id = db.Column(db.Integer(), db.ForeignKey('meal.id'))
    last_suprise = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def get_meal_name(self,meal_id):
        return Meal.query.filter_by(id=meal_id).first().get_meal_name()

    def get_meal_ingredients(self,meal_id):
        return Meal.query.filter_by(id=meal_id).first().get_all_ingredients_with_comma()


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(24), unique=True, nullable=False)
    last_visit = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
