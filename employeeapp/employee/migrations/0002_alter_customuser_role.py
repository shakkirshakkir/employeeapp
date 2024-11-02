# Generated by Django 5.1.2 on 2024-11-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('employee', 'Employee')], default='employee', max_length=10),
        ),
    ]