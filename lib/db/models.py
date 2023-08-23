from sqlalchemy import Integer, create_engine, Column, Text, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from constants import board_state

Base = declarative_base()

engine = create_engine('sqlite:///chessdatabase.db')
Session = sessionmaker(bind=Base)
session = Session()

game_user = Table(
    'game_users',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('game_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(Text())

    games = relationship('Game', secondary=game_user, back_populates='users')

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    turn_count = Column(Integer())
    board_state = board_state
    active_game = True
    
    users = relationship('User', secondary=game_user, back_populates='games')
