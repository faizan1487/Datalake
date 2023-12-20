# Generated by Django 4.1.5 on 2023-12-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_expense_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=60),
        ),
        migrations.AlterField(
            model_name='expense',
            name='currency',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='expense',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]