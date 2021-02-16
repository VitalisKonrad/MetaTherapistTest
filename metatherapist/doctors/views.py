from django.shortcuts import render

from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
POSTGRE_USER = 'postgres'
POSTGRE_PASSWORD = 'Guard1994'
POSTGRE_HOST = 'localhost'
# DataBase need to be created manualy
POSTGRE_DB = 'MetaPsychotherapist'

base = declarative_base()
class PsychotherapistData(base):
    # Information about Psychotherapist

    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    photo = Column(JSON)
    methods = Column(JSON)
    create_time = Column(String)
    airtable_record_id = Column(String)

engine = create_engine(f'postgresql+psycopg2://{POSTGRE_USER}:{POSTGRE_PASSWORD}@{POSTGRE_HOST}/{POSTGRE_DB}', echo = True)
doctor_id = 8
def doctor(request):
    name = None
    doc_photo = None
    methods = None
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    for name, photo, methods in session.query(PsychotherapistData.name, PsychotherapistData.photo, PsychotherapistData.methods).filter(PsychotherapistData.id == doctor_id):
        name = name
        doc_photo = (photo[0]['url'])
        methods = methods
        print (name)
    return render(request, 'index.html', {'doc_photo':doc_photo,
                                          'name':name,
                                          'methods':methods})
def get_doctors_info(doctor_id):
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    for name, photo, methods in session.query(PsychotherapistData.name, PsychotherapistData.photo, PsychotherapistData.methods).filter(PsychotherapistData.id == doctor_id):
        name = name
        doc_photo = (photo[0]['url'])
        methods = methods
    return name, doc_photo, methods
    # for item in doc_methods:
    #     for methods in item:
    #         print(x)

# for name, photo in session.query(PsychotherapistData.name, PsychotherapistData.photo).order_by(PsychotherapistData.airtable_record_id):
# for methods in session.query(PsychotherapistData.methods).order_by(PsychotherapistData.airtable_record_id):
#     methods = methods
#     for i in methods:
#         for x in i:
#             print(x)
# print(methods1)
# for name, methods, photo in session.query(PsychotherapistData.name, PsychotherapistData.methods, PsychotherapistData.photo).order_by(PsychotherapistData.airtable_record_id):

# user = session.query(PsychotherapistData.methods).filter_by(airtable_record_id=PsychotherapistData.airtable_record_id).first()
# print(user)