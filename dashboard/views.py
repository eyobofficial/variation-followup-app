from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Import Message Framework
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Import models
from .models import (Consultant,
                     Contractor,
                     Project,
                     Status,
                     Variation,
                     Claim)

def index(request):
    return render(request, 'dashboard/index.html', {
            'page_name': 'dashboard',
        })

class VariationList(generic.ListView):
    """
    Lists all variations for all project
    """
    model = Variation

    def get_queryset(self, *args, **kwargs):
        return Variation.objects.all().order_by('-updated_at')

    def get_context_data(self, *args, **kwargs):
        context = super(VariationList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class VariationDetail(generic.DetailView):
    """
    Detail for a particular variation record
    """
    model = Variation

    def get_context_data(self, *args, **kwargs):
        context = super(VariationDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class VariationCreate(SuccessMessageMixin, CreateView):
    """
    Create a new variation record
    """
    model = Variation
    fields = ('project', 'title', 'work_order', 'description', 'status', 'recieved_date', 'recieved_letter', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Variation created successfully.'

    def get_context_data(self, *args, **kwargs):
        context = super(VariationCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class VariationUpdate(SuccessMessageMixin, UpdateView):
    """
    Update a particular variation record
    """
    model = Variation
    fields = ('title', 'work_order', 'description', 'status', 'recieved_date', 'recieved_letter', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Variation updated successfully.'

    def get_context_data(self, *args, **kwargs):
        context = super(VariationUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class VariationDelete(DeleteView):
    """
    Delete a particular variation record
    """
    model = Variation
    success_url = '/dashboard/variations/'
    success_message = 'Variation deleted successfully.'

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(VariationDelete, self).delete(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(VariationDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class ClaimList(generic.ListView):
    """
    Lists all time claims for all project
    """
    model = Claim

    def get_queryset(self, *args, **kwargs):
        return Claim.objects.all().order_by('-updated_at')

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimList, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context

class ClaimDetail(generic.DetailView):
    """
    Detail for a particular time extension claim record
    """
    model = Claim

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimDetail, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context

class ClaimCreate(SuccessMessageMixin, CreateView):
    """
    Create a new time extension claim record
    """
    model = Claim
    fields = ('project', 'title', 'number', 'description', 'status', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Time claim created successfully.'

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context

class ClaimUpdate(SuccessMessageMixin, UpdateView):
    """
    Update a particular time claim record
    """
    model = Claim
    fields = ('title', 'number', 'description', 'status', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Time claim updated successfully.'

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimUpdate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context

class ClaimDelete(DeleteView):
    """
    Delete a particular time claim record
    """
    model = Claim
    success_url = '/dashboard/claims/'
    success_message = 'Time claim deleted successfully.'

    def delete(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ClaimDelete, self).delete(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ClaimDelete, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'time claims'
        return context