# Generated by Django 4.0.6 on 2022-08-26 10:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commented_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]