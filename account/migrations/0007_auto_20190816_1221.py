# Generated by Django 2.1.7 on 2019-08-16 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_userhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhistory',
            name='latitude',
            field=models.FloatField(default='27.6817'),
        ),
        migrations.AlterField(
            model_name='userhistory',
            name='longitude',
            field=models.FloatField(default='85.3170'),
        ),
    ]
