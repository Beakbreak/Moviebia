# Generated by Django 4.2 on 2023-04-09 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collaborative', '0020_key_movie_backdrop_path_movie_budget_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Key',
        ),
    ]