# Generated by Django 2.0 on 2018-09-10 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180907_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='read_num',
            field=models.IntegerField(default=0),
        ),
    ]
