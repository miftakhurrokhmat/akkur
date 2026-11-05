from sqlalchemy.orm import Session
from ..models.auth import User
from ..core.security import hash_password, verify_password


def create_user(db: Session, username: str, password: str,
                role: str, ref_id: int = None) -> User:
    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role,
        ref_id=ref_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter_by(username=username, aktif=True).first()
    if user and verify_password(password, user.password_hash):
        return user
    return None


def get_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter_by(username=username).first()