# Generated by Django 5.1.6 on 2025-03-21 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0010_alter_user_company'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
