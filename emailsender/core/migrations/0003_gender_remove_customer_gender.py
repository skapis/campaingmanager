# Generated by Django 4.0.5 on 2023-01-31 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_campaigntocustomer_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='customer',
            name='gender',
        ),
    ]