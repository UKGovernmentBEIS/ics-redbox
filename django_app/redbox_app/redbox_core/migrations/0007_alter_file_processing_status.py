# Generated by Django 5.0.6 on 2024-05-15 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redbox_core', '0006_file_core_file_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='processing_status',
            field=models.CharField(choices=[('uploaded', 'Uploaded'), ('parsing', 'Parsing'), ('chunking', 'Chunking'), ('embedding', 'Embedding'), ('indexing', 'Indexing'), ('complete', 'Complete'), ('unknown', 'Unknown')]),
        ),
    ]
