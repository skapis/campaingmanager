# Generated by Django 4.0.5 on 2023-01-31 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_gender_remove_customer_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.gender'),
        ),
    ]
