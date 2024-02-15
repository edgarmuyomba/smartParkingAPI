# Generated by Django 5.0.1 on 2024-02-15 06:38

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
                ('structured', models.BooleanField(default=False)),
                ('multistoried', models.BooleanField(default=False)),
                ('number_of_stories', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('services_provided', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=28, primary_key=True, serialize=False, unique=True)),
                ('token', models.BigIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('slot_number', models.CharField(max_length=10)),
                ('latitude', models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True)),
                ('occupied', models.BooleanField(default=False)),
                ('reserved', models.BooleanField(default=False)),
                ('parking_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='core.parkinglot')),
                ('reserve_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('token', models.BigIntegerField(blank=True, null=True)),
                ('parking_lot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.parkinglot')),
                ('slot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sensor', to='core.slot')),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSession',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('timestamp_start', models.BigIntegerField()),
                ('timestamp_end', models.BigIntegerField(blank=True, null=True)),
                ('slot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.slot')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sessions', to='core.user')),
            ],
        ),
    ]
