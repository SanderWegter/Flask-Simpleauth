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

#Routes
@app.route('/')
def index():
	if 'username' not in session:
		return redirect(url_for('login', message='Please log in'))
	return render_template('index.html',session=session)

@app.route('/users')
def users():
	if 'username' not in session:
		return redirect(url_for('login', message="Please log in"))
	if session['username'] != 'admin':
		return redirect(url_for('index', message="Admin only page"))

	users = Users.getUsers(db)
	if not users:
		return render_template('users.html', message="Failed to retrieve users")
	return render_template('users.html', users=users)

@app.route('/users/edit/<user>')
def editUser(user):
	return "ToDo"

@app.route('/users/delete/<user>')
def delUser(user):
	if 'username' not in session:
		return redirect(url_for('login', message="Please log in"))
	if session['username'] != 'admin':
		return redirect(url_for('index', message="Admin only page"))

	result = Users.deleteUser(db,user)
	if not result:
		return redirect(url_for('users', message="User deleted successfully"))
	return redirect(url_for('users', message="Something went wrong: "+result))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'username' in session:
		return redirect(url_for('index'))

	if request.method == 'POST':
		result = Users.loginForm(db, request.form)
		if not result:
			return redirect(url_for('index'))
		else:
			return render_template('login.html', message="Failed to log in")
	return render_template('login.html')

@app.route('/logout')
def logout():
	if 'username' not in session:
		return redirect(url_for('login'))
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'POST':
		result = Users.registerUser(db, request.form, config['pw_rounds'])
		if not result:
			return redirect(url_for('index',message='Registration successful'))
		else:
			return render_template('register.html', message="Something went wrong: "+result)
	if config['registration_enabled']:
		return render_template('register.html')
	else:
		return redirect(url_for('login', message="User registration is disabled by the admin"))

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
			port=config['server_ip'],
			debug=config['debug']
		)