from django.contrib import admin

# Import models
from .models import (Profile,
                     Consultant,
                     Contractor,
                     ConstructionType,
                     ProjectStatus,
                     Project,
                     Activity,
                     VariationStatus,
                     Variation,
                     ClaimStatus,
                     Claim, 
                     InsuranceType, 
                     InsuranceStatus,
                     Bank,
                     Insurance, 
                     Package,)

# Customize admin site header and title
admin.site.site_header = 'Orit Construction Admin'
admin.site.site_title = 'Orit Construction Admin'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contractor',)
    list_filter = ('contractor',)

@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'created_at', 'updated_at', 'id',)
    list_filter = ('created_at', 'updated_at',)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'group', 'price', 'id')
    list_filter = ('group',)

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'is_active', 'created_at', 'updated_at', 'id',)
    list_filter = ('is_active', 'created_at', 'updated_at',)

@admin.register(ConstructionType)
class ConstructionTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'group', 'id')
    list_filter = ('level', 'group',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'employer', 'consultant', 'contractor', 'construction_type', 'created_at', 'updated_at', 'id',)
    list_filter = ('consultant', 'contractor', 'construction_type', 'created_at', 'updated_at',)

@admin.register(Activity)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(VariationStatus)
class VariationStatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'group', 'id')
    list_filter = ('level', 'group',)

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'work_order', 'status', 'activity', 'received_date', 'created_at', 'updated_at', 'id')
    list_filter = ('project', 'status', 'work_order', 'received_date', 'submitted_date', 'approved_date', 'activity',)

@admin.register(ClaimStatus)
class ClaimStatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'group', 'id')
    list_filter = ('level', 'group',)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'created_at', 'updated_at', 'id')
    list_filter = ('project', 'status', 'submitted_date', 'approved_date',)

@admin.register(InsuranceType)
class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'id')

@admin.register(InsuranceStatus)
class InsuranceStatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'group', 'id',)
    list_filter = ('level', 'group',)

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'id')

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('project', 'insurance_type', 'bank', 'start_date', 'period', 'end_date', 'status',)
    list_filter = ('project', 'insurance_type', 'bank', 'status',)