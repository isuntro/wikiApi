DROP TABLE IF EXISTS documents;
CREATE TABLE documents (
    title char(50) not null,
    content longtext null,
    tstamp timestamp not null
);