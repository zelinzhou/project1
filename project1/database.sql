



CREATE TABLE user (
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL,
  password VARCHAR NOT NULL
);


CREATE TABLE book(
  isbn INT PRIMARY KEY,
  title varchar(255),
  author varchar(255),
  year int
);
