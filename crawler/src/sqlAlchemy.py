from sqlalchemy import *
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except:
	pass


db = create_engine('mysql://phpmyadmin:pass@db:3306/stocksvision')
db.connect_args={'auth_plugin': 'mysql_native_password'}
db.echo = False

metadata = MetaData(db)

users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('age', Integer),
    Column('password', String(50)),
)
users.create()