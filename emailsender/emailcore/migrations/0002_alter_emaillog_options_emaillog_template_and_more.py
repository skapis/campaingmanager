# Generated by Django 4.0.5 on 2023-02-07 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailcore', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emaillog',
            options={'ordering': ['-timestamp'], 'verbose_name_plural': 'EmailLog'},
        ),
        migrations.AddField(
            model_name='emaillog',
            name='template',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='emaillog',
            name='templateId',
            field=models.UUIDField(null=True),
        ),
    ]
