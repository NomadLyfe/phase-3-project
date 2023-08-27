from sqlalchemy import Integer, create_engine, Column, Text, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from constants import board_state

Base = declarative_base()

engine = create_engine('sqlite:///chessdatabase.db')
Session = sessionmaker(bind=engine)
session = Session()

class HiScoreChart(Base):
    __tablename__ = 'hi_score_chart'

    id = Column(Integer(), primary_key=True)

    user_id = Column(Integer(), ForeignKey('users.id'))
    game_id = Column(Integer(), ForeignKey('games.id'))
    turn_count = Column(Integer())

    game = relationship('Game', back_populates='hi_score_chart')
    user = relationship('User', back_populates='hi_score_chart')
    
    @property
    def username(self):
        return self.user.username

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(Text())
    password = Column(Text())

    hi_score_chart = relationship('HiScoreChart', back_populates='user', cascade='all, delete-orphan')
    games = association_proxy('hi_score_chart', 'game', creator=lambda gm: HiScoreChart(game=gm))

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    turn_count = Column(Integer())
    board_state = board_state
    active_game = True
    
    hi_score_chart = relationship('HiScoreChart', back_populates='game', cascade='all, delete-orphan')
    users = association_proxy('hi_score_chart', 'user', creator=lambda us: HiScoreChart(user=us))
