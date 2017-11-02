from django.contrib import admin

# Import models
from .models import (Consultant,
                     Contractor,
                     ProjectStatus,
                     Project,
                     VariationStatus,
                     Variation,
                     ClaimStatus,
                     Claim,)

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'created_at', 'updated_at', 'id',)
    list_filter = ('created_at', 'updated_at',)

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'is_active', 'created_at', 'updated_at', 'id',)
    list_filter = ('is_active', 'created_at', 'updated_at',)

@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'id')
    list_filter = ('level',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'employer', 'consultant', 'contractor', 'created_at', 'updated_at', 'id',)
    list_filter = ('consultant', 'contractor', 'created_at', 'updated_at',)

@admin.register(VariationStatus)
class VariationStatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'id')
    list_filter = ('level',)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'work_order', 'status', 'recieved_date', 'created_at', 'updated_at', 'id')
    list_filter = ('project', 'status', 'work_order', 'recieved_date', 'submitted_date', 'approved_date',)

@admin.register(ClaimStatus)
class ClaimStatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'id')
    list_filter = ('level',)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'project', 'status', 'created_at', 'updated_at', 'id')
    list_filter = ('project', 'status', 'submitted_date', 'approved_date',)