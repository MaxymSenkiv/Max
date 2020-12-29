from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("postgresql://postgres:29.03.2002@localhost/musiclist", echo = True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column('id',Integer,primary_key=True)
    username = Column('name',String)
    email = Column('email',String,unique=True)
    password = Column('password',String)

class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column('id',Integer,primary_key=True)
    name = Column('name',String)
    owner_id = Column('owner_id',Integer,ForeignKey(User.id))
    songs = Column('songs',ARRAY(String))
    status = Column('status', String)