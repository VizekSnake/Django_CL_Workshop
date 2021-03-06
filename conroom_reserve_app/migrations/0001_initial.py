# Generated by Django 3.2.4 on 2021-06-19 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255, unique=True)),
                ('capacity', models.IntegerField()),
                ('projector_avaibility', models.BooleanField(default=False)),
            ],
        ),
    ]
