# Generated by Django 4.0.5 on 2023-01-28 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaigntocustomer',
            options={'verbose_name_plural': 'Campaigns2Customers'},
        ),
        migrations.AlterModelOptions(
            name='emaillog',
            options={'verbose_name_plural': 'EmailLog'},
        ),
        migrations.AlterField(
            model_name='campaign',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]