# import modules
import os
from flask import Flask
from database import db
from flask import render_template
from flask import request
from flask import redirect, url_for
from database import db
from models import *

app = Flask(__name__)
app.static_folder = './static'
app.template_folder = './templates'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

# initialize the database and bind it to flask
db.init_app(app)
with app.app_context():
    db.create_all()

# routing

# GET / - show the user the landing page
@app.route('/')
@app.route('/index')
@app.route('/notes') # can delete this later if needed
def index():
    a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
    projects = db.session.query(Project).all()

    return render_template('index.html',user=a_user,user_projects=projects)

# VIEW PROJECT
@app.route('/view_project/<project_id>')
def get_project(project_id):
    a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    return render_template('view_project.html', project=my_project, user=a_user)


# ADD NEW PROJECT
@app.route('/new_project', methods=['GET','POST'])
def new_project():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['detail']
        company = request.form['company_name']
        new_record = Project(title, text, company)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
        return render_template('new_project.html', user=a_user)

# EDIT PROJECT
@app.route('/project/edit/<project_id>',methods=['GET','POST'])
def edit_project(project_id):
    if request.method == 'POST':
        title = request.form['title']
        detail = request.form['detail']
        company_name = request.form['company_name']
        project = db.session.query(Project).filter_by(id=project_id).one()
        project.title = title
        project.detail = detail
        project.company_name = company_name
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
        my_project = db.session.query(Project).filter_by(id=project_id).one()
        return render_template('new_project.html',project=my_project,user=a_user)

# DELETE PROJECT
@app.route('/project/delete/<project_id>',methods=['POST'])
def delete_project(project_id):
    my_project = db.session.query(Project).filter_by(id=project_id).one()
    db.session.delete(my_project)
    db.session.commit()

    return redirect(url_for('index'))
#Placeholder code for creating new task
@app.route('/new_task', methods=['GET','POST'])
def new_task():
    a_user = db.session.query(User).filter_by(email='ajoshy@uncc.edu').one()
    return render_template('new_task.html', user=a_user)

# start server at http://127.0.0.1:5000
app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)