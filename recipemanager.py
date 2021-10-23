import os

from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "recipedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Recipe(db.Model):
    Title = db.Column(db.String(80),nullable=False, primary_key=True)
    Ingredients = db.Column(db.String(10000),nullable=False)
    Steps = db.Column(db.String(50000),nullable=False)
    
    def __init__(self, Title, Ingredients, Steps):
        self.Title = Title
        self.Ingredients = Ingredients
        self.Steps = Steps
        

@app.route("/", methods=["GET","POST"])
def home():
    if request.form:
        recipe = Recipe(Title=request.form.get("title"), Ingredients=request.form.get("ingredients"), Steps=request.form.get("steps"))
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('show_all'))
    recipes = Recipe.query.all()
    return render_template("home.html", recipes=recipes )

@app.route("/show")
def show_all():
    return render_template("show_all.html",Rec = Recipe.query.all())

if __name__ == "__main__":
    app.run(debug=True)