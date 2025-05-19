from django.contrib import admin
from .models import ServiceCategory, ServiceType, QuoteStatus, Quote


class QuoteStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'service_type', 'status', 'created_at', 'updated_at')
    list_filter = ('service_type', 'status')
    search_fields = ('name', 'company', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')  # Add this line

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'description', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)
    
admin.site.register(Quote, QuoteStatusAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)