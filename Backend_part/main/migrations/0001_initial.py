# Generated by Django 4.2.2 on 2023-06-30 17:30

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(max_length=200)),
                ('rate', models.IntegerField(default=0, validators=[main.models.validate_range])),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_field', models.IntegerField(validators=[main.models.validate_range])),
                ('votes', models.IntegerField(default=0)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='main.review')),
            ],
        ),
    ]
