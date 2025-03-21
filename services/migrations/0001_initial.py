# Generated by Django 5.1.5 on 2025-03-06 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('offer_price', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=10, null=True)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('service_type', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('country', models.CharField(choices=[('india', 'India'), ('saudi', 'Saudi Arabia')], default='saudi', max_length=10)),
                ('tax_codes', models.CharField(choices=[('HSN', 'HSN'), ('HS', 'HS')], default='HS', max_length=10)),
                ('gst_type', models.CharField(choices=[('GST_5', '5% GST'), ('GST_12', '12% GST'), ('GST_18', '18% GST'), ('GST_28', '28% GST'), ('none', 'No Tax')], default='none', max_length=10)),
                ('gst_rate', models.DecimalField(decimal_places=2, default=15, max_digits=5)),
                ('gst_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('vat_type', models.CharField(choices=[('standard', 'Standard VAT (15%)'), ('zero_rated', 'Zero-Rated VAT (0%)'), ('exempt', 'Exempt VAT (No VAT applied)')], default='standard', max_length=20)),
                ('vat_rate', models.DecimalField(decimal_places=2, default=15, max_digits=5)),
                ('vat_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='services.category')),
            ],
        ),
    ]
