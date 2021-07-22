# Generated by Django 2.2.24 on 2021-06-30 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oppia', '0039_auto_20210627_1445'),
        ('summary', '0007_dailyactiveuser_time_spent'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyactiveuser',
            name='course',
            field=models.ForeignKey(blank=True,
                                    default=None,
                                    null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    to='oppia.Course'),
        ),
    ]
