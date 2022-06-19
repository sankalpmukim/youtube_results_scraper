from django.contrib import admin
from .models import ApiKey, Health


admin.site.register(ApiKey)
admin.site.register(Health)
