# Generated by Django 4.0.6 on 2022-07-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0003_products_digital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pic/'),
        ),
    ]
