from sqlalchemy import Column, Integer, String
from source.database import Base


class User(Base):
    __tablename__ = 'users'

    tg_id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)

    def __init__(self, tg_id: int, token: str):
        self.tg_id = tg_id
        self.token = token
