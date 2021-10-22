import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "recipedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Recipe(db.Model):
    Title = db.Column(db.String(80),nullable=False, primary_key=True)
    #Ingredients = db.Column(db.String(80),nullable=False)
    #Steps = db.Column(db.String(80),nullable=False)
    
    def __repr__(self):
        return "<Title: {}>".format(self.title)


@app.route("/", methods=["GET","POST"])
def home():
    if request.form:
        recipe = Recipe(Title=request.form.get("title"))
        db.session.add(recipe)
        db.session.commit()
    recipes = Recipe.query.all()
    return render_template("home.html", recipes=recipes )

if __name__ == "__main__":
    app.run(debug=True)