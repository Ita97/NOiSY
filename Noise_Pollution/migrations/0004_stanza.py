# Generated by Django 2.2.3 on 2019-10-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Noise_Pollution', '0003_sensore_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stanza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('rep', models.CharField(max_length=50)),
                ('mail', models.EmailField(max_length=254)),
            ],
        ),
    ]