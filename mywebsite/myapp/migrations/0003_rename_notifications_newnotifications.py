# Generated by Django 5.0 on 2023-12-31 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_termsandcondition_accountinfo_notifications_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notifications',
            new_name='newNotifications',
        ),
    ]
