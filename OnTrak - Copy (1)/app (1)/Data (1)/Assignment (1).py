# This is the definition for the Assignment data object.  This says how the
# data is to be stored in and retrieved from the MongoDB Database.
from .Section import Section
from mongoengine import StringField, DateTimeField, EmbeddedDocument, Document, ReferenceField, CASCADE

class Assignment(Document):
    section = ReferenceField(Section, reverse_delete_rule=CASCADE)
    name = StringField()
    duedate = DateTimeField()
    assigndate = DateTimeField()
    description = StringField()

    meta = {
        'ordering': ['+duedate']
    }
