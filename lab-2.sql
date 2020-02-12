-- SQL script to create the tables necessary for lab 1 in EDAF75.
-- MySQL version.
--
-- Creates the tables students, courses, taken_courses and
-- populates them with (simulated) data.
--
-- We disable foreign key checks temporarily so we can delete the
-- tables in arbitrary order, and so insertion is faster.

PRAGMA foreign_keys = off;

--DROP TABLES IF ALREADY EXISTS.



DROP TABLE IF EXISTS theater;
CREATE TABLE theater(
	theater_name	TEXT,
	capacity	INT,
	PRIMARY KEY (theater_name)
);


DROP TABLE IF EXISTS movie;
CREATE TABLE movie(
	imdb		TEXT,
	year		INT,
	title		TEXT,
	running_time	INT,
	PRIMARY KEY 	(IMDB)
);


DROP TABLE IF EXISTS screening;
CREATE TABLE screening(
	imdb		TEXT,
	theater_name	TEXT,
	screening_id	DEFAULT (lower(hex(randomblob(16)))),
	seats_remaining	INT,
	start_time	TIME,
	date 		DATE,
	PRIMARY KEY 	(screening_id)
	FOREIGN KEY	(imdb) REFERENCES movie(imdb),
	FOREIGN KEY 	(theater_name) REFERENCES theater(theater_name)
);
--line 46
DROP TABLE IF EXISTS customer;
CREATE TABLE customer(
	full_name	TEXT,
	password	TEXT,
	username	TEXT,
	PRIMARY KEY	(username)
);


DROP TABLE IF EXISTS ticket;
CREATE TABLE ticket(
	ticket_id	DEFAULT (lower(hex(randomblob(16)))),
	username	TEXT,
	screening_id	DEFAULT (lower(hex(randomblob(16)))),
	PRIMARY KEY	(ticket_id)
	FOREIGN KEY	(username) REFERENCES customer(username),
	FOREIGN KEY	(screening_id) REFERENCES screening(screening_id)
);
--line 65			
	
INSERT
INTO 	movie(imdb, year, title, running_time)
VALUES	('tt0050083', 1957, '12 Angry Men', 96),
	('tt7984734', 2019, 'The Lighthouse', 109),
	('tt7775622', 2018, 'Free Solo', 100),
	('tt3416742', 2014, 'What We Do In The Shadows', 86),
	('tt0167260', 2003, 'The Lord of the Rings: The Return of the King', 201);

INSERT
INTO	theater(theater_name, capacity)
VALUES	('Bergakungen', 100),
	('Hagabion', 30);


INSERT
INTO	screening(theater_name, imdb, start_time, date, screening_id)
VALUES 	('Bergakungen', 'tt0050083', '19:00', '2020-02-15', lower(hex(randomblob(16)))),
	('Hagabion', 'tt7775622', '14:14', '2020-02-20',  lower(hex(randomblob(16))));


INSERT
INTO	customer(full_name, password, username)
VALUES	('Diederik Harmsen', 'svårknäcktlösenord123', 'coolkille1996');

INSERT 
INTO	ticket(ticket_id, username, screening_id)
VALUES	(lower(hex(randomblob(16))), 'coolkille1996', "VET EJ VAD JAG SKA FÖRA IN HÄR!!");
	
