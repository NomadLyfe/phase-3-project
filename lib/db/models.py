from sqlalchemy import Integer, create_engine, Column, Text, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from constants import board_state

Base = declarative_base()

engine = create_engine('sqlite:///chessdatabase.db')
Session = sessionmaker(bind=engine)
session = Session()

class GameUser(Base):
    __tablename__ = 'game_users'

    id = Column(Integer(), primary_key=True)

    user_id = Column(Integer(), ForeignKey('users.id'))
    game_id = Column(Integer(), ForeignKey('games.id'))

    game = relationship('Game', back_populates='game_users')
    user = relationship('User', back_populates='game_users')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(Text())

    game_users = relationship('GameUser', back_populates='user', cascade='all, delete-orphan')
    games = association_proxy('game_users', 'game', creator=lambda gm: GameUser(game=gm))

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    turn_count = Column(Integer())
    board_state = board_state
    active_game = True
    
    game_users = relationship('GameUser', back_populates='game', cascade='all, delete-orphan')
    users = association_proxy('game_users', 'user', creator=lambda us: GameUser(user=us))