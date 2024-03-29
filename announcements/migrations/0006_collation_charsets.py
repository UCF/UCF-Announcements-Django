# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2022-04-08 17:14
from __future__ import unicode_literals

from django.db import migrations

def alter_collation(character_set, collation, scheme_editor):
    with scheme_editor.connection.cursor() as cursor:
        # Set collation and character set defaults for database
        print('Altering databases...')
        cursor.execute('ALTER DATABASE CHARACTER SET ' + character_set + ' COLLATE ' + collation + ';')

        # Set collation and character set for each table
        cursor.execute('SHOW TABLES;')
        for table, in cursor.fetchall():
            print('Altering table ' + table + '...')

            cursor.execute(
                'ALTER TABLE ' + table + ' CONVERT TO CHARACTER SET ' + character_set + ' COLLATE ' + collation + ';'
            )

def alter_collation_forwards(apps, schema_editor):
	'''
	Sets *collation* and *character_set* for a database and its tables.
	Also converts data in the tables if necessary.
	'''
	return alter_collation('utf8mb4', 'utf8mb4_general_ci', schema_editor)


def alter_collation_reverse(apps, schema_editor):
	return alter_collation('latin1', 'latin1_swedish_ci', schema_editor)


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0005_auto_20180322_1505'),
    ]

    operations = [
        migrations.RunPython(alter_collation_forwards, alter_collation_reverse)
    ]
