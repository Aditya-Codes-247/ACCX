# FastAPI Deployable API

## Description
A FastAPI-based API for handling GST queries and managing transactions.

## Features
- User Authentication
- Transaction Management
- GST Query Handling
- Ready for Deployment on Railway

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn app.main:app --reload`
4. Access the app at `http://127.0.0.1:8000`.

## Deployment
1. Build the Docker image: `docker build -t fastapi-app .`
2. Run the container: `docker run -p 8000:8000 fastapi-app`
