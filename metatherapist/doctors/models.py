from django.db import models
from django.conf import settings
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, JSON
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()
class DoctorsData(base):
    # Information about Psychotherapist

    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo = Column(JSON)
    methods = Column(String)
    create_time = Column(String)
    airtable_record_id = Column(String)
