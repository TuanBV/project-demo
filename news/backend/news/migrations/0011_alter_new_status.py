# Generated by Django 5.1.6 on 2025-02-20 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_alter_new_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new',
            name='status',
            field=models.CharField(choices=[('1', 'Deleted'), ('2', 'Hidden'), ('3', 'Active'), ('4', 'Save')], default='Active', max_length=10),
        ),
    ]
