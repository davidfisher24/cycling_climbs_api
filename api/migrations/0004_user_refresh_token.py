# Generated by Django 2.2.7 on 2020-01-21 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190821_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='refresh_token',
            field=models.CharField(db_index=True, max_length=255, null=True, unique=True),
        ),
    ]
