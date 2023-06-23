from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conn_string=URL.create(drivername="mysql+mysqldb", username="root", password="Punith007#",
                       host="localhost",port=3306, database='world')

engine=create_engine(conn_string)
SessionLocal=sessionmaker(bind=engine, autoflush=False,autocommit=False)

Base=declarative_base()


def get_db():
    db=SessionLocal()
    try:
        return db
    finally:
        db.close()
