from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.dependency import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.models.application import Application
from app.core.deps import get_current_user
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


# REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# LOGIN
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
    "access_token": access_token,
    "token_type": "bearer",
    "is_admin": user.is_admin,
    "username": user.username
}


# CURRENT USER
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }
    
@router.get("/profile")
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    total_applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).count()

    return {
        "username": current_user.username,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "total_applications": total_applications
    }