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
                     Variation,)

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

class VariationCreate(SuccessMessageMixin, CreateView):
    """
    Update a particular variation record
    """
    model = Variation
    fields = ('project', 'title', 'work_order', 'description', 'status', 'recieved_date', 'recieved_letter', 'submitted_amount', 'submitted_date', 'submitted_letter', 'approved_amount', 'approved_date', 'approved_letter', 'remark', )
    success_message = 'Variation created successfully.'

    def get_context_data(self, *args, **kwargs):
        context = super(VariationCreate, self).get_context_data(*args, **kwargs)
        context['page_name'] = 'variations'
        return context

class VariationDelete(SuccessMessageMixin, DeleteView):
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