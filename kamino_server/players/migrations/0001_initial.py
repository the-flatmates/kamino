# Generated by Django 4.1 on 2022-08-24 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('elo', models.FloatField()),
                ('games_played', models.IntegerField()),
                ('games_won', models.IntegerField()),
            ],
        ),
    ]
