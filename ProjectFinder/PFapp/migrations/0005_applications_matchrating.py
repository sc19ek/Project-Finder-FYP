# Generated by Django 4.1.6 on 2023-04-19 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PFapp', '0004_applications'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='matchRating',
            field=models.IntegerField(default=0),
        ),
    ]
