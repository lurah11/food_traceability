# Generated by Django 4.0.1 on 2022-01-06 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import traceability.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('customer', models.CharField(max_length=100)),
                ('volume', models.IntegerField()),
                ('cycle_begin', models.DateField()),
                ('cycle_end', models.DateField()),
                ('qty_produced', models.IntegerField(default=0)),
                ('qty_onhold', models.IntegerField(default=0)),
                ('qty_released', models.IntegerField(default=0)),
                ('qty_delivered', models.IntegerField(default=0)),
                ('qty_diff', models.IntegerField(default=0)),
                ('traceability_date', models.DateField(blank=True, null=True)),
                ('result', models.CharField(choices=[('ok', 'ok'), ('not ok', 'not ok')], default='not ok', max_length=10)),
                ('summary', models.CharField(blank=True, max_length=1000, null=True)),
                ('report_duration', models.IntegerField(default=0)),
                ('wh_duration', models.IntegerField(default=0)),
                ('pd_duration', models.IntegerField(default=0)),
                ('qc_duration', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TraceabilityStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('wh_submit', models.BooleanField(default=False)),
                ('prd_submit', models.BooleanField(default=False)),
                ('qc_submit', models.BooleanField(default=False)),
                ('report_submit', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traceability.productinfo')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('raw material', 'raw material'), ('packaging', 'packaging')], default='raw material', max_length=20, null=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('batch_no', models.CharField(blank=True, max_length=100, null=True)),
                ('prod_date', models.DateField(blank=True, null=True)),
                ('exp_date', models.DateField(blank=True, null=True)),
                ('qty', models.FloatField(blank=True, default=0, null=True)),
                ('qc_fs', models.CharField(blank=True, default='No Note', max_length=400, null=True)),
                ('qc_halal', models.CharField(blank=True, default='No Note', max_length=400, null=True)),
                ('qcfs_atch', models.FileField(blank=True, null=True, upload_to=traceability.models.RawMaterial.upload_path_fs)),
                ('qchalal_atch', models.FileField(blank=True, null=True, upload_to=traceability.models.RawMaterial.upload_path_halal)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traceability.productinfo')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_no', models.CharField(blank=True, max_length=30, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('receiver', models.CharField(blank=True, max_length=300, null=True)),
                ('destination', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('qty', models.IntegerField(blank=True, default=0, null=True)),
                ('record', models.FileField(blank=True, null=True, upload_to=traceability.models.ProductDelivery.upload_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traceability.productinfo')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept', models.CharField(choices=[('production', 'production'), ('qc', 'qc'), ('warehouse', 'warehouse'), ('qa', 'qa')], default='production', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
