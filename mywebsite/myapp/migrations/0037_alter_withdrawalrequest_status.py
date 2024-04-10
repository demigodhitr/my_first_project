# Generated by Django 5.0 on 2024-02-10 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_alter_clientmessages_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='status',
            field=models.CharField(choices=[('Checking', 'Checking'), ('Paid', 'Paid'), ('Under review', 'Under review'), ('Failed', 'Failed'), ('pending', 'Approved, Pending')], default='Checking', max_length=30),
        ),
    ]
