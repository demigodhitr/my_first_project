# Generated by Django 5.0 on 2024-01-04 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_withdrawalrequest_requestid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='RequestID',
            field=models.IntegerField(default=0),
        ),
    ]