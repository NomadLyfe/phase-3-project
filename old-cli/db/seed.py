from random import choice as rc
from models import session, Game, User, HiScoreChart
from faker import Faker

fake = Faker()

def insert_data():
    games = [Game(turn_count=rc(range(4,20)), active_game=False) for i in range(150)]
    users = [User(username=fake.unique.first_name(), password=fake.word()) for i in range(50)]
    hi_score_chart = [HiScoreChart() for i in range(150)]
    session.add_all(games + users + hi_score_chart)
    session.commit()
    return games, users, hi_score_chart

def relate_one_to_many(games, users, hi_score_chart):
    for hi_score in hi_score_chart:
        hi_score.user = rc(users)
        chosen_game = rc(games)
        hi_score.game = chosen_game
        games.remove(chosen_game)
        hi_score.turn_count = chosen_game.turn_count
    session.add_all(hi_score_chart)
    session.commit()

def delete_data():
    session.query(Game).delete()
    session.query(User).delete()
    session.query(HiScoreChart).delete()
    session.commit()

if __name__ == '__main__':
    delete_data()
    games, users, hi_score_chart = insert_data()
    relate_one_to_many(games, users, hi_score_chart)