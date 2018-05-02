#!envAPI/bin/python
import sqlite3
from flask import Flask, jsonify, make_response, g, request
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config["development"])
app.config.from_pyfile('config.py')

def connectDB():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
def initDB():
    db = getDB()
    with app.open_resource('schema.sql', mode='r') as f :
        db.cursor().executescript(f.read())
    db.commit()
@app.cli.command('initDB')
def initdbCommand():
    initDB()
    print('DB Initialised')

@app.route('/documents')
def getDocuments():
    return ''
@app.route('/documents/<string:title>')
def getDocumentRevs(title):
    return ''
@app.route('/documents/<string:title>/<int:timestamp>')
def getDocumentTime(title, timestamp):
    return ''

@app.route('/documents/<string:title>/latest')
def getDocumentLatest():
    return 'Latest Document Revision'

@app.route('/documents/<string:title>', methods=['POST'])
def addDocument(title):
    return ''