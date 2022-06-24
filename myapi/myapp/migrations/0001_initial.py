# Generated by Django 4.0.1 on 2022-06-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.TextField(blank=True, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
                ('avg_price', models.IntegerField(blank=True, null=True)),
                ('watch_price', models.IntegerField(blank=True, null=True)),
                ('margin_difference', models.IntegerField(blank=True, null=True)),
                ('group_id', models.TextField(blank=True, null=True)),
                ('sender_id', models.TextField(blank=True, null=True)),
                ('sender_name', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('replied', models.BooleanField(default=False)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_number', models.TextField(blank=True, null=True)),
                ('group_id', models.TextField(blank=True, null=True)),
                ('message_id', models.TextField(blank=True, null=True)),
                ('listing_type', models.TextField(blank=True, null=True)),
                ('watch_price', models.IntegerField(blank=True, null=True)),
                ('watch_condition', models.TextField(blank=True, null=True)),
                ('watch_year', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('state_name', models.TextField(blank=True, null=True)),
                ('watch_brand', models.TextField(blank=True, null=True)),
                ('watch_model', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.TextField(blank=True, null=True)),
                ('sender_id', models.TextField(blank=True, null=True)),
                ('sender_name', models.TextField(blank=True, null=True)),
                ('is_reply', models.BooleanField(blank=True, null=True)),
                ('user_id', models.TextField(blank=True, null=True)),
                ('message_id', models.TextField(blank=True, null=True)),
                ('message_timestamp', models.IntegerField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('message_type', models.TextField(blank=True, null=True)),
                ('image_url', models.TextField(blank=True, null=True)),
                ('image_mimetype', models.TextField(blank=True, null=True)),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('jpeg_thumbnail', models.TextField(blank=True, null=True)),
                ('reply_message_id', models.TextField(blank=True, null=True)),
                ('reply_message_sender_id', models.TextField(blank=True, null=True)),
                ('reply_message_quote', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.TextField(blank=True, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
                ('avg_price', models.IntegerField(blank=True, null=True)),
                ('total_listings', models.IntegerField(blank=True, null=True)),
                ('name_variations', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
