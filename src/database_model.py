from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Define the base for declarative models
Base = declarative_base()


# Define the model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    job_id = Column(Integer, ForeignKey('job.id'))
    job = relationship("Job", back_populates="user")

    def __repr__(self):
        return f"<User(name='{self.name}', age={self.age})>"

class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    permission_level = Column(Integer)

    user = relationship("User", back_populates="job")