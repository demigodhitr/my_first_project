# Generated by Django 5.0 on 2024-01-07 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_deposit_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='not_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
