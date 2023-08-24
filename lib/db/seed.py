from random import choice as rc
import random
from models import session, Game, User, GameUser
from faker import Faker

fake = Faker()

def insert_data():
    games = [Game(turn_count=rc(range(7,20))) for i in range(25)]
    users = [User(username=fake.name()) for i in range(90)]
    game_users = [GameUser() for i in range(150)]
    session.add_all(games + users + game_users)
    session.commit()
    return games, users, game_users

def relate_one_to_many(games, users, game_users):
    for game_user in game_users:
        game_user.user = rc(users)
        game_user.game = rc(games)
    session.add_all(game_users)
    session.commit()

def delete_data():
    session.query(Game).delete()
    session.query(User).delete()
    session.query(GameUser).delete()
    session.commit()

if __name__ == '__main__':
    delete_data()
    games, users, game_users = insert_data()
    relate_one_to_many(games, users, game_users)