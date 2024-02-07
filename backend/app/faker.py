from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import Message, User
from datetime import datetime, timedelta

fake = Faker()

def make_users(count=10):
    i = 0
    while i < count:
        user = User(username=fake.user_name(),
                    password='hello ant')
        db.session.add(user)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def make_messages(count=100):
    user_count = User.query.count()
    i = 0
    # start_date = datetime(2023, 1,1)    
    # end_date = datetime(2024, 1,30)
    start_date= datetime.utcnow()
    end_date=start_date - timedelta(365)
    
    while i < count:
        sender = User.query.offset(randint(0, user_count - 1)).first()
        recipient = User.query.offset(randint(0, user_count - 1)).first()
        while sender.id == recipient.id:
            recipient = User.query.offset(randint(0, user_count - 1)).first()
        message = Message(body= fake.text(),
                          To=sender, From=recipient,
                          date_created=fake.date_time_between(start_date=start_date, end_date=end_date))
        db.session.add(message)
        try:
            db.session.commit()
            i += 1
        except:
            db.session.rollback()
