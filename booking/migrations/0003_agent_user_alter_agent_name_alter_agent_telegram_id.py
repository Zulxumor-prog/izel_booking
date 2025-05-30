# Generated by Django 5.2 on 2025-05-07 09:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_tourschedule_booking_agent_commission_booking_tour'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agent',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Ismi'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='telegram_id',
            field=models.CharField(blank=True, max_length=50, verbose_name='Telegram ID'),
        ),
    ]
