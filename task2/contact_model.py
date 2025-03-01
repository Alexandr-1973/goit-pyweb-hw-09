from mongoengine import Document, StringField, BooleanField, IntField


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    phone = IntField(required=True, unique=True)
    delivery = StringField(required=True, choices=['sms', 'email'])
    done = BooleanField(default=False)
    meta = {"collection": "contacts"}
