# Generated by Django 4.0 on 2022-01-10 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_user_watchlist_alter_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to='auctions.user'),
        ),
    ]
