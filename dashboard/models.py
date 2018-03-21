from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contractor = models.ForeignKey(
        'Contractor',
        null=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField('Job Title', max_length=100)
    bio = models.TextField('Short Bio', null=True, blank=True)
    thumbanil = models.ImageField(upload_to='user/thumbanils/')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

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
    full_name = models.CharField(
        max_length=100,
        help_text='Official full name of the Consultant firm',
    )
    short_name = models.CharField(
        max_length=100,
        help_text='Short common name of the Consultant firm',
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text='Short description of the Consultant firm. (Optional)',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('dashboard:consultant-detail', args=[str(self.pk)])


class Package(models.Model):
    """
    Represents a Package available for subscription
    """
    title = models.CharField('Package title', max_length=100)
    level = models.IntegerField('Package level')
    group = models.IntegerField()
    duration = models.IntegerField(
        'Package duration in days',
        null=True,
        blank=True,
    )
    max_projects = models.PositiveIntegerField(
        'Max number of projects allowed',
        null=True,
        blank=True,
    )
    max_users = models.PositiveIntegerField(
        'Max number of users allowed',
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        'Package price',
        decimal_places=2,
        max_digits=2,
        default=0.0,
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Contractor(models.Model):
    """
    Represents a Contractor Firm
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    full_name = models.CharField(
        max_length=100,
        help_text='Official full name of the Contractor firm',
    )
    short_name = models.CharField(
        max_length=100,
        help_text='Short common name of the Contractor firm',
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text='Short description of the Contractor firm. (Optional)',
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('dashboard:contractor-detail', args=[str(self.pk)])

    def __str__(self):
        return self.short_name


class Subscription(models.Model):
    """
    Represents a Constractor subscription
    """
    contractor = models.OneToOneField(Contractor, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField('Start date for subscription')
    end_date = models.DateField('Expriation date for subscription')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.package in None:
            self.package = Package.objects.get(level=0)
        super(Subscription, self).save(*args, **kwargs)

    def __str__(self):
        return '{} Subscription'.format(self.contractor)


class ConstructionType(models.Model):
    """
    Represents a construction type (Example: Building, Road, Irrigation)
    """
    title = models.CharField(
        max_length=100,
        help_text='Type of the construction. Example: Building, Highway etc..',
    )
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
    group = models.IntegerField(
        null=True,
        blank=True,
        help_text='To group different status with different level, give them the same group number',
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text='Short description of the status meaning. (Optional)',
    )

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
    status = models.ForeignKey(ProjectStatus, default=1, on_delete=models.CASCADE)
    full_name = models.CharField('Official Project Title', max_length=100, help_text='Official full name of the construction project')
    short_name = models.CharField('Short Unofficial Project Title', max_length=100, help_text='Short common name of the construction project')
    project_code = models.CharField('Project Code (Optional)', max_length=30, null=True, blank=True)
    description = models.TextField('Short Project Description', null=True, blank=True, help_text='Short description of the construction project. (Optional)')
    contract_amount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, help_text='Project contract amount in ETB')
    signing_date = models.DateField('Agreement Signing Date', null=True, blank=True, help_text='User yyyy-mm-dd format')
    site_handover = models.DateField('Site Handover Date', null=True, blank=True, help_text='User yyyy-mm-dd format')
    commencement_date = models.DateField('Commenecment Date', null=True, blank=True, help_text='User yyyy-mm-dd format')
    period = models.IntegerField('Contract Period', null=True, blank=True, help_text='Project life time in calendar days')
    completion_date = models.DateField('Intended Completion Date', null=True, blank=True, help_text='User yyyy-mm-dd format')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.commencement_date and self.period:
            self.completion_date = self.commencement_date + datetime.timedelta(self.period)
        super(Project, self).save(*args, **kwargs)

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
    group = models.IntegerField(null=True, blank=True, help_text='To group different status with different level, give them the same group number')
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
    received_date = models.DateField(help_text='Received date of the variation or work order. (Use yyyy-mm-dd format)')
    received_letter = models.CharField('Ref. No. for received Order (Optional)', max_length=100, null=True, blank=True, help_text='Ref. No. for the letter containing the order received.')
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
    group = models.IntegerField(null=True, blank=True, help_text='To group different status with different level, give them the same group number')
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

class InsuranceType(models.Model):
    """
    Represents an insurance bond type (Example: Advance bond guranttee, Performance bond guranttee)
    """
    title = models.CharField(max_length=100, help_text='Type of Insurance Bong Guranttee. Example: Advance bond guranttee, Performance bond guranttee etc..')
    short_title = models.CharField(max_length=60, help_text='Shorter title for mobile responsive views')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class InsuranceStatus(models.Model):
    """
    Represents status of an insurance
    """
    title = models.CharField(max_length=30)
    short_title = models.CharField(max_length=30)
    level = models.IntegerField()
    group = models.IntegerField(null=True, blank=True, help_text='To group different status with different level, give them the same group number')
    description = models.TextField(null=True, blank=True, help_text='Short description of the status meaning. (Optional)')

    class Meta:
        verbose_name_plural = 'Insurance Status'

    def __str__(self):
        return self.title

class Bank(models.Model):
    """
    Represents a Bank or another type of Insurance Provider firm
    """
    full_name = models.CharField(max_length=100, help_text='Full official name of the bank or insurance provider firm')
    short_name = models.CharField(max_length=100, help_text='Short (unofficial) commonly used name of the bank or insurance provider firm')
    description = models.TextField('Short description (optional)', null=True, blank=True, help_text='Short optional description about the firm')

    def __str__(self):
        return self.short_name

class Insurance(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True, help_text='Insurance amount in ETB')
    start_date = models.DateField(help_text='Starting date of this insurance. (Use yyyy-mm-dd format)')
    period = models.IntegerField(help_text='Number of calendar days covered by the insurance')
    end_date = models.DateField('Expiration date', null=True, blank=True, help_text='Expiration date of this insurance. (Use yyyy-mm-dd format)')
    status = models.ForeignKey(InsuranceStatus, on_delete=models.CASCADE)
    issue_number = models.IntegerField('Number of revision', null=True, blank=True, help_text='If unsure, please leave it blank')
    description = models.TextField('Note (optional)', null=True, blank=True, help_text='Optional notes or remarks regarding the insruance')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.end_date = self.start_date + datetime.timedelta(self.period)
        super(Insurance, self).save(*args, **kwargs)
        self.update_status()

    def update_status(self, *args, **kwargs):
        if (self.start_date + datetime.timedelta(self.period)) <= datetime.date.today() and self.status.level == 10:
            self.status = InsuranceStatus.objects.filter(level=310)[0]
            self.save()
        if (self.start_date + datetime.timedelta(self.period)) > datetime.date.today() and self.status.level == 310:
            self.status = InsuranceStatus.objects.filter(level=10)[0]
            self.save()

    def get_days_left(self, *args, **kwargs):
        if self.end_date > datetime.date.today():
            d = self.end_date - datetime.date.today()
            return d.days

    def __str__(self):
        return '{} ({})'.format(self.project, self.insurance_type)

    def get_absolute_url(self):
        return reverse('dashboard:insurance-detail', kwargs={'pk': str(self.pk)})


