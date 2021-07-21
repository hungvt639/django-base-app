from django.contrib import admin
from .models.location import Provincials, Districts, Wards


admin.site.register(Provincials)
admin.site.register(Districts)
admin.site.register(Wards)

