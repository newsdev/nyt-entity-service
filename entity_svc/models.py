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


class BaseModel(Model):
    active = BooleanField(default=True)
    created = DateTimeField()
    class Meta:
        database = db_engine(**db['OPTIONS'])


class Entity(BaseModel):
    id = UUIDField()
    name = CharField(max_length=255, unique=True)
    notes = TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid4())

        if not self.created:
            self.created = datetime.datetime.now()

        return super(Entity, self).save(*args, **kwargs)
