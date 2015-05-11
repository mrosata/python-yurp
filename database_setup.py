from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, autoincrement=True, primary_key=True)
    inserted = Column(DateTime, default=datetime.utcnow())
    last_edit = Column(DateTime, default=datetime.utcnow())
    publicity = Column(String(12), nullable=False)
    author = Column(Integer, nullable=False)
    category = Column(Integer, default=0)
    title = Column(String(64), nullable=False)
    gist = Column(String(140), nullable=True)
    content = Column(String(None), nullable=False)

    # For making JSON queries
    @property
    def serialize(self):
        return {
            'id': self.id
        }


# labels, aka categories. they have no relation outside their own table
class Label(Base):
    __tablename__ = 'labels'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(String(30), nullable=True)


class Day(Base):
    __tablename__ = 'days'
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(Date, nullable=True)
    order = Column(Integer, nullable=True)
    entry_id = Column(Integer, ForeignKey('entries.id'))
    entries = relationship(Entry)


class CategoryLink(Base):
    __tablename__ = 'cat_links'
    id = Column(Integer, autoincrement=True, primary_key=True)
    label_id = Column(Integer, ForeignKey('labels.id'))
    entry_id = Column(Integer, ForeignKey('entries.id'))
    labels = relationship(Label)
    entries = relationship(Entry)

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(16),nullable=False)
    src = Column(String(32), nullable=False)
    entry_id = Column(Integer, ForeignKey('entries.id'))
    entries = relationship(Entry)


engine = create_engine('sqlite:///yurp.application.db')
Base.metadata.create_all(engine)

