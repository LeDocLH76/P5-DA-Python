# Generated by Django 4.1.5 on 2023-02-21 09:28

from django.db import migrations
import its_app.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_myuser_email_alter_myuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='myuser',
            managers=[
                ('objects', its_app.users.models.MyUserManager()),
            ],
        ),
    ]