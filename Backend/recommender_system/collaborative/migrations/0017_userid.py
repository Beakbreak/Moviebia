# Generated by Django 4.1.7 on 2023-04-01 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborative', '0016_suggestion_suggestion_35'),
    ]

    operations = [
        migrations.CreateModel(
            name='userid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('userId', models.IntegerField()),
            ],
        ),
    ]
