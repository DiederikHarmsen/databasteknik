# The setup for the channel
from bottle import get, post, run, request, response
import sqlite3
import json


HOST = 'localhost'
PORT = 7007

conn = sqlite3.connect("labb3.sqlite")



def url(resource):
	return "http://{}:{}{}".format(HOST, PORT,resource)

def format_response(d):
    return json.dumps(d, indent=4) + "\n"

@get('/ping')
def get_ping():
	response.status = 200
	return "pong \n"


@post('/reset')
def reset():
	c = conn.cursor()
	c.executescript(
	"""
	PRAGMA foreign_keys = OFF;
	DELETE
	FROM movies;
	DELETE
	FROM customer;
	DELETE
	FROM theater;
	DELETE
	FROM performances;
	DELETE
	FROM ticket;
	PRAGMA foreign_keys = ON;

	INSERT INTO   movies(imdb, title, year, running_time)
	VALUES ('tt5580390', 'The Shape of Water' , 2017, 123),
	('tt4975722', 'Moonlight' , 2016, 111),
	('tt1895587', 'Spotlight' , 2015, 129),
	('tt2562232', 'Birdman' , 2014, 119);

	INSERT INTO   customer(full_name, username, password)
	VALUES ('Alice', 'alice', 'dobido' ),
	('Bob', 'bob', 'whatsinaname');

	INSERT INTO   theater(theater_name, capacity)
	VALUES ('Kino', 10),
	('Sodran', 16),
	('Skandia', 100);
	"""
	)
	conn.commit()

	response.status = 200
	return "OK \n"



@get('/movies')
def get_movies():
	response.content_type = 'application/json'
	c = conn.cursor()
	params = []
	query = """SELECT imdb, title, year, running_time
		FROM movies
		WHERE 1 = 1
		"""
	if request.query.title:
		query += "AND title = ?"
		params.append(request.query.title)
	if request.query.year:
		query += "AND year = ?"
		params.append(request.query.year)
	c.execute(
		query,
		params
	)
	s = [{"imdb": imdb, "title": title, "year": year, "running_time": running_time}
		for(imdb, title, year, running_time) in c]

	response.status = 200
	return json.dumps({"data" : s}, indent= 4)

@get('/movies/<imdb>')
def get_movies	(imdb):
	response.content_type = 'application/json'
	c = conn.cursor()
	params = []
	query = """
		SELECT imdb, title, year, running_time
		FROM movies
		WHERE imdb = ?
		"""

	params.append(imdb)

	c.execute(
        query,
        params)
	s = [{"imdb": imdb, "title": title, "year": year, "running_time": running_time}
		for (imdb, title, year, running_time) in c]
	response.status = 200
	return json.dumps({"data": s}, indent=4)

@get('/performances')
def get_performances():
	c = conn.cursor()
	c.execute(
		"""
		SELECT performances_id, date, time, title, year, theater_name
		FROM performances
		INNER JOIN movies
		USING(imdb)
		INNER JOIN theater
		USING(theater_name)
		"""
	)
	s = [{"performances_id": performances_id, "date": date, "time":time, "title":title, "year":year, "theater_name":theater_name, "capacity_left":get_capacity(theater_name, performances_id) }
		for(performances_id, date, time, title, year, theater_name) in c]
	response.status = 200
	return json.dumps({"data" : s}, indent= 4)

def get_capacity(thea_name, perf_id):
	c = conn.cursor()
	query="""
		SELECT(
		SELECT capacity
		FROM theater
		WHERE theater_name = ?
		)
		-
		(
		SELECT count()
		FROM ticket
		WHERE performances_id = ?
		)
		"""
	c.execute(
	query,
	[thea_name, perf_id]
	)
	return c.fetchone()[0]

@get('/tickets')
def get_ticket():
	c = conn.cursor()
	c.execute(
		"""
		SELECT ticket_id, username, performances_id
		FROM ticket
		"""
	)
	s = [{"ticket_id": ticket_id, "username": username, "performances_id": performances_id}
		for(ticket_id, username, performances_id) in c]
	response.status = 200
	return json.dumps({"data" : s}, indent= 4)

@get('/customers')
def get_customer():
	c = conn.cursor()
	c.execute(
		"""
		SELECT full_name, password, username
		FROM customer
		"""
	)
	s = [{"full_name":full_name, "password":password, "username":username}
		for(full_name, password, username)in c]
	response.status = 200
	return json.dumps({"data" : s}, indent= 4)


@get('/customers/<username>/tickets')
def get_customer(username):
	response.content_type = 'application/json'
	c = conn.cursor()
	c.execute(
		"""
		SELECT date, time, theater_name, title, year, count(ticket_id) AS nbroftickets
		FROM customer
		INNER JOIN ticket
		USING(username)
		INNER JOIN performances
		USING(performances_id)
		INNER JOIN movies
		USING(imdb)
		INNER JOIN theater
		USING(theater_name)
		WHERE username = ?
		GROUP BY performances_id
		"""
		,[username]
	)
	s= [{"date":date, "time":time, "theater_name":theater_name, "title":title, "year":year, "nbroftickets":nbroftickets}
		for(date, time, theater_name, title, year, nbroftickets)in c]
	return format_response({"data":s})



@get('/theater')
def get_theater():
	c = conn.cursor()
	c.execute(
		"""
		SELECT theater_name, capacity
		FROM theater
		"""
	)
	s = [{"theater_name":theater_name, "capacity":capacity}
		for(theater_name, capacity)in c]
	response.status = 200
	return json.dumps({"data" : s}, indent= 4)


@post('/movies')
def post_movies():
	response.content_type = 'application/json'
	imdb = request.query.imdb
	title = request.query.title
	year = request.query.year
	running_time = request.query.running_time
	if not (imdb and title and year and running_time):
		response.status = 400
		return format_response({"error": "Missing parameter"})
	c = conn.cursor()
	c.execute(
		"""
		INSERT
		INTO   movies(imdb, title, year, running_time)
		VALUES (?, ?, ?, ?)
		""",
		[imdb, title, year, running_time]
	)
	conn.commit()
	response.status = 200

@post('/performances')
def post_performances():

	response.content_type = 'application/json'
	imdb = request.query.imdb
	theater_name = request.query.theater
	date = request.query.date
	time = request.query.time
	if not (imdb and theater_name and date and time):
		response.status = 400
		return format_response({"error": "Missing parameter"})

	c = conn.cursor()
	# c.execute(
	# 	"""
	# 	SELECT theater_name
	# 	FROM theater
	# 	"""
	# )
	# s = [{"theater_name":theater_name}
	# 	for(theater_name)in c]

	#koll= False
	#
	# for da in s:
	# 	if theater_name == da:
	# 		koll=True
	# 		continue
	#
	#
	# if koll
	# 	return "No such theater"

	#if c. < 1:
	#	response.status = 400
	#	return "No such theater\n"
#
#	c.execute(
#		"""
#		SELECT imdb
#		FROM movie
#		WHERE imdb = ?
	# 	""",
	# 	[imdb]
	# )
	#
	# if c.rowcount < 1:
	# 	response.status = 400
	# 	return "No such movie"


	c.execute(

		"""
		INSERT
		INTO   performances(imdb, theater_name, date, time, performances_id)
		VALUES (?, ?, ?, ?, lower(hex(randomblob(16))))
		""",
		[imdb, theater_name, date, time]
	)

	conn.commit()
	c.execute(
		"""
		SELECT performances_id
		FROM performances
		WHERE rowid = last_insert_rowid()
		"""
	)
	performances_id = c.fetchone()[0]

	response.status = 200
	return format_response({"performances_id": performances_id})


@post('/customers')
def post_customer():
	response.content_type = 'application/json'
	full_name = request.query.full_name
	password = request.query.password
	username = request.query.username
	if not (full_name and password and username):
		response.status = 400
		return format_response({"error": "Missing parameter"})
	c = conn.cursor()
	c.execute(
		"""
		INSERT
		INTO   customer(full_name, password, username)
		VALUES (?, ?, ?)
		""",
		[full_name, password, username]
	)
	conn.commit()
	response.status = 200

@post('/tickets')
def post_Ticket():
	response.content_type = 'application/json'

	username = request.query.user
	password = request.query.pwd
	performances_id = request.query.performance

	if not (username and password and performances_id):
		response.status = 400
		return json.dump({"error": "missing parameter"}, indent=4)
	try:
		c = conn.cursor()

		c.execute(
	        """
	        SELECT password
	        FROM customer
	        WHERE username = ?
	        """,
	        [username]

	    )
		if password != c.fetchone()[0]:
			response.status = 400
			return "Wrong password\n"


		c.execute(
	        """
	        SELECT theater_name
	        FROM   performances
	        WHERE  performances_id = ?
	        """,
	        [performances_id]
	    )

		if(get_capacity(c.fetchone()[0], performances_id) < 1):

			response.status = 400
			return json.dumps({"error": "No tickets left"}, indent=4)

		c.execute(
	        """
	        INSERT
	        INTO ticket(ticket_id, username, performances_id)
	        VALUES (lower(hex(randomblob(16))), ?, ?)
	        """,
	        [username, performances_id]
	    )

		conn.commit()

		c.execute(
	    """
	    SELECT ticket_id
	    FROM ticket
	    WHERE rowid = last_insert_rowid()

	    """
	    )

		ticket_id = c.fetchone()[0]

		response.status=200

		return json.dumps({"ticket_id": str(ticket_id)}, indent = 4)
	except:
		return "Error\n"

@post('/theater')
def post_theater():
	response.content_type = 'application/json'
	theater_name = request.query.theater_name
	capacity = request.query.capacity
	if not (theater_name and capacity):
		response.status = 400
		return format_response({"error": "Missing parameter"})
	c = conn.cursor()
	c.execute(
		"""
		INSERT
		INTO   theater(theater_name, capacity)
		VALUES (?, ?)
		""",
		[theater_name, capacity]
	)
	conn.commit()
	response.status = 200




run(host=HOST, port=PORT, debug=True)
