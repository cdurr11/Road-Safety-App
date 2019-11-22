from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config

MYSQL = {
    'user': Config.SQL_USER,
    'pw': Config.SQL_PASSWORD,
    'db': Config.SQL_DB,
    'host': Config.SQL_HOST,
    'port': Config.SQL_PORT,
}

address = 'mysql+pymysql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % MYSQL
engine = create_engine(address)

Base = declarative_base(engine)
Base.metadata.reflect(engine)

class alameda(Base):
    __table__ = Base.metadata.tables["Alameda"]

class san_francisco(Base):
    __table__ = Base.metadata.tables["san francisco"]

class san_mateo(Base):
    __table__ = Base.metadata.tables["san mateo"]


db_session = scoped_session(sessionmaker(bind=engine))