# Generated by Django 4.1.4 on 2022-12-12 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_rename_author_post_post_author_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-created_at"]},
        ),
    ]
