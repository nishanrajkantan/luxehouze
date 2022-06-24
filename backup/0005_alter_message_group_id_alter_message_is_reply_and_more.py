# Generated by Django 4.0.1 on 2022-02-08 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_message_group_id_alter_message_image_mimetype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='group_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='is_reply',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='reply_message_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='reply_message_quote',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='reply_message_sender_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='user_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
