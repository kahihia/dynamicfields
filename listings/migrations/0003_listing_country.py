# Generated by Django 3.2.3 on 2021-09-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20210914_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='country',
            field=models.CharField(default='ca', max_length=100),
            preserve_default=False,
        ),
    ]