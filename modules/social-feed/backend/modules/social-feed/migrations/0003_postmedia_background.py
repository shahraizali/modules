# Generated by Django 2.2.24 on 2022-06-05 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social-feed', '0002_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='postmedia',
            name='background',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]