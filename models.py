import collections
import datetime
import importlib
import json
import os
import re
import time
from uuid import uuid4

from peewee import *

import utils

settings = importlib.import_module('config.%s.settings' % utils.get_env())
db = settings.DATABASES['default']
db_engine = getattr(importlib.__import__(db['ENGINE'].split('.')[0]), db['ENGINE'].split('.')[1])
database = db_engine(**db['OPTIONS'])

class BaseModel(Model):
    active = BooleanField(default=True)
    created = DateTimeField()
    user_email = CharField(max_length=255, null=True)

    class Meta:
        database = database


class Entity(BaseModel):
    id = UUIDField(primary_key=True)
    name = CharField(max_length=255, unique=True)
    canonical_entity = TextField(null=True)

    def to_dict(self):
        payload = self.__dict__['_data']
        payload['notes'] = self.notes_dict()

        return payload

    def notes(self):
        return EntityNote.select().where(EntityNote.entity==str(self.id))

    def notes_dict(self):
        return [n.to_dict() for n in self.notes()]

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid4())

        if not self.created:
            self.created = datetime.datetime.now()

        return super(Entity, self).save(*args, **kwargs)

class EntityNote(BaseModel):
    id = UUIDField(primary_key=True)
    entity = UUIDField(index=True)
    note = TextField(null=True)

    def to_dict(self):
        return self.__dict__['_data']

    def entity_obj(self):
        return Entity.get(Entity.id==self.entity)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid4())

        if not self.created:
            self.created = datetime.datetime.now()

        return super(EntityNote, self).save(*args, **kwargs)
