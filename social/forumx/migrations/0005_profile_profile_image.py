# Generated by Django 5.0.1 on 2024-01-28 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumx', '0004_alter_profile_date_modified_thread_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
