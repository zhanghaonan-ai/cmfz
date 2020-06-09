from django.contrib import admin

# Register your models here.
from cmfz_permission import models


admin.site.register(models.Permission)
admin.site.register(models.Role)
admin.site.register(models.User)