import sqlite3
from flask_restful import Resource, reqparse

class User:
	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect(
			'/Users/omkar/Udemy/interview_flask/venv_sec5/code/data.db')

		cursor = connection.cursor()

		select_query = "select * from users"
		output = cursor.execute(select_query)
		for row in output:
			print(row)
		print('done')

		query = "SELECT * from users where username=?"
		result = cursor.execute(query, (username,))

		row = result.fetchone()
		if row:
			user = cls(*row)
		else:
			user = None

		connection.close()
		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')

		cursor = connection.cursor()

		query = "SELECT * from users where id=?"
		result = cursor.execute(query, (_id,))

		row = next(result)
		if row:
			user = cls(*row)
		else:
			user = None

		connection.close()
		return user

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="This field cannot be left blank!"
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="This field cannot be blank!"
	)

	def post(self):
		data = UserRegister.parser.parse_args()

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		check_user_exist = "SELECT * from users where id=?"
		if User.find_by_username(data['username']):
			return {'message':'user already exists'}, 400
	
		else:
			query = "INSERT INTO users VALUES (NULL, ?, ?);"
			cursor.execute(query, (data['username'], data['password']))

			connection.commit()
			connection.close()

			return {'message':'user created succesfully'}, 201