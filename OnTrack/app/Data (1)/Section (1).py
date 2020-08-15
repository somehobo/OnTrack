# This is the definition for the Section data object.  This says how the
# data is to be stored in and retrieved from the MongoDB Database.
from mongoengine import Document, StringField, IntField

class Section(Document):
    name = StringField()
    subject = StringField()
    period = IntField()
    description = StringField()
    teacher = StringField()

    meta = {
        'ordering': ['+period']
    }
