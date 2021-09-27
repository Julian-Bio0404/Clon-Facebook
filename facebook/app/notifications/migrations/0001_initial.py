# Generated by Django 3.2.5 on 2021-09-27 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the was las modified.', verbose_name='modified at')),
                ('message', models.CharField(help_text='notification message', max_length=200)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
