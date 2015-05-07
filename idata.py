#!/usr/bin/env python
__author__ = 'michaael'
__package__ = ''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Entry, Day, Attachment, Base

# Setup database and session so it can be used in console
engine = create_engine('sqlite:///yurp.application.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

