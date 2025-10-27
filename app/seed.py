from datetime import datetime, timedelta
from faker import Faker
from sqlmodel import select

from .models import Team, Tournament, Match

fake = Faker()


def seed_data(session):
    if session.exec(select(Team)).first():
        return

    teams = []
    for _ in range(8):
        t = Team(name=fake.city())
        session.add(t)
        teams.append(t)
    session.commit()
    for t in teams:
        session.refresh(t)

    tournaments = []
    for i in range(2):
        tr = Tournament(name=f"Cup {fake.word().title()} {i+1}")
        session.add(tr)
        tournaments.append(tr)
    session.commit()
    for tr in tournaments:
        session.refresh(tr)

    now = datetime.utcnow()
    for tr in tournaments:
        for i in range(6):
            home, away = fake.random_choices(elements=teams, length=2)
            m = Match(
                tournament_id=tr.id,
                home_team_id=home.id,
                away_team_id=away.id,
                home_score=fake.random_int(min=0, max=6),
                away_score=fake.random_int(min=0, max=6),
                played_at=now - timedelta(days=fake.random_int(min=0, max=30)),
            )
            session.add(m)
    session.commit()
