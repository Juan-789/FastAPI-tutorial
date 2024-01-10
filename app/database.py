from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# generates tables
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# #raw sql
# while True:  # tries to connect to host until it does
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                       password="profile_password", cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2)
#
#     my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1}]
# # Dependancy


