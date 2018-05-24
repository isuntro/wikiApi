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
        # Add dummy data
        self.content1 = {'content': 'something about stars'}
        self.content2 = {'content': "something else about stars"}
        self.doc1 = self.app.post('/documents/astar', json = self.content1).json
        self.doc2 = self.app.post('/documents/astar', json = self.content2).json

    def test_document_creation(self):
        res = self.app.post('/documents/astar', json = self.content1)
        self.assertEqual(res.status_code, 201)
        self.assertIn( self.content1['content'], res.json['content'])
        res = self.app.post('/documents/1234', json = '')
        self.assertEqual(res.status_code, 400)

    def test_get_all_documents(self):
        res = self.app.get('/documents')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json['results']), 2)

    def test_get_doc_revisions(self):
        res = self.app.get('/documents/astar')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json['results']), 2)

    def test_get_latest_doc_rev(self):
        res = self.app.get('/documents/astar/latest')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['tstamp'], self.doc2['tstamp'])

    def test_get_doc_at_timestamp(self):
        res = self.app.get('/documents/astar/'+repr(self.doc1['tstamp']))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json['tstamp'], self.doc1['tstamp'])

    def tearDown(self):
        os.unlink(api.app.config['DATABASE'])
        os.close(self.db_fd)

    

if __name__ == '__main__':
    unittest.main()