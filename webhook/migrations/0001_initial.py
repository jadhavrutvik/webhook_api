# Generated by Django 5.1.4 on 2024-12-25 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sender", models.CharField(max_length=50)),
                ("receiver", models.CharField(max_length=20)),
                ("content", models.TextField()),
                ("status", models.CharField(max_length=20)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("mobile_no", models.CharField(max_length=20, null=True)),
            ],
        ),
    ]
