# Generated by Django 3.0 on 2021-03-30 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20210329_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookorder',
            name='books',
            field=models.ManyToManyField(null=True, related_name='books', to='library.Book'),
        ),
    ]
