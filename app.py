from flask import Flask, render_template, request, jsonify, session, redirect, escape, url_for
import MySQLdb
import lib.Users as Users

app = Flask(__name__)

class ServerError(Exception):pass

class DB:
	conn = None
	
	def connect(self):
		config = {}
		execfile("config.conf",config)

		self.conn = MySQLdb.connect(
			host=config['db_host'],
			user=config['db_user'],
			passwd=config['db_pass'],
			db=config['db_data']
		)
		self.conn.autocommit(True)
		self.conn.set_character_set('utf8') 

	def query(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql,args)
		except (AttributeError, MySQLdb.OperationalError):
			self.connect()
			cursor = self.conn.cursor()
			cursor.execute(sql,args)
		return cursor

if __name__ == '__main__':
	config = {}
	execfile("config.conf",config)
	app.secret_key = config['app_key']
	db = DB()
	notifications = None

#Routes
@app.route('/')
def index():
	message = None
	global notifications
	if notifications:
		message = notifications
		notifications = None
	if 'username' not in session:
		message = {'message': 'Please log in', 'type': 'warning'}
		return redirect(url_for('login'))
	return render_template('index.html',session=session,message=message)

@app.route('/users')
def users():
	message = None
	global notifications
	if notifications:
		message = notifications
		notifications = None
	if 'username' not in session:
		notifications = {'message': 'Please log in', 'type': 'warning'}
		return redirect(url_for('login'))
	if session['username'] != 'admin':
		return redirect(url_for('index', message="Admin only page"))

	users = Users.getUsers(db)
	if not users:
		notifications = {'message': 'Failed to retrieve users', 'type': 'error'}
		return render_template('users.html', message=message)
	return render_template('users.html', users=users, message=message)

@app.route('/users/edit/<user>')
def editUser(user):
	return "ToDo"

@app.route('/users/delete/<user>')
def delUser(user):
	global notifications
	if 'username' not in session:
		notifications = {'message': 'Please log in', 'type': 'warning'}
		return redirect(url_for('login'))
	if session['username'] != 'admin':
		notifications = {'message': 'Admin only page', 'type': 'error'}
		return redirect(url_for('index'))

	result = Users.deleteUser(db,user)
	if not result:
		notifications = {'message': 'User deleted successfully', 'type': 'success'}
		return redirect(url_for('users', message="User deleted successfully"))
	notifications = {'message': 'Something went wrong: '+result, 'type': 'error'}
	return redirect(url_for('users', message="Something went wrong: "+result))

@app.route('/login', methods=['GET', 'POST'])
def login():
	message = None
	global notifications
	if notifications:
		message = notifications
		notifications = None
	if 'username' in session:
		return redirect(url_for('index'))

	if request.method == 'POST':
		result = Users.loginForm(db, request.form)
		if not result:
			notifications = {'message': 'Logged in', 'type': 'success'}
			return redirect(url_for('index'))
		else:
			message = {'message': 'Failed to log in', 'type': 'error'}
			return render_template('login.html', message=message)
	return render_template('login.html',message=message)

@app.route('/logout')
def logout():
	global notifications
	if 'username' not in session:
		return redirect(url_for('login'))
	session.pop('username', None)
	notifications = {'message': 'Logged out', 'type': 'success'}
	return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
	message = None
	global notifications
	if notifications:
		message = notifications
		notifications = None
	if request.method == 'POST':
		result = Users.registerUser(db, request.form, config['pw_rounds'])
		if not result:
			notifications = {'message': 'Registration successful', 'type': 'success'}
			if session['username'] == 'admin':
				return redirect(url_for('register'))
			else:
				return redirect(url_for('login'))
		else:
			message = {'message': 'Something went wrong: '+result, 'type': 'error'}
			return render_template('register.html', message=message)
	if config['registration_enabled']:
		return render_template('register.html')
	else:
		notifications = {'message': 'User registration is disabled by the admin', 'type': 'warning'}
		return redirect(url_for('login'))

#Run app
if __name__ == '__main__':
	if config['ssl']:
		context = (config['ssl_crt'],config['ssl_key'])
		app.run(
			host=config['server_ip'],
			port=config['server_port'],
			ssl_context=context,
			debug=config['debug']
		)
	else:
		app.run(
			host=config['server_ip'],
			port=config['server_port'],
			debug=config['debug']
		)