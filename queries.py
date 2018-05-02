#!venv/bin/python
getAllDocuments = 'SELECT * FROM documents'
getDocumentRevisions = 'SELECT * FROM documents WHERE title = :title'
insertDocument = "INSERT INTO documents VALUES(:title, :content, :tstamp)"
getDocumentRevision = "SELECT * FROM documents WHERE title = :title AND tstamp = :tstamp"
