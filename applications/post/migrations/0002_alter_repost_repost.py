# Generated by Django 4.1.7 on 2023-03-22 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repost',
            name='repost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repostsss', to='post.post'),
        ),
    ]