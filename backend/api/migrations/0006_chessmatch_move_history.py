# Generated by Django 4.2.18 on 2025-04-03 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_chessmatch_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessmatch',
            name='move_history',
            field=models.JSONField(default=list),
        ),
    ]
