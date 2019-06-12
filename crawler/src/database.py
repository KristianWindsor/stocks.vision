from sqlalchemy import *
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except:
	pass
from flask_migrate import Migrate
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import os
 

Base = declarative_base()

mysqlCreds = 'mysql://phpmyadmin:pass@' + os.environ['MYSQL_HOSTNAME'] + ':3306/stocksvision'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = mysqlCreds
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(Base):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    name = Column(String(251))

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 


engine = create_engine(mysqlCreds, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)
