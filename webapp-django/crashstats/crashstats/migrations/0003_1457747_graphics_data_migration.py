# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-25 15:42
from __future__ import print_function
from __future__ import unicode_literals

from django.db import connection, migrations


def copy_graphics_devices_data(apps, schema_editor):
    """Copy data from the old sqlalchemy/alembic graphics_device table to the Django one"""
    GraphicsDevice = apps.get_model('crashstats', 'GraphicsDevice')

    cursor = connection.cursor()

    # First, we verify the table is there, if not, we don't need to do anything
    cursor.execute("""
    SELECT relname from pg_catalog.pg_class
    WHERE relname = 'graphics_device'
    """)
    row = cursor.fetchone()
    if row is None:
        print('no graphics_device table--nothing to do', end='')
        return

    # Second, pull all the data from it
    columns = ['vendor_hex', 'adapter_hex', 'vendor_name', 'adapter_name']
    cursor.execute(
        """
        SELECT %(columns)s
        FROM graphics_device
        """ % {
            'columns': ', '.join(columns)
        }
    )

    print('')
    insert_count = 0
    skip_count = 0

    # Third, create new GraphicsDevice instances and save them to the db.
    # Looks like stage and prod have a *lot* of junk data. This is a lookup
    # table so we're going to junk anything that doesn't have names.
    for row in cursor.fetchall():
        item = dict(zip(columns, row))
        if item['vendor_name'] is None and item['adapter_name'] is None:
            print('skipping', item)
            skip_count += 1
        else:
            print('inserting', item)
            GraphicsDevice.objects.create(
                vendor_hex=item['vendor_hex'],
                adapter_hex=item['adapter_hex'],
                vendor_name=item['vendor_name'],
                adapter_name=item['adapter_name']
            )
            insert_count += 1

    print('inserted: %s' % insert_count)
    print('skipped: %s' % skip_count)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('crashstats', '0002_1457747_graphics_devices'),
    ]

    operations = [
        migrations.RunPython(copy_graphics_devices_data, noop),
    ]