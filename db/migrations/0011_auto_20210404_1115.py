# Generated by Django 3.1.6 on 2021-04-04 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0010_auto_20210404_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='channel',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]