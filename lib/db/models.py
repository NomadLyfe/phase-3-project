from sqlalchemy import Integer, create_engine, Column, Text, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from constants import B_ROOK,B_KNIGHT,B_BISHOP,B_QUEEN,B_KING,B_BISHOP,B_KNIGHT,B_ROOK,B_PAWN,W_ROOK,W_KNIGHT,W_BISHOP,W_QUEEN,W_KING,W_BISHOP,W_KNIGHT,W_ROOK,W_PAWN,B_EMPTY,W_EMPTY

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

    id = Column(Integer(), primary_kay=True)
    username = Column(Text())

    games = relationship('Game', secondary=game_user, back_populates='users')

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    turn_count = Column(Integer())
    board_state = [[B_ROOK,B_KNIGHT,B_BISHOP,B_QUEEN,B_KING,B_BISHOP,B_KNIGHT,B_ROOK],
               [B_PAWN,B_PAWN,B_PAWN,B_PAWN,B_PAWN,B_PAWN,B_PAWN,B_PAWN],
               [W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY],
               [B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY],
               [W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY],
               [B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY,B_EMPTY,W_EMPTY],
               [W_PAWN,W_PAWN,W_PAWN,W_PAWN,W_PAWN,W_PAWN,W_PAWN,W_PAWN],
               [W_ROOK,W_KNIGHT,W_BISHOP,W_QUEEN,W_KING,W_BISHOP,W_KNIGHT,W_ROOK]]
    active_game = True
    
    users = relationship('User', secondary=game_user, back_populates='games')
