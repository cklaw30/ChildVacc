# Generated by Django 5.0.1 on 2024-02-05 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_child_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalvaccine',
            name='expiry',
            field=models.DateField(null=True),
        ),
    ]