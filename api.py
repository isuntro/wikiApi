#!venv/bin/python
import sqlite3
from flask import Flask, jsonify, make_response, g, request
from config import app_config
from queries import *

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
def getDB():
    db = getattr(g, 'sqlite_db', None)
    if db is None:
        db = connectDB()
    return db

@app.cli.command('initDB')
def initdbCommand():
    initDB()
    print('DB Initialised')

@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': "NOT FOUND"}),404)

@app.route('/documents')
def getDocuments():
    ''' Return all documents '''
    results = getDB().execute(getAllDocuments)
    print(results.fetchall())
    return jsonify(results.fetchall())
@app.route('/documents/<string:title>')
def getDocumentRevs(title):
    ''' Return all versions of document with title '''
    results = getDB().execute(getDocumentRevisions, {"title" : title})
    return jsonify(results.fetchall())

@app.route('/documents/<string:title>/<int:timestamp>')
def getDocumentTime(title, timestamp):
    ''' Return Document with title at given timestamp '''
    if not title and not timestamp:
        abort(404)
    if timestamp > datetime.time() or len(title) < 1:
        abort(404)
    results = getDB().execute(getDocumentRevision, title, timestamp)
    if not results:
        abort(404)
    return jsonify(results.fetchall())

@app.route('/documents/<string:title>/latest')
def getDocumentLatest():
    ''' Return latest revision of document with title '''
    return 'Latest Document Revision'

@app.route('/documents/<string:title>', methods=['POST'])
def addDocument(title):
    ''' Add a new document '''
    if not request.json:
        abort(400)
    if len(title) > 50 or len(title) < 1:
        abort(400)
    document = {
        'title': title,
        'content': request.json['content'],
        'tstamp': time.time()
    }
    cur = getDB().execute(insertDocument, document)
    getDB().commit()
    return jsonify(document),201