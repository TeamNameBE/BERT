# Generated by Django 3.1.6 on 2021-02-26 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_reminder_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='advertised',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reminder',
            name='dp_participants',
            field=models.BooleanField(default=False),
        ),
    ]
