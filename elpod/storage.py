# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import desc, func
from sqlalchemy.orm.session import sessionmaker

Base = declarative_base()


class Storage:
    def __init__(self):
        self._engine = create_engine('sqlite:///./elpod.db', echo=False)
        Base.metadata.create_all(self._engine)

    def is_initial(self):
        session = self.__get_session()
        count = session.query(func.count(Status.status_id)).scalar()
        if count == 0:
            return True
        else:
            return False


    def __get_session(self):
        session_maker = sessionmaker(bind=self._engine)
        return session_maker()

    def add_status(self, screen_name, status_id, posted_at, text):
        session = self.__get_session()
        status = Status(screen_name=screen_name, status_id=status_id, posted_at=posted_at, text=text)
        session.add(status)
        session.commit()


    def get_latest_status_id(self, screen_name):
        session = self.__get_session()
        status = session.query(Status).filter(Status.screen_name == screen_name).order_by(
            desc(Status.posted_at)).order_by(
            desc(Status.status_id)).first()
        if status is None:
            return None
        return status.status_id

    def get_latest_status_text(self, screen_name):
        session = self.__get_session()
        status = session.query(Status).filter(Status.screen_name == screen_name).order_by(
            desc(Status.posted_at)).order_by(
            desc(Status.status_id)).first()
        if status is None:
            return None
        return status.text

    def get_all_status_text(self):
        session = self.__get_session()
        status = session.query(Status.text).all()
        if status is None:
            return None
        return [x[0] for x in status]


class Status(Base):
    __tablename__ = 'tweet'
    screen_name = Column(String, primary_key=True)
    status_id = Column(Integer, primary_key=True)
    posted_at = Column(DateTime)
    text = Column(String)
