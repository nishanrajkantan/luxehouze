# Generated by Django 4.0.1 on 2022-06-15 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_listing_watch_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='average_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
