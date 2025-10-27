from typing import List
from sqlmodel import select
from sqlmodel import Session

from .models import Team, Tournament, Match


def get_teams(session: Session) -> List[Team]:
    return session.exec(select(Team)).all()


def get_team(session: Session, team_id: int) -> Team | None:
    return session.get(Team, team_id)


def get_tournaments(session: Session):
    return session.exec(select(Tournament)).all()


def get_tournament(session: Session, tournament_id: int):
    return session.get(Tournament, tournament_id)


def get_matches(session: Session):
    return session.exec(select(Match)).all()


def get_match(session: Session, match_id: int):
    return session.get(Match, match_id)


def get_matches_for_tournament(session: Session, tournament_id: int):
    stmt = select(Match).where(Match.tournament_id == tournament_id)
    return session.exec(stmt).all()
