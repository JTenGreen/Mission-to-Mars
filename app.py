# Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up flask
app = Flask(__name__)

# Connect Python to Mongo via flask_pymongo
#URI is a uniform resource identifier similar to a URL
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Set up Flask routes
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Set up scraping route, it will create a "button" on our webpage app to scrape data when we press it
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# Tell flask to run
if __name__ == "__main__":
   app.run()