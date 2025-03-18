from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base for declarative models
Base = declarative_base()

# Define the model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __repr__(self):
        return f"<User(name='{self.name}', age={self.age})>"

# Create an engine to connect to the database (in memory in this example)
engine = create_engine('sqlite:///temp.db')

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Insert data
user1 = User(name='Alice', age=30)
user2 = User(name='Bob', age=25)
session.add_all([user1, user2])
session.commit()

# Query data
users = session.query(User).all()
for user in users:
    print(user)

# Query a specific user
user_alice = session.query(User).filter_by(name='Alice').first()
print(f"User Alice: {user_alice}")

# Close the session
session.close()