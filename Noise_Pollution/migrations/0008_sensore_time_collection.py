# Generated by Django 2.2.3 on 2019-11-28 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Noise_Pollution', '0007_sensore_authenticated'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensore',
            name='time_collection',
            field=models.IntegerField(default=0),
        ),
    ]