from random import choice as rc
from models import session, Game, User, game_user
from faker import Faker

fake = Faker()

def insert_data():
    games = [Game(username=fake.name()) for i in range(25)]
    users = [User(turn_count=rc(range(7,20))) for i in range(15)]
    #game_users = [game_user for i in range(50)]
    session.add_all(games + users)
    session.commit()
    return games, users

#def relate_one_to_many(games, users, game_users):
#    for row in game_users:
#        row.user = rc(users)
#        row.games = rc(games)

def delete_data():
    session.query(Game).delete()
    session.query(User).delete()
    session.commit()

if __name__ == '__main__':
    delete_data()
    games, users = insert_data()