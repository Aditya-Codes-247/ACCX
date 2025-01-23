from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app import models, schemas, crud
from app.database import SessionLocal, engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this if you want to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI GST API!"}

# User signup route
@app.post("/signup/")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db=db, user=user)

# Get all transactions
@app.get("/transactions/")
def get_transactions(db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db)
    return transactions

# Add a new transaction
@app.post("/transactions/")
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

# Ask a GST-related query
@app.post("/ask/")
def ask_question(question: str):
    import google.generativeai as genai

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"You are an expert in Goods and Services Tax (GST). Your role is to provide clear, "
            f"professional, and actionable guidance related to GST queries. "
            f"Answer the following question in a clean, formatted manner:\n\n"
            f"Question: {question}\n\nResponse:"
        )
        response = model.generate_content([prompt])
        return {"response": response.text if response and hasattr(response, "text") else "No response"}
    except Exception as e:
        return {"error": f"Failed to process query: {e}"}
