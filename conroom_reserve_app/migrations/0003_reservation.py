# Generated by Django 3.2.4 on 2021-06-19 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conroom_reserve_app', '0002_room_additional_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateField()),
                ('comment', models.TextField(null=True)),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conroom_reserve_app.room')),
            ],
            options={
                'unique_together': {('room_id', 'reservation_date')},
            },
        ),
    ]
