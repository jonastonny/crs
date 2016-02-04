from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'authentication/login_form.html'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^reset/$', views.reset_password, {'post_reset_redirect': '/authentication/reset/done/'}, name='reset_password'),
    url(r'reset/done/$', views.reset_password_done, name='reset_password_done'),
    url('^', include('django.contrib.auth.urls')),  # same as the following lines
    # ^login/$ [name='login']
    # ^logout/$ [name='logout']
    # ^password_change/$ [name='password_change']
    # ^password_change/done/$ [name='password_change_done']
    # ^password_reset/$ [name='password_reset']
    # ^password_reset/done/$ [name='password_reset_done']
    # ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
    # ^reset/done/$ [name='password_reset_complete']
]
