# Generated by Django 3.0.5 on 2020-04-29 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_stuff',
            field=models.BooleanField(default=False),
        ),
    ]
