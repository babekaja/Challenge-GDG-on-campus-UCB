# Generated by Django 5.1.1 on 2024-10-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('mot_de_passe', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('telephone', models.CharField(max_length=20)),
                ('adresse', models.CharField(max_length=100)),
                ('sexe', models.CharField(max_length=20)),
            ],
        ),
    ]
