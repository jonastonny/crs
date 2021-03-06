from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    # ROOM
    url(r'^room/create/$', views.CreateRoomView.as_view(), name='room_create'),
    url(r'^room/(?P<pk>[0-9]+)/$', views.RoomDetailView.as_view(), name='room_detail'),
    url(r'^room/(?P<room>[0-9]+)/edit/$', views.room_edit, name='room_edit'),
    url(r'^room/(?P<room>[0-9]+)/delete/$', views.room_delete, name='room_delete'),
    url(r'^room/(?P<room>[0-9]+)/update/$', views.room_update, name='room_update'),
    url(r'^room/(?P<room>[0-9]+)/subscribe/$', views.room_subscribe, name='room_subscribe'),
    # QUESTION GROUP
    url(r'^room/(?P<room>[0-9]+)/group/create/$', views.questingroup_create, name='questiongroup_create'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<pk>[0-9]+)/$', views.QuestionGroupDetailView.as_view(), name='questiongroup_detail'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/edit/$', views.questiongroup_edit, name='questiongroup_edit'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/update/$', views.questiongroup_update, name='questiongroup_update'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/toggle/$', views.questiongroup_toggle, name='questiongroup_toggle'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/delete/$', views.questiongroup_delete, name='questiongroup_delete'),
    # QUESTION
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/create/$', views.question_answer_create, name='question_create'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<pk>[0-9]+)/$', views.QuestionDetailView.as_view(), name='question_detail'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<question>[0-9]+)/edit/$', views.question_answer_edit, name='question_edit'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<question>[0-9]+)/update/$', views.question_answer_update, name='question_update'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<question>[0-9]+)/delete/$', views.question_delete, name='question_delete'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<question>[0-9]+)/toggle/$', views.question_toggle, name='question_toggle'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<question>[0-9]+)/responses/$', views.question_response, name='question_response'),
    # ANSWERS
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<question>[0-9]+)/response/$', views.answer_response, name='answer_response'),
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<question>[0-9]+)/answer/(?P<answer>[0-9]+)/delete/$', views.answer_delete, name='answer_delete'),
    # DATA
    url(r'^room/(?P<room>[0-9]+)/group/(?P<questiongroup>[0-9]+)/question/(?P<question>[0-9]+)/responses/data$', views.get_response_data, name='response_data'),

]
