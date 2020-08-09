# Generated by Django 2.1.15 on 2020-07-06 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Covid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.CharField(default='', max_length=100)),
                ('Total_Cases', models.CharField(default='', max_length=200)),
                ('New_Cases', models.CharField(default='', max_length=200)),
                ('Total_Deaths', models.CharField(default='', max_length=200)),
                ('New_Deaths', models.CharField(default='', max_length=200)),
                ('Total_Recovred', models.CharField(default='', max_length=200)),
                ('New_Recovred', models.CharField(default='', max_length=200)),
                ('Eliminated_Cases', models.CharField(default='', max_length=200)),
                ('Active_Cases', models.CharField(default='', max_length=200)),
                ('Tanger_Tetouan_AlHoceima', models.CharField(default='', max_length=200)),
                ('Oriental', models.CharField(default='', max_length=200)),
                ('Fes_Meknes', models.CharField(default='', max_length=200)),
                ('Rabat_Sale_Kenitra', models.CharField(default='', max_length=200)),
                ('BeniMellal_Khenifra', models.CharField(default='', max_length=200)),
                ('Casablanca_Settat', models.CharField(default='', max_length=200)),
                ('Marrakech_Safi', models.CharField(default='', max_length=200)),
                ('Draa_Tafilalet', models.CharField(default='', max_length=200)),
                ('Sous_Massa', models.CharField(default='', max_length=200)),
                ('Guelmim_OuedNoun', models.CharField(default='', max_length=200)),
                ('Laayoune_SaguiaalHamra', models.CharField(default='', max_length=200)),
                ('EdDakhla_OuededDahab', models.CharField(default='', max_length=200)),
            ],
        ),
    ]