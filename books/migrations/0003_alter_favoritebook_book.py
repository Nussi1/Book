# Generated by Django 4.2.7 on 2023-11-20 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritebook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_books', to='books.book'),
        ),
    ]