import datetime
import os
from flask import Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from sqlalchemy import func
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from . import db
from .models import Meal, Suprise
from .forms import MealForm, MealCreateForm

suggestion = Blueprint('suggestion', __name__)

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = '\static\media'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@suggestion.route('/suggest')
def suggest():
    form = MealForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('Thanks for registering')
        return redirect(url_for('suggestion.view_suggest'))
    suggestions = Meal.query.all()
    return render_template('suggestion.html', suggestions=suggestions, form=form)


@suggestion.route('/suggest/me', methods=['GET'])
def suggest_me():
    form = MealForm(request.form)
    return render_template('suggest_me.html', form=form)


@suggestion.route('/suprise')
def suprise_me():
    random = Meal.query.order_by(func.random()).first()
    suprise = Suprise.query.filter_by(id=1).first()
    if not suprise:
        new_suprise = Suprise(meal_id=random.id)
        db.session.add(new_suprise)
        db.session.commit()
    now = datetime.datetime.now()
    difference = abs((now - suprise.last_suprise).seconds)
    if difference > 60:
        suprise.last_suprise = now
        suprise.meal_id = random.id
        db.session.commit()
    return render_template('suprise_me.html', random=suprise)


@suggestion.route('/suggest/me', methods=['POST'])
def suggest_me_post():
    ingredients = request.form.getlist('ingredients')
    cuisine = request.form.get('cuisine')
    meals = Meal.query.all()
    list = []
    dicty = {}
    for meal in meals:  # tüm yemekleri gez
        for meal_ingredients in meal.get_all_ingredients():  # tüm yemek malzemelerini gez
            for ing in ingredients:  # kendi listeni gez
                if (ing == meal_ingredients) and meal.cuisine == cuisine:
                    if meal.name in dicty.keys():
                        dicty[meal.id] = dicty[meal.id] + ', ' + meal.id
                    else:
                        dicty[meal.id] = meal.id
    for k,v in dicty.items():
        list += Meal.query.filter_by(id=v)
    return render_template('view_suggestion.html', ingredients=ingredients, cuisine=cuisine, suggestions=list)


@suggestion.route('/suggest/create')
@login_required
def suggest_create():
    form = MealCreateForm(CombinedMultiDict((request.files, request.form)))
    return render_template('suggestion_create.html', form=form)


@suggestion.route('/suggest/create', methods=['POST'])
@login_required
def suggest_create_post():
    image = request.files['image']
    name = request.form.get('name')
    raw_ingredients = request.form.getlist('ingredients')
    cuisine = request.form.get('cuisine')
    if not raw_ingredients:
        flash("No Ingredients! Please Select Some Ingredients.")
        return redirect(url_for('suggestion.suggest_create'))
    if image.filename == "":
        flash("No File Name!")
        return redirect(url_for('suggestion.suggest_create'))
    if allowed_image(image.filename):
        filename = secure_filename(image.filename)
        #image.save(os.path.join(app.root_path + app.config['IMAGE_UPLOADS'], filename)),
        image.save(os.path.join(app.root_path, 'static', 'media', filename))
        image_path = (app.config['IMAGE_UPLOADS']).replace('\\', '/') + '/' + filename
        meal = Meal.query.filter_by(name=name).first()
        if meal:
            flash('This meal already exists')
            return redirect(url_for('suggestion.suggest_create'))
        ingredients = ','.join(raw_ingredients)
        new_meal = Meal(name=name, ingredients=ingredients, cuisine=cuisine, image=image_path)
        db.session.add(new_meal)
        db.session.commit()
        return redirect(url_for('suggestion.suggest'))
    else:
        flash("That file extension is not allowed")
        return redirect(url_for('suggestion.suggest_create'))
