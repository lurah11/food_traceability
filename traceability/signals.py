from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from .models import Employee, ProductInfo, ProductDelivery, RawMaterial, TraceabilityStatus

# It will activate whenever you will save file in uploadfolder model

# def getCurrentPath(id):
#
#
# @receiver(pre_save, sender=ProductDelivery)
# def file_update(sender, **kwargs):
#     print("agustampansejagat")
#     ProductDelivery_instance = kwargs['instance']
#     print(ProductDelivery_instance)
#     if ProductDelivery_instance.id:
#         getCurrentPath(id);
#         path = ProductDelivery_instance.record.path
#         if path :
#             print(path)
#             print("agus dalam path")
#             os.remove(path)
#             print(path)
