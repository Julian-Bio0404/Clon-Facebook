# Generated by Django 3.2.5 on 2021-08-31 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_shared'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='shares',
            field=models.IntegerField(default=0),
        ),
    ]