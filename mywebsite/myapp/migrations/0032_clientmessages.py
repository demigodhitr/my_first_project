# Generated by Django 5.0 on 2024-01-11 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0031_alter_accountinfo_verificationstatus_alter_idme_dob_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.CharField(blank=True, max_length=150, null=True)),
                ('message', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
