# Generated by Django 5.0.1 on 2024-01-12 07:32

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True)),
                ('rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('image', models.ImageField(upload_to='parking_lots')),
                ('open', models.TimeField()),
                ('close', models.TimeField()),
                ('multistoried', models.BooleanField(default=False)),
                ('number_of_stories', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('services_provided', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('slot_number', models.CharField(max_length=5)),
                ('status', models.BooleanField(default=False)),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.parkinglot')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSession',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, max_length=28, null=True)),
                ('timestamp_start', models.BigIntegerField()),
                ('timestamp_end', models.BigIntegerField()),
                ('slot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.slot')),
            ],
        ),
    ]
