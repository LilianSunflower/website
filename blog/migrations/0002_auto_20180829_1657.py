# Generated by Django 2.0 on 2018-08-29 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='blog_type',
            new_name='article_type',
        ),
    ]