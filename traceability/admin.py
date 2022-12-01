from django.contrib import admin
from .models import Employee, ProductInfo, ProductDelivery, RawMaterial, TraceabilityStatus

# Register your models here.
admin.site.register(Employee)
admin.site.register(ProductInfo)
admin.site.register(ProductDelivery)
admin.site.register(RawMaterial)
admin.site.register(TraceabilityStatus)
