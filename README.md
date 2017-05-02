# Flask-Simpleauth
Simple mysql authentication with flask

# Installation
### Install requirements
```
apt install python-flask python-mysqldb python-bcrypt
```

### Load database
```
mysql -u USERNAME -p DATABASENAME < db.sql

example:
mysql -u root -p flask < db.sql
```

### Config
Edit the config file and save it as 'config.conf'

### Run application
```
python app.py
```

Default username/password is admin/admin

# ToDo
* Add more security
* Add editable passwords for the user / admin