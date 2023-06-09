# Generated by Django 4.2 on 2023-04-09 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collaborative', '0019_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('public_key', models.CharField(max_length=64)),
                ('private_key', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='backdrop_path',
            field=models.TextField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='budget',
            field=models.TextField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='original_language',
            field=models.CharField(default=-1, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='overview',
            field=models.TextField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='poster_path',
            field=models.TextField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='runtime',
            field=models.FloatField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='tagline',
            field=models.TextField(default=-1, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='tmdb_title',
            field=models.TextField(default=-1, null=True),
        ),
    ]
