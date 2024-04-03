from flask import Flask, jsonify, abort, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
 
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(120), nullable=False)  
    developer = db.Column(db.String(120), nullable=False)  
    year = db.Column(db.String(120), default=False)  
    console = db.Column(db.String(120), nullable=False)  
 
    def tasks_bd(self):
        return {
            'id': self.id,
            'title': self.title,
            'developer': self.developer,
            'year': self.year,
            'console': self.console
        }
 
BASE_URL = '/api/'
 
@app.route('/')
def home():
    return 'Bienvenido a mi nueva api con ORM'
 
@app.route(BASE_URL + 'tasks', methods=['POST'])
def create_task():
    if not request.json:
        abort(400, "Missing JSON body in request")
        """
    if 'title' not in request.json:
        abort(400, "Error, missing 'name' in JSON data.")
    if 'developer' not in request.json:
        abort(400, "Error, missing 'category' in JSON data.")
        """
    task = Task(title=request.json['title'], developer=request.json['developer'], year=request.json['year'], console=request.json['console'])
    db.session.add(task)  
    db.session.commit()
    return jsonify({'task': task.tasks_bd()}), 201
 
 
@app.route(BASE_URL + 'tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()  
    return jsonify({'tasks': [task.tasks_bd() for task in tasks]})
 
 
@app.route(BASE_URL + 'tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task': task.tasks_bd()})
 
 
@app.route(BASE_URL + 'tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    if not request.json:
        abort(400, "Missing JSON body in request")
    task.status = not task.status
    db.session.commit()  
    return jsonify({'task': task.tasks_bd()})  
 
#
@app.route(BASE_URL + 'tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    db.session.delete(task)  
    db.session.commit()  
    return jsonify({'result': True})  
 
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
