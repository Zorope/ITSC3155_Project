# import modules
import os
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.static_folder = './static'
app.template_folder = './templates'

# routing

# GET / - show the user the landing page
@app.route('/')
def index():
    return render_template('index.html')

# start server at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)