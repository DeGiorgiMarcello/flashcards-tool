from sqlalchemy import String, Boolean, Integer, Column, Sequence
from sqlalchemy.orm import declarative_base

from source.backend.db import engine
Base = declarative_base()


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    front_text = Column(String)
    back_text = Column(String)
    front_sub_text =  Column(String) 
    back_sub_text = Column(String)
    tag = Column(String)
    both_sides = Column(Boolean, default=False)


    def __repr__(self):

        return f"======\n{self.front_text}\n{self.front_sub_text}\n-----\n{self.back_text}\n{self.back_sub_text}\n====="

    def save_to_database(self, session: "Session"):
        session.add(self)
        session.commit()

    def load_from_database(self, session: "Session"):
        pass


Base.metadata.create_all(engine)
