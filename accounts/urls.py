from django.conf.urls import url,include
from . import views


urlpatterns = [
	url(r'^accounts/login/',views.site,name='login'),
    #url(r'^$', views.activate, name='activate'),   
    url(r'^register/',views.register_view,name='register'),
    url(r'^logout/',views.logout_page,name='logout'), 
    url(r'^reset/',views.reset_view,name='reset'),
    url(r'^refer/',views.refer_view,name='refer'),
    url(r'^success/',views.success,name='success'),
]
