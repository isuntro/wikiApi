#!venv/bin/python
import sqlite3
from flask import Flask, jsonify, make_response, g, request, abort
import time
from config import app_config
from queries import *

app = Flask(__name__)
app.config.from_object(app_config["development"])
app.config.from_pyfile('config.py')

def createApp(config):
    ''' Create App from config '''
    app = Flask(__name__)
    app.config.from_object(app_config[config])
    app.config.from_pyfile('config.py')
    return app

def connectDB():
    ''' Create db connection '''
    rv = sqlite3.connect(app.config['DATABASE'])
    # rv.row_factory = sqlite3.Row
    return rv

def getDB():
    ''' Get DB conection from g or create it '''
    db = getattr(g, 'sqlite_db', None)
    if db is None:
        db = connectDB()
    return db
    
def initDB():
    '''Initiate DB from schema'''
    db = getDB()
    with app.open_resource('schema.sql', mode='r') as f :
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initDB')
def initdbCommand():
    initDB()
    print('DB Initialised')

@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': "NOT FOUND"}),404)
@app.errorhandler(400)
def badRequeset(error):
    return make_response(jsonify({'error': "BAD REQUEST"}),400)
@app.route('/documents')
def getDocuments():
    ''' Return all documents '''
    results = getDB().execute(getAllDocuments)
    results = results.fetchall()
    res = []
    if not results:
        abort(404)
    for row in results:
        obj = makeDict(row)
        res.append(obj)
    return jsonify(results = res),200

@app.route('/documents/<string:title>')
def getDocumentRevs(title):
    ''' Return all versions of a document with title '''
    if not isinstance(title, str):
        abort(400)
    results = getDB().execute(getDocumentRevisions, {"title" : title})
    results = results.fetchall()
    if not results:
        abort(404)
    res = []
    for row in results:
        obj = makeDict(row)
        res.append(obj)
    return jsonify(results = res),200

@app.route('/documents/<string:title>/<float:timestamp>')
def getDocumentTime(title, timestamp):
    ''' Return Document with title at given timestamp '''
    if not isinstance(timestamp, float):
        abort(400)
    if timestamp > time.time():
        abort(400)
    results = getDB().execute(getDocumentRevision, {'title': title, 'tstamp': timestamp })
    results = results.fetchone()
    if not results:
        abort(404)
    res = makeDict(results)
    return jsonify(res),200

@app.route('/documents/<string:title>/latest')
def getDocumentLatest(title):
    ''' Return latest revision of document with title '''
    results = getDB().execute(getDocumentRevisions, {'title': title})
    results = results.fetchall()
    if not results:
        abort(404)
    results = max(results, key=lambda x:x[2])
    res = makeDict(results)
    return jsonify(res),200

@app.route('/documents/<string:title>', methods=['POST'])
def addDocument(title):
    ''' Add a new document '''
    if not request.json :
        abort(400)
    if len(title) > 50:
        abort(400)
    document = {
        'title': title,
        'content': request.json['content'],
        'tstamp': time.time()
    }
    cur = getDB()
    with cur:
        cur.execute(insertDocument, document)
    return jsonify(document),201
    
def makeDict(result):
    obj = {
        'title': result[0],
        'content': result[1],
        'tstamp': result[2]
    }
    return obj
