# Generated by Django 4.0.1 on 2022-02-08 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_message_group_id_alter_message_is_reply_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_timestamp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
