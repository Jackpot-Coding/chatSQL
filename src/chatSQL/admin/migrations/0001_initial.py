# Generated by Django 5.0.4 on 2024-04-12 12:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StrutturaDatabase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tabella',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('structure', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='table', to='admin.StrutturaDatabase')),
            ],
        ),
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('field_type', models.CharField(choices=[('VARCHAR', 'VARCHAR'), ('BINARY', 'BINARY'), ('VARBINARY', 'VARBINARY'), ('TINYBLOB', 'TINYBLOB'), ('TINYTEXT', 'TINYTEXT'), ('TEXT', 'TEXT'), ('BLOB', 'BLOB'), ('MEDIUMTEXT', 'MEDIUMTEXT'), ('MEDIUMBLOB', 'MEDIUMBLOB'), ('LONGTEXT', 'LONGTEXT'), ('LONGBLOG', 'LONGBLOG'), ('ENUM', 'ENUM'), ('SET', 'SET'), ('BIT', 'BIT'), ('TINYINT', 'TINYINT'), ('BOOL', 'BOOL'), ('BOOLEAN', 'BOOLEAN'), ('SMALLINT', 'SMALLINT'), ('MEDIUMINT', 'MEDIUMINT'), ('INT', 'INT'), ('INTEGER', 'INTEGER'), ('FLOAT', 'FLOAT'), ('DOUBLE', 'DOUBLE'), ('DECIMAL', 'DECIMAL'), ('DATE', 'DATE'), ('DATETIME', 'DATETIME'), ('TIME', 'TIME'), ('YEAR', 'YEAR')], max_length=10)),
                ('description', models.TextField()),
                ('synonyms', models.JSONField(blank=True, null=True)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field', to='admin.Tabella')),
            ],
        ),
    ]