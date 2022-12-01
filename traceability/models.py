from django.db import models
from django.contrib.auth.models import User
import os


class Employee (models.Model):
    DEPT = [
    ('production','production'),
    ('qc','qc'),
    ('warehouse','warehouse'),
    ('qa','qa')
    ]

    user = models.ForeignKey(User,on_delete = models.CASCADE)
    dept = models.CharField(choices=DEPT, max_length=20, default = 'production')

    def __str__(self):
        return f"{self.user.username}_{self.dept}"

class ProductInfo (models.Model):
    OK = [
        ('ok','ok'),
        ('not ok', 'not ok')
    ]
    name = models.CharField(max_length=50)
    customer = models.CharField(max_length=100)
    volume = models.IntegerField()
    cycle_begin = models.DateField()
    cycle_end = models.DateField()
    qty_produced = models.IntegerField(default=0)
    qty_onhold = models.IntegerField(default=0)
    qty_released = models.IntegerField(default=0)
    qty_delivered = models.IntegerField(default=0)
    qty_diff = models.IntegerField(default=0)
    qty_stored = models.IntegerField(default=0)
    traceability_date =models.DateField(blank=True, null=True)
    result = models.CharField(choices=OK, default='not ok', max_length=10)
    summary = models.CharField(max_length=1000,blank=True, null=True)
    report_duration = models.IntegerField(default=0)
    wh_duration = models.IntegerField(default=0)
    pd_duration = models.IntegerField(default=0)
    qc_duration = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    updated = models.DateTimeField(null=True, blank = True)
    def __str__(self):
        return f"{self.name}_{self.cycle_begin}"

class ProductDelivery (models.Model):
    def upload_path(instance,filename):
        return 'traceability_{0}_{1}/Product_Delivery/{2}__{3}'.format(instance.product.name, instance.product.traceability_date, instance.id,filename)


    product = models.ForeignKey(ProductInfo,on_delete=models.CASCADE)
    shipment_no = models.CharField(max_length=30, blank = True, null=True)
    date = models.DateField(blank = True, null=True)
    receiver = models.CharField(max_length=300, blank = True, null=True)
    destination = models.CharField(max_length=100, blank = True, null=True)
    address = models.CharField(max_length=300, blank = True, null=True)
    qty = models.IntegerField(blank = True, null=True, default = 0)
    record = models.FileField(upload_to=upload_path, blank=True, null=True)
    def __str__(self):
        return f"{self.product.name}_{self.date}_{self.shipment_no}"

    # def save(self, *args, **kwargs):
    #     if ProductDelivery.objects.filter(id=self.id).exists() :
    #         product = ProductDelivery.objects.get(id=self.id)
    #         try :
    #             if self.record.path and product.record.path :
    #                 try :
    #                     productpath = product.record.path
    #                     os.remove(productpath)
    #                 except:
    #                     print("errrrorooooorrr")
    #             elif self.record.path is None and product.record.path :
    #                 self.record.path = product.record.path
    #         except :
    #             print ("Error22222")
    #     super(ProductDelivery, self).save(*args, **kwargs)

class RawMaterial (models.Model):
    def upload_path_halal(instance,filename):
        return 'traceability_{0}_{1}/qc_halal/{2}__{3}'.format(instance.product.name, instance.product.traceability_date, instance.id,filename)

    def upload_path_fs(instance,filename):
        return 'traceability_{0}_{1}/qc_food_safety/{2}__{3}'.format(instance.product.name, instance.product.traceability_date, instance.id,filename)

    RM_TYPE = [
        ('raw material','raw material'),
        ('packaging','packaging')
    ]
    OK = [
        ('ok','ok'),
        ('not ok', 'not ok')
    ]
    product = models.ForeignKey(ProductInfo,on_delete=models.CASCADE)
    type = models.CharField(blank = True , null = True , choices=RM_TYPE, max_length=20, default='raw material')
    code = models.CharField(blank = True, null = True, max_length=50)
    batch_no = models.CharField(max_length = 100, blank=True, null=True)
    prod_date = models.DateField(blank=True,null=True)
    exp_date = models.DateField(blank=True,null=True)
    qty = models.FloatField(blank=True,null=True, default = 0 )
    qc_fs = models.CharField( default='No Note', max_length=400, blank=True,null=True)
    qc_halal = models.CharField(default='No Note', max_length=400, blank=True, null=True)
    qcfs_atch = models.FileField(blank=True, null=True, upload_to=upload_path_fs)
    qchalal_atch = models.FileField(blank=True,null=True, upload_to=upload_path_halal)
    def __str__(self):
        return f"{self.code}_{self.product.name}"
    # def save(self, *args, **kwargs):
    #     if RawMaterial.objects.filter(id=self.id).exists() :
    #         rawmat = RawMaterial.objects.get(id=self.id)
    #         try :
    #             if self.qcfs_atch.path and self.qchalal_atch.path :
    #                 if rawmat.qcfs_atch.path :
    #                     try :
    #                         os.remove(rawmat.qcfs_atch.path)
    #                     except :
    #                         print("error removing existing qcfs path")
    #                 elif rawmat.qchalal_atch.path:
    #                     try :
    #                         os.remove(rawmat.qchalal_atch.path)
    #                     except :
    #                         print("error removing existing qchalal path")
    #             elif self.qcfs_atch.path is None and self.qchalal_atch.path :
    #                 if rawmat.qcfs_atch.path :
    #                     self.qcfs_atch.path = rawmat.qcfs_atch.path
    #                 elif rawmat.qchalal_atch.path :
    #                     try :
    #                         os.remove(rawmat.qchalal_atch.path)
    #                     except :
    #                         print("error removing existing qchalal path 2")
    #             elif self.qcfs_atch.path and self.qchalal_atch.path is None :
    #                 if rawmat.qchalal_atch.path :
    #                     self.qchalal_atch.path = rawmat.qchalal_atch.path
    #                 elif rawmat.qcfs_atch.path :
    #                     try :
    #                         os.remove(rawmat.qcfs_atch.path)
    #                     except :
    #                         print("error removing existing qcfs path 2")
    #             else :
    #                 if rawmat.qchalal_atch.path :
    #                     self.qchalal_atch.path = rawmat.qchalal_atch.path
    #                 else :
    #                     self.qcfs_atch.path = rawmat.qcfs_atch.path
    #         except :
    #             print ("Errortriliilii")
    #     super(RawMaterial, self).save(*args, **kwargs)

class TraceabilityStatus(models.Model):
    product = models.ForeignKey(ProductInfo,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    wh_submit = models.BooleanField(default=False)
    prd_submit = models.BooleanField(default=False)
    qc_submit = models.BooleanField(default=False)
    report_submit = models.BooleanField(default=False)
