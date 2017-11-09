from django.conf.urls import url 
from . import views

app_name = 'dashboard'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Variation URLS
    url(r'^variations/$', views.VariationList.as_view(), name='variation-list'),
    url(r'^variation/(?P<pk>[0-9]+)$', views.VariationDetail.as_view(), name='variation-detail'),   
    url(r'^variation/add/$', views.VariationCreate.as_view(), name='variation-create'),
    url(r'^variation/(?P<pk>[0-9]+)/update/$', views.VariationUpdate.as_view(), name='variation-update'),
    url(r'^variation/(?P<pk>[0-9]+)/delete/$', views.VariationDelete.as_view(), name='variation-delete'),

    # Time Claim URLS
    url(r'^claims/$', views.ClaimList.as_view(), name='claim-list'),
    url(r'^claim/(?P<pk>[0-9]+)$', views.ClaimDetail.as_view(), name='claim-detail'),
    url(r'^claim/add/$', views.ClaimCreate.as_view(), name='claim-create'),
    url(r'^claim/(?P<pk>[0-9]+)/update/$', views.ClaimUpdate.as_view(), name='claim-update'),
    url(r'^claim/(?P<pk>[0-9]+)/delete/$', views.ClaimDelete.as_view(), name='claim-delete'),

    # Insurance URLS
    url(r'^insurances/$', views.InsuranceList.as_view(), name='insurance-list'),
    url(r'^insurance/(?P<pk>[0-9]+)$', views.InsuranceDetail.as_view(), name='insurance-detail'),

    # Project URLs
    url(r'^projects/$', views.ProjectList.as_view(), name='project-list'),
    url(r'^project/(?P<pk>[0-9]+)$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^project/add/$', views.ProjectCreate.as_view(), name='project-create'),
    url(r'^project/(?P<pk>[0-9]+)/update/$', views.ProjectUpdate.as_view(), name='project-update'),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', views.ProjectDelete.as_view(), name='project-delete'),

    # Project Variation URLs
    url(r'^project/variation/(?P<pk>[0-9]+)$', views.ProjectVariationDetail.as_view(), name='project-variation-detail'),
    url(r'^project/(?P<project_pk>[0-9]+)/variation/create/$', views.ProjectVariationCreate.as_view(), name='project-variation-create'),
    url(r'^project/variation/(?P<pk>[0-9]+)/update$', views.ProjectVariationUpdate.as_view(), name='project-variation-update'),
    url(r'^project/(?P<project_pk>[0-9]+)/variation/(?P<pk>[0-9]+)/delete/$', views.ProjectVariationDelete.as_view(), name='project-variation-delete'),

    # Project Time Claim URLs
    url(r'^project/claim/(?P<pk>[0-9]+)$', views.ProjectClaimDetail.as_view(), name='project-claim-detail'),
    url(r'^project/(?P<project_pk>[0-9]+)/claim/create/$', views.ProjectClaimCreate.as_view(), name='project-claim-create'),
    url(r'^project/claim/(?P<pk>[0-9]+)/update$', views.ProjectClaimUpdate.as_view(), name='project-claim-update'),
    url(r'^project/(?P<project_pk>[0-9]+)/claim/(?P<pk>[0-9]+)/delete/$', views.ProjectClaimDelete.as_view(), name='project-claim-delete'),
]