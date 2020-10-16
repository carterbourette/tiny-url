-- create our application database
create database tinyurl;

-- switch database context
use tinyurl;

-- create the url table and apply a unique index on the hash
create table url (
    hash varchar(20) not null,
    url varchar(255) not null
);
create unique index uidx_hash on url (hash);