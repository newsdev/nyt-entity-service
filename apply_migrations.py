import models

from playhouse.migrate import *

"""
http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations
"""

migrator = SqliteMigrator(models.database)
migrations = {
    "Add canonical entity field to entity.": migrator.add_column('entity', 'canonical_entity', CharField(null=True)),
}

for desc, m in migrations.items():
    try:
        print(desc)
        migrate(m)
    except Exception as e:
        print("\tError: %s" % e)
