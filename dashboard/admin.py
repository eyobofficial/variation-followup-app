from django.contrib import admin

# Import models
from .models import (Consultant,
                     Contractor,
                     Project,
                     Status,
                     Variation,)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'created_at', 'updated_at', 'id',)
    list_filter = ('created_at', 'updated_at',)

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'is_active', 'created_at', 'updated_at', 'id',)
    list_filter = ('is_active', 'created_at', 'updated_at',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'employer', 'consultant', 'contractor', 'created_at', 'updated_at', 'id',)
    list_filter = ('consultant', 'contractor', 'created_at', 'updated_at',)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'work_order', 'status', 'recieved_date', 'created_at', 'updated_at', 'id')
    list_filter = ('project', 'status', 'work_order', 'recieved_date', 'submitted_date', 'approved_date',)