# Generated by Django 3.0.8 on 2021-02-11 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210211_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamtask',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='teamtask/%Y/%m/%d/', verbose_name='活動照片'),
        ),
    ]
