# Generated by Django 3.2.9 on 2021-11-19 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('movie_id', models.IntegerField()),
                ('overview', models.TextField()),
                ('thumbnail_path', models.CharField(max_length=200)),
            ],
        ),
    ]
