# Generated by Django 4.0.5 on 2023-02-05 15:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaignId', models.UUIDField()),
                ('campaign', models.CharField(max_length=255)),
                ('customerId', models.UUIDField()),
                ('customer', models.EmailField(max_length=254)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'EmailLog',
            },
        ),
    ]