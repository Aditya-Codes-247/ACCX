from .database import Base, engine
from .models import User, Transaction

# Ensure the database tables are created
Base.metadata.create_all(bind=engine)
