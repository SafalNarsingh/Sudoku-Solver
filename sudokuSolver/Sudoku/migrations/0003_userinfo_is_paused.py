# Generated by Django 5.1.3 on 2025-02-17 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sudoku', '0002_rename_score_userinfo_current_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='is_paused',
            field=models.BooleanField(default=False),
        ),
    ]
