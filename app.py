import os

from flask import Flask
from flask import render_template
from flask import request
from flask import flash

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "recipedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = "secret"

db = SQLAlchemy(app)

class Recipe(db.Model):
    Title = db.Column(db.String(80), primary_key=True)
    Ingredients = db.Column(db.String(10000))
    Steps = db.Column(db.String(50000))
    
    def __init__(self, Title, Ingredients, Steps):
        self.Title = Title
        self.Ingredients = Ingredients
        self.Steps = Steps
        

@app.route("/", methods=['GET','POST'])
def home():
     
    if request.method == 'POST':
        title = request.form.get('title')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        title_check = Recipe.query.filter_by(Title=title).first()
        
        if ingredients == "" or steps == "" or title == "" :
                flash('Please enter all the fields !')
                
        elif title_check:
                flash('Recipe already exists !')
         
        else:
                recipe = Recipe(title, ingredients, steps)
                        
        
                db.session.add(recipe)
                db.session.commit()
                flash('Recipe was successfully added !!')
        #return redirect(url_for('show_all'))
    recipes = Recipe.query.all()
    return render_template("home.html", recipes=recipes )
    
    

@app.route("/show")
def show_all():
    return render_template("show_all.html",Rec = Recipe.query.all())

if __name__ == "__main__":
    app.run(debug=True)