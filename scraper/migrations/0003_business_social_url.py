# Generated by Django 4.2.2 on 2023-07-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_business_website_alter_business_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='social_url',
            field=models.URLField(default=''),
        ),
    ]
