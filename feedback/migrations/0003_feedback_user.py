# Generated by Django 4.1.5 on 2023-08-16 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0049_alter_marketing_pkr_form_financial_sponsorship_and_more'),
        ('feedback', '0002_remove_feedback_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_feedbacks', to='user.main_user'),
        ),
    ]