from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..db import get_session
from ..crud import get_teams, get_team

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("", response_model=list)
def list_teams(session: Session = Depends(get_session)):
    return get_teams(session)


@router.get("/{team_id}")
def read_team(team_id: int, session: Session = Depends(get_session)):
    t = get_team(session, team_id)
    if not t:
        raise HTTPException(status_code=404, detail="Team not found")
    return t
