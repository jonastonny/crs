from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^profile/$', views.profile_detail, name='profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^profile/update/$', views.profile_update, name='profile_update'),
    url(r'^home/$', views.IndexView.as_view(), name='index'),
]
