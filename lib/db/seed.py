from random import choice as rc
from models import Game, User, session, game_user
from faker import Faker

fake = Faker()

def insert_data():
    games = [Game(username=fake.name()) for i in range(25)]
    users = [User(turn_count=rc(range(7,20))) for i in range(15)]
    session.add_all(games + users)
    session.commit()
    return games, users

def delete_data():
    session.query(Game).delete()
    session.query(User).delete()
    session.commit()

if __name__ == '__main__':
    delete_data()
    games, users = insert_data()