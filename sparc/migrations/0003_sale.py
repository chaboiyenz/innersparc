# Generated by Django 5.1.7 on 2025-03-31 05:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sparc', '0002_profile_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sparc.profile')),
            ],
        ),
    ]
