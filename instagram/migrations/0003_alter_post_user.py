# Generated by Django 5.2.1 on 2025-05-08 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_alter_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
