# Generated by Django 4.2.2 on 2023-06-30 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_rate_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
