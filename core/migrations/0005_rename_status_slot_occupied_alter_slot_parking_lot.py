# Generated by Django 5.0.1 on 2024-01-12 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20240112_1033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slot',
            old_name='status',
            new_name='occupied',
        ),
        migrations.AlterField(
            model_name='slot',
            name='parking_lot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='core.parkinglot'),
        ),
    ]
