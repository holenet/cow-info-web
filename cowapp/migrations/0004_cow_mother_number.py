# Generated by Django 2.0.4 on 2018-06-25 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cowapp', '0003_auto_20180622_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='cow',
            name='mother_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
