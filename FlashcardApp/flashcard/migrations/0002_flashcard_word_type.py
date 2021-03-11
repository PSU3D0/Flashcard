# Generated by Django 3.1.7 on 2021-03-10 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='word_type',
            field=models.CharField(choices=[('N', 'Noun'), ('V', 'Verb'), ('A', 'Adjective')], default='N', max_length=1),
            preserve_default=False,
        ),
    ]