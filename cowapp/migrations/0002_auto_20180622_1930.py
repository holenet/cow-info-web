# Generated by Django 2.0.4 on 2018-06-22 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cowapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cow',
            name='number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
