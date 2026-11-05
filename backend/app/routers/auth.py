from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..services import auth as auth_svc
from ..core.security import create_access_token
from ..core.deps import get_current_user
from ..models.auth import User

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # admin / dosen / mahasiswa
    ref_id: int | None = None


@router.post("/login", response_model=TokenOut)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = auth_svc.authenticate(db, form.username, form.password)
    if not user:
        raise HTTPException(401, "Username/password salah")
    token = create_access_token({"sub": user.username, "role": user.role})
    return TokenOut(
        access_token=token, role=user.role, username=user.username,
    )


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {
        "id": user.id, "username": user.username,
        "role": user.role, "ref_id": user.ref_id,
    }


@router.post("/register", status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if auth_svc.get_by_username(db, data.username):
        raise HTTPException(400, "Username sudah ada")
    user = auth_svc.create_user(
        db, data.username, data.password, data.role, data.ref_id
    )
    return {"id": user.id, "username": user.username, "role": user.role}