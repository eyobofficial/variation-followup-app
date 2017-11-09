from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Import user authentication modules
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Import Message Framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Import models
from .models import (Consultant,
                     Contractor,
                     ProjectStatus,
                     Project,
                     VariationStatus,
                     Variation,
                     ClaimStatus,
                     Claim, 
                     InsuranceType, 
                     InsuranceStatus, 
                     Bank, 
                     Insurance, )

# Import forms
from .forms import (SignupForm,)

# Check if user is committee
def check_committee(user):
    return user.profile.is_committee

# Update Insurance Status
def update_ins_status():
    for i in Insurance.objects.all():
        i.update_status()

# Signup view
def signup(request):
    """
    Register a new user, login the new user and redirect to breakdowns:index page
    """

    # Check if user already logged
    if request.user.is_authenticated:
        return redirect('dashboard:index')
        
    form_class = SignupForm
    template_name = 'registration/signup.html'

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = False
            user.profile.contractor = form.cleaned_data['contractor']
            user.save()
            messages.success(request, 'You have successfully created a new account.')
            messages.warning(request, 'Your account must be activated before you can start using it. Please contact the admin to quickly activate your account.')
            return redirect('dashboard:index')
    else:
        form = form_class()
    return render(request, template_name, {
            'form': form,
        })

@login_required
def index(request):
    return render(request, 'dashboard/index.html', {
            'page_name': 'dashboard',
        })

class ProjectList(UserPassesTestMixin, generic.ListView):
    """
    List all projects for a particular contractor
    """
    model = Project

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active

    def get_queryset(self, *args, **kwargs):
        return Project.objects.filter(contractor=self.request.user.profile.contractor)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectDetail(UserPassesTestMixin, generic.DetailView):
    """
    Detail for a particular variation record
    """
    model = Project

    def test_func(self, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return self.request.user.is_active and project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDetail, self).get_context_data(*args, **kwargs)
        context['all_variation_list'] = Variation.objects.filter(project=self.kwargs['pk']).order_by('-updated_at')
        context['under_prep_variation_list'] = Variation.objects.filter(project=self.kwargs['pk']).filter(status__group=1).order_by('-updated_at')
        context['pending_variation_list'] = Variation.objects.filter(project=self.kwargs['pk']).filter(status__group=2).order_by('-updated_at')
        context['submitted_variation_list'] = Variation.objects.filter(project=self.kwargs['pk']).filter(status__group=3).order_by('-updated_at')
        context['approved_variation_list'] = Variation.objects.filter(project=self.kwargs['pk']).filter(status__group=4).order_by('-updated_at')

        context['all_claim_list'] = Claim.objects.filter(project=self.kwargs['pk']).order_by('-updated_at')
        context['submitted_claim_list'] = Claim.objects.filter(project=self.kwargs['pk']).filter(status__group=3).order_by('-updated_at')
        context['approved_claim_list'] = Claim.objects.filter(project=self.kwargs['pk']).filter(status__group=4).order_by('-updated_at')
        context['page_name'] = 'projects'
        return context

class ProjectCreate(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Create a new project record
    """
    model = Project
    fields = ('construction_type', 'consultant', 'employer', 'full_name', 'short_name', 'status', 'description', )
    success_message = 'New project created successfully.'

    def form_valid(self, form, *args, **kwargs):
        form.instance.contractor = self.request.user.profile.contractor
        return super(ProjectCreate, self).form_valid(form, *args, **kwargs)

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active and self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectUpdate(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update a particular project record
    """
    model = Project
    fields = ('construction_type', 'consultant', 'employer', 'full_name', 'short_name', 'status', 'description', )
    success_message = 'Project updated created successfully.'

    def test_func(self, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return self.request.user.is_active and self.request.user.is_staff and project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectDelete(UserPassesTestMixin, DeleteView):
    """
    Delete a particular a project record
    """
    model = Project
    success_url = '/dashboard/projects/'
    success_message = 'A project is deleted successfully.'

    def test_func(self, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return self.request.user.is_active and self.request.user.is_staff and project.contractor == self.request.user.profile.contractor

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProjectDelete, self).delete(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectVariationDetail(UserPassesTestMixin, generic.DetailView):
    """
    Detail for a particular variation record
    """
    model = Variation
    template_name = 'dashboard/project_variation_detail.html'

    def test_func(self, *args, **kwargs):
        variation = get_object_or_404(Variation, pk=self.kwargs['pk'])
        return self.request.user.is_active and variation.project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectVariationDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectVariationCreate(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Create a new variation record for current project
    """
    model = Variation
    fields = ('title', 'work_order', 'activity', 'description', 'status', 'recieved_date', 'recieved_letter', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    template_name = 'dashboard/project_variation_form.html'
    success_message = 'New variation created successfully.'

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active and self.request.user.is_staff

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:project-variation-detail', kwargs={'pk': str(self.object.id)})

    def form_valid(self, form, *args, **kwargs):
        form.instance.project = Project.objects.get(pk=self.kwargs['project_pk'])
        return super(ProjectVariationCreate, self).form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectVariationCreate, self).get_context_data(*args, **kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        context['page_name'] = 'projects'
        return context

class ProjectVariationUpdate(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update a particular variation record for the current project
    """
    model = Variation
    fields = ('title', 'work_order', 'activity', 'description', 'status', 'recieved_date', 'recieved_letter', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    template_name = 'dashboard/project_variation_form.html'
    success_message = 'Variation updated successfully.'

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active and self.request.user.is_staff

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:project-variation-detail', kwargs={'pk': str(self.object.id)})

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectVariationUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectVariationDelete(UserPassesTestMixin, DeleteView):
    """
    Delete a particular a variation record from the current project
    """
    model = Variation
    template_name = 'dashboard/project_variation_confirm_delete.html'
    success_message = 'Variation deleted successfully.'

    def test_func(self, *args, **kwargs):
        variation = get_object_or_404(Variation, pk=self.kwargs['pk'])
        return self.request.user.is_active and self.request.user.is_staff and variation.project.contractor == self.request.user.profile.contractor
    
    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:project-detail', kwargs={'pk': str(self.kwargs['project_pk'])})

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProjectVariationDelete, self).delete(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectVariationDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectClaimDetail(UserPassesTestMixin, generic.DetailView):
    """
    Detail for a particular time extension claim record of a particular project
    """
    model = Claim
    template_name = 'dashboard/project_claim_detail.html'

    def test_func(self, *args, **kwargs):
        claim = get_object_or_404(Claim, pk=self.kwargs['pk'])
        return self.request.user.is_active and claim.project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectClaimDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectClaimCreate(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Create a new time extension claim record for current project
    """
    model = Claim
    fields = ('title', 'number', 'description', 'status', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    template_name = 'dashboard/project_claim_form.html'
    success_message = 'Time claim created successfully.'

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active and self.request.user.is_staff

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:project-claim-detail', kwargs={'pk': str(self.object.id)})

    def form_valid(self, form, *args, **kwargs):
        form.instance.project = Project.objects.get(pk=self.kwargs['project_pk'])
        return super(ProjectClaimCreate, self).form_valid(form, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectClaimCreate, self).get_context_data(*args, **kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        context['page_name'] = 'projects'
        return context

class ProjectClaimUpdate(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Create a new time extension claim record for current project
    """
    model = Claim
    fields = ('title', 'number', 'description', 'status', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    template_name = 'dashboard/project_claim_form.html'
    success_message = 'Time claim created successfully.'

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active and self.request.user.is_staff

    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:project-claim-detail', kwargs={'pk': str(self.object.id)})

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectClaimUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class ProjectClaimDelete(UserPassesTestMixin, DeleteView):
    """
    Delete a particular time claim record from the current project
    """
    model = Claim
    template_name = 'dashboard/project_claim_confirm_delete.html'
    success_message = 'Time claim deleted successfully.'

    def test_func(self, *args, **kwargs):
        claim = get_object_or_404(Claim, pk=self.kwargs['pk'])
        return self.request.user.is_active and self.request.user.is_staff and claim.project.contractor == self.request.user.profile.contractor
    
    def get_success_url(self, *args, **kwargs):
        return reverse('dashboard:project-detail', kwargs={'pk': str(self.kwargs['project_pk'])})

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ProjectClaimDelete, self).delete(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectClaimDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'projects'
        return context

class VariationList(UserPassesTestMixin, generic.ListView):
    """
    Lists all variations for all project
    """
    model = Variation

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active

    def get_queryset(self, *args, **kwargs):
        return Variation.objects.filter(project__contractor=self.request.user.profile.contractor).order_by('-updated_at')

    def get_context_data(self, *args, **kwargs):
        context = super(VariationList, self).get_context_data(*args, **kwargs)
        context['under_prep_variation_list'] = Variation.objects.filter(project__contractor=self.request.user.profile.contractor).filter(status__group=1).order_by('-updated_at')
        context['pending_variation_list'] = Variation.objects.filter(project__contractor=self.request.user.profile.contractor).filter(status__group=2).order_by('-updated_at')
        context['submitted_variation_list'] = Variation.objects.filter(project__contractor=self.request.user.profile.contractor).filter(status__group=3).order_by('-updated_at')
        context['approved_variation_list'] = Variation.objects.filter(project__contractor=self.request.user.profile.contractor).filter(status__group=4).order_by('-updated_at')
        context['page_name'] = 'variations'
        return context

class VariationDetail(UserPassesTestMixin, generic.DetailView):
    """
    Detail for a particular variation record
    """
    model = Variation

    def test_func(self, *args, **kwargs):
        variation = get_object_or_404(Variation, pk=self.kwargs['pk'])
        return self.request.user.is_active and variation.project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(VariationDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class VariationCreate(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Create a new variation record
    """
    model = Variation
    fields = ('project', 'title', 'work_order', 'activity', 'description', 'status', 'recieved_date', 'recieved_letter', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Variation created successfully.'

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active and self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(VariationCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class VariationUpdate(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update a particular variation record
    """
    model = Variation
    fields = ('title', 'work_order', 'activity', 'description', 'status', 'recieved_date', 'recieved_letter', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Variation updated successfully.'

    def test_func(self, *args, **kwargs):
        variation = get_object_or_404(Variation, pk=self.kwargs['pk'])
        return self.request.user.is_active and self.request.user.is_staff and variation.project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(VariationUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class VariationDelete(UserPassesTestMixin, DeleteView):
    """
    Delete a particular variation record
    """
    model = Variation
    success_url = '/dashboard/variations/'
    success_message = 'Variation deleted successfully.'

    def test_func(self, *args, **kwargs):
        variation = get_object_or_404(Variation, pk=self.kwargs['pk'])
        return self.request.user.is_active and self.request.user.is_staff and variation.project.contractor == self.request.user.profile.contractor

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(VariationDelete, self).delete(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(VariationDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class ClaimList(UserPassesTestMixin, generic.ListView):
    """
    Lists all time claims for all project
    """
    model = Claim

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active

    def get_queryset(self, *args, **kwargs):
        return Claim.objects.filter(project__contractor=self.request.user.profile.contractor).order_by('-updated_at')

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimList, self).get_context_data(*args, **kwargs)
        context['all_claim_list'] = Claim.objects.filter(project__contractor=self.request.user.profile.contractor).order_by('-updated_at')
        context['submitted_claim_list'] = Claim.objects.filter(project__contractor=self.request.user.profile.contractor).filter(status__group=3).order_by('-updated_at')
        context['approved_claim_list'] = Claim.objects.filter(project__contractor=self.request.user.profile.contractor).filter(status__group=4).order_by('-updated_at')
        context['page_name'] = 'time claims'
        return context

class ClaimDetail(UserPassesTestMixin, generic.DetailView):
    """
    Detail for a particular time extension claim record
    """
    model = Claim

    def test_func(self, *args, **kwargs):
        claim = get_object_or_404(Claim, pk=self.kwargs['pk'])
        return self.request.user.is_active and claim.project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context

class ClaimCreate(UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Create a new time extension claim record
    """
    model = Claim
    fields = ('project', 'title', 'number', 'description', 'status', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Time claim created successfully.'

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active and self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context

class ClaimUpdate(UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update a particular time claim record
    """
    model = Claim
    fields = ('title', 'number', 'description', 'status', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Time claim updated successfully.'

    def test_func(self, *args, **kwargs):
        claim = get_object_or_404(Claim, pk=self.kwargs['pk'])
        return self.request.user.is_active and self.request.user.is_staff and claim.project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context

class ClaimDelete(UserPassesTestMixin, DeleteView):
    """
    Delete a particular time claim record
    """
    model = Claim
    success_url = '/dashboard/claims/'
    success_message = 'Time claim deleted successfully.'

    def test_func(self, *args, **kwargs):
        claim = get_object_or_404(Claim, pk=self.kwargs['pk'])
        return self.request.user.is_active and self.request.user.is_staff and claim.project.contractor == self.request.user.profile.contractor

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ClaimDelete, self).delete(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context

class InsuranceList(UserPassesTestMixin, generic.ListView):
    """
    Lists all time claims for all project
    """
    model = Insurance

    def test_func(self, *args, **kwargs):
        return self.request.user.is_active

    def get_queryset(self, *args, **kwargs):
        return Insurance.objects.filter(project__contractor=self.request.user.profile.contractor).filter(status__level=10).order_by('end_date')

    def get_context_data(self, *args, **kwargs):
        context = super(InsuranceList, self).get_context_data(*args, **kwargs)
        context['expired_insurance_list'] = Insurance.objects.filter(project__contractor=self.request.user.profile.contractor).filter(status__level=310)
        context['page_name'] = 'insurances'
        # Run update status code
        update_ins_status()        
        return context

class InsuranceDetail(UserPassesTestMixin, generic.DetailView):
    """
    Detail for a particular insurance record
    """
    model = Insurance

    def test_func(self, *args, **kwargs):
        insurance = get_object_or_404(Insurance, pk=self.kwargs['pk'])
        return self.request.user.is_active and insurance.project.contractor == self.request.user.profile.contractor

    def get_context_data(self, *args, **kwargs):
        context = super(InsuranceDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'insurances'
        return context
