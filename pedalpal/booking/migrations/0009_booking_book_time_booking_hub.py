# Generated by Django 4.2.10 on 2024-03-10 06:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0008_alter_lock_cycle"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="book_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="booking",
            name="hub",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                to="booking.hub",
            ),
            preserve_default=False,
        ),
    ]
