# Generated by Django 4.1.4 on 2023-01-11 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('divulgar', '0004_alter_pet_staus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pet',
            old_name='staus',
            new_name='status',
        ),
    ]
