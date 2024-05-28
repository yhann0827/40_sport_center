from config import SQLALCHEMY_DATABASE_URI
from app import db, models
import os.path

db.create_all()
