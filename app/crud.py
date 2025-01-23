from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_user = models.User(username=user.username, password=user.password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()  # Rollback transaction on failure
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")
    return db_user

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    try:
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
    except Exception as e:
        db.rollback()  # Rollback transaction on failure
        raise HTTPException(status_code=500, detail=f"Error creating transaction: {str(e)}")
    return db_transaction

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    # Use pagination to avoid loading too many records at once
    return db.query(models.Transaction).offset(skip).limit(limit).all()
