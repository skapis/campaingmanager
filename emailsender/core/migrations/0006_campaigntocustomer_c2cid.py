# Generated by Django 4.0.5 on 2023-02-04 11:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_campaign_options_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaigntocustomer',
            name='c2cId',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
