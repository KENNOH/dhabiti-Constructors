from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^dashboard/client/', views.client_home, name='client_home'),   
    url(r'^dashboard/worker/(?P<pk>[0-9]+)$',views.service_expand,name='service_expand'), 
    url(r'^dashboard/worker/profile/', views.update_worker, name='update_worker'),
    url(r'^dashboard/worker/add/', views.add, name='add'),
    url(r'^dashboard/worker/', views.service_provider_home, name='service_provider_home'),
    url(r'^dashboard/transactions/', views.trans, name='trans'),
]
