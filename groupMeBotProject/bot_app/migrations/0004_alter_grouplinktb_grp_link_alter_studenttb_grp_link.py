# Generated by Django 4.0.3 on 2024-02-09 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_app', '0003_studenttb_year_alter_studenttb_grp_link_grouplinktb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouplinktb',
            name='grp_link',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='studenttb',
            name='grp_link',
            field=models.ForeignKey(default=None, max_length=200, on_delete=django.db.models.deletion.RESTRICT, to='bot_app.grouplinktb'),
        ),
    ]
