#!venv/bin/python
import os, api, unittest, time
import tempfile
from flask import jsonify

class testCaseAPI(unittest.TestCase):

    def setUp(self):
        self.db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
        with api.app.app_context():
            api.initDB()
        self.app = api.app.test_client()
        
        self.content1 = {'content': 'something about stars'}
        self.content2 = {'content': "something else about stars"}
        self.doc1 = self.app.post('/documents/astar', json = self.content1).json
        self.doc2 = self.app.post('/documents/astar', json = self.content2).json

    def test_document_creation(self):
        res = self.app.post('/documents/astar', json = (self.content1))
        self.assertEqual(res.status_code, 201)
        self.assertIn( self.content1['content'], res.json['content'])

    def test_getDocuments(self):
        res = self.app.get('/documents')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json['results']), 2)

    def test_getDocRevisions(self):
        res = self.app.get('/documents/astar')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json['results']), 2)

    def test_getLatestRev(self):
        res = self.app.get('/documents/astar/latest')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['tstamp'], self.doc2['tstamp'])

    def test_getDocTime(self):
        print('/documents/astar/'+repr(self.doc1['tstamp']))
        res = self.app.get('/documents/astar/'+repr(self.doc1['tstamp']))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['tstamp'], self.doc1['tstamp'])

    def tearDown(self):
        os.unlink(api.app.config['DATABASE'])
        os.close(self.db_fd)

    

if __name__ == '__main__':
    unittest.main()