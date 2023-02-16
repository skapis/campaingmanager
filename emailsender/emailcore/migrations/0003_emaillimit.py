# Generated by Django 4.0.5 on 2023-02-10 21:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('emailcore', '0002_alter_emaillog_options_emaillog_template_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('resetDate', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
