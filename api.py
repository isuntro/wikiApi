#!envAPI/bin/python
import sqlite3
from flask import Flask, jsonify, make_response, g, request

app = Flask(__name__)
app.config.from_object(__name__)

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