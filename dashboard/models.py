from django.db import models
from django.urls import reverse

# STATUS MODES REMARKS
# How to read the level field of status models
# 
# Level Ranges        Description
# ------------        ------------
#  info               0 - 99
#  success            100 - 199
#  warning            200 - 299
#  error              300 - 399



class Consultant(models.Model):
    """
    Represents a Consultant Firm
    """
    full_name = models.CharField(max_length=100, help_text='Official full name of the Consultant firm')
    short_name = models.CharField(max_length=100, help_text='Short common name of the Consultant firm')
    description = models.TextField(null=True, blank=True, help_text='Short description of the Consultant firm. (Optional)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name 

    def get_absolute_url(self):
        return reverse('dashboard:consultant-detail', kwargs={'pk': str(self.pk)})

class Contractor(models.Model):
    """
    Represents a Contractor Firm
    """
    full_name = models.CharField(max_length=100, help_text='Official full name of the Contractor firm')
    short_name = models.CharField(max_length=100, help_text='Short common name of the Contractor firm')
    description = models.TextField(null=True, blank=True, help_text='Short description of the Contractor firm. (Optional)')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name 

    def get_absolute_url(self):
        return reverse('dashboard:contractor-detail', kwargs={'pk': str(self.pk)})

class ConstructionType(models.Model):
    """
    Represents a construction type (Example: Building, Road, Irrigation)
    """
    title = models.CharField(max_length=100, help_text='Type of the construction. Example: Building, Highway etc..')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title 

class ProjectStatus(models.Model):
    """
    Represents status of a project
    """
    title = models.CharField(max_length=30)
    short_title = models.CharField(max_length=30)
    level = models.IntegerField()
    description = models.TextField(null=True, blank=True, help_text='Short description of the status meaning. (Optional)')

    class Meta:
        verbose_name_plural = 'Project Status'

    def __str__(self):
        return self.title 

class Project(models.Model):
    """
    Represents a Construction Project
    """
    construction_type = models.ForeignKey(ConstructionType, on_delete=models.CASCADE)
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    employer = models.CharField(max_length=100, help_text='Official full name of the Employer')
    status = models.ForeignKey(ProjectStatus, on_delete=models.CASCADE)
    full_name = models.CharField('Official Project Title', max_length=100, help_text='Official full name of the construction project')
    short_name = models.CharField('Short Unofficial Project Title', max_length=100, help_text='Short common name of the construction project')
    project_code = models.CharField('Project Code (Optional)', max_length=30, null=True, blank=True)
    description = models.TextField('Short Project Description', null=True, blank=True, help_text='Short description of the construction project. (Optional)')
    signing_date = models.DateTimeField('Agreement Signing Date', null=True, blank=True, help_text='User yyyy-mm-dd format')
    site_handover = models.DateTimeField('Site Handover Date', null=True, blank=True, help_text='User yyyy-mm-dd format')
    mobilzation_period = models.IntegerField(null=True, blank=True)
    commencement_date = models.DateTimeField('Commenecment Date', null=True, blank=True, help_text='User yyyy-mm-dd format')
    completion_date = models.DateTimeField('Intended Completion Date', null=True, blank=True, help_text='User yyyy-mm-dd format')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name 

    def get_absolute_url(self):
        return reverse('dashboard:project-detail', kwargs={'pk': str(self.pk)})

class Activity(models.Model):
    """
    Represents a work activity (Example: Earth work, concrete works, finishing works, electrical works, sanitary works ...)
    """
    title = models.CharField(max_length=100, help_text='Type of the work activity. Example: Concrete works, Electrical works, Finishing works..')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.title 


class VariationStatus(models.Model):
    """
    Represents status of a variation
    """
    title = models.CharField(max_length=30)
    short_title = models.CharField(max_length=30)
    level = models.IntegerField()
    description = models.TextField(null=True, blank=True, help_text='Short description of the status meaning. (Optional)')

    class Meta:
        verbose_name_plural = 'Variation Status'

    def __str__(self):
        return self.title 

class Variation(models.Model):
    """
    Represents a construction Variation Works
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    status = models.ForeignKey(VariationStatus, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text='Title for the variation works')
    description = models.TextField(null=True, blank=True, help_text='Short description about the variation works and/or work order. (Optional)')
    work_order = models.CharField(max_length=10, null=True, blank=True, help_text='Work order no. of the variation works. (Optional)')
    recieved_date = models.DateField(help_text='Recieved date of the variation or work order. (Use yyyy-mm-dd format)')
    recieved_letter = models.CharField('Ref. No. for recieved Order (Optional)', max_length=100, null=True, blank=True, help_text='Ref. No. for the letter containing the order recieved.')
    submitted_date = models.DateField(null=True, blank=True, help_text='Submitted date of the variation. (Use yyyy-mm-dd format)')
    submitted_letter = models.CharField('Ref. No. for submission letter (Optional)', max_length=100, null=True, blank=True, help_text='Ref. No. for the submission letter of the variation.')
    submitted_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, help_text='Submitted amount in ETB')
    approved_date = models.DateField('Approved/Rejected Date', null=True, blank=True, help_text='Approved date of the variation. (Use yyyy-mm-dd format)')
    approved_letter = models.CharField('Ref. No. for approval/rejection letter (Optional)', max_length=100, null=True, blank=True, help_text='Ref. No. for the approval or rejection letter.')
    approved_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, help_text='Approved amount in ETB')
    remark = models.TextField(null=True, blank=True, help_text='Short helpfull remarks or notes regarding the current status. (Optional)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('dashboard:variation-detail', kwargs={'pk': str(self.pk)})

class ClaimStatus(models.Model):
    """
    Represents status of a time claim
    """
    title = models.CharField(max_length=30)
    short_title = models.CharField(max_length=30)
    level = models.IntegerField()
    description = models.TextField(null=True, blank=True, help_text='Short description of the status meaning. (Optional)')

    class Meta:
        verbose_name_plural = 'Time Claim Status'

    def __str__(self):
        return self.title 

class Claim(models.Model):
    """
    Represents a construction time extension claims
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.ForeignKey(ClaimStatus, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text='Title for the Time Extension Claim')
    number = models.IntegerField('Time Claim Number')
    description = models.TextField(null=True, blank=True, help_text='Short description about the time extension and claimant arguments. (Optional)')
    submitted_date = models.DateField(null=True, blank=True, help_text='Submitted date of the time extension request. (Use yyyy-mm-dd format)')
    submitted_letter = models.CharField('Ref. No. for submission letter (Optional)', max_length=100, null=True, blank=True, help_text='Ref. No. for the submission letter of the time extension request.')
    submitted_amount = models.IntegerField('Requested Amount in Calendar Days', help_text='Submitted amount in calendar days')
    approved_date = models.DateField('Approved/Rejected Date', null=True, blank=True, help_text='Approved date of the time extension request. (Use yyyy-mm-dd format)')
    approved_letter = models.CharField('Ref. No. for approval/rejection letter (Optional)', max_length=100, null=True, blank=True, help_text='Ref. No. for the approval or rejection letter.')
    approved_amount = models.IntegerField('Approved Amount in Calendar Days', null=True, blank=True, help_text='Approved amount in calendar days')
    remark = models.TextField(null=True, blank=True, help_text='Short helpfull remarks or notes regarding the current status. (Optional)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('dashboard:claim-detail', kwargs={'pk': str(self.pk)})

