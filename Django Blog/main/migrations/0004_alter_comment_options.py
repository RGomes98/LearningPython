# Generated by Django 4.1.4 on 2022-12-15 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_post_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={"ordering": ["-created_at"]},
        ),
    ]