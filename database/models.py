from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("postgresql://postgres:147896325@localhost/musiclist", echo = True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column('user_id',Integer,primary_key=True)
    name = Column('name',String)
    email = Column('email',String,unique=True)
    password = Column('password',String)

class Playlist(Base):
    __tablename__ = 'playlist'

    playlist_id = Column('playlist_id',Integer,primary_key=True)
    name = Column('name',String)
    owner_id = Column('owner_id',Integer,ForeignKey(User.user_id))
    songs = Column('songs',ARRAY(String))