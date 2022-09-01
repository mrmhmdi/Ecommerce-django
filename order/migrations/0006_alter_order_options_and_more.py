# Generated by Django 4.1 on 2022-09-01 08:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-create_at',)},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='paid_amaount',
            new_name='paid_amount',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='order.order'),
        ),
    ]