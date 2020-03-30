from flask import Flask
from flask import render_template
from flask import request
import relevantRooms as rr
from htmlmaker import images_html

catalog = rr.setup()

hotwords = "cozy clean white double desk office"

app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template("index.html")

@app.route('/', methods = ['POST', 'GET'])
def index_words():
    hotwords = request.form["search_words"]
    
    url_list = rr.get_url_list(catalog, hotwords)
    
    return images_html(hotwords, url_list)