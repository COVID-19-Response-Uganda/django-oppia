# Generated by Django 2.2.24 on 2021-07-26 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_auto_20190321_0755'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dashboardaccesslog',
            options={'get_latest_by': ['pk']},
        ),
    ]
