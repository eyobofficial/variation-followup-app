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
]