# Generated by Django 4.0.4 on 2022-04-12 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_message_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('review', 'review'), ('blocked', 'blocked'), ('correct', 'correct')], default='review', max_length=10),
        ),
    ]