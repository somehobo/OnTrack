from mongoengine import Document, StringField


class User(Document):
    name = StringField()
