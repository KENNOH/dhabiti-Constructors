from django.conf.urls import url,include
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^view_client_bookings/', views.view_client_bookings,name='view_client_bookings'),
	url(r'^view_service/(?P<urlhash>[0-9A-Za-z_\-]+)/$', views.view_service, name='view_service'),
    url(r'^book_appointment/(?P<urlhash>[0-9A-Za-z_\-]+)/$',views.create_booking, name='create_booking'),
    url(r'^process_payment/(?P<id>[0-9A-Za-z_\-]+)/$',views.process_payment, name='process_payment'),
    url(r'^process_lnms/$',views.process_lnm, name='process_lnm'),
    url(r'^sort/(?P<Username>[\w.@+-]+)',views.filter_services, name='sort'),

]
